from datetime import datetime
from typing import Any, Literal, Dict, Tuple, List
from pydantic import BaseModel, Field
from models.schemas import AgentState
from shared.create_llm import _create_llm
from langchain_core.messages import BaseMessage, SystemMessage
from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)

import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RoutingDecision(BaseModel):
    """Decision about which agent to route to next"""
    next_agent: Literal["product","order","inventory","complete"] = Field(
        description="The next agent to route to, or 'complete' if the task is done"
    )
    reasoning: str = Field(
        description="Brief explanation of why this agent was chosen"
    )

llm = _create_llm("coordinator_agent", temperature=0.2, session_id=None)

agent = _create_react_agent(llm, tools=[], response_format=RoutingDecision).with_config(
    {
        "run_name": "coordinator_agent",
        "tags": ["agent", "agent:coordinator_agent"],
        "metadata": {
            "agent_name": "coordinator_agent",
        },
    }
)

AGENT_CATALOG: Dict[str, Tuple[str, str]] = {
    # name: (description, state_field_name)
    "product": (
        "Handles product details, descriptions, pricing.",
        "product_summary",
    ),
    "order": (
        "Handles new order creation, retrieving order history.",
        "order_summary",
    ),
    "inventory": (
        "Handles inventory requests, such as getting the current inventory for a product and store, or decrementing inventory when an order is placed.",
        "inventory_summary",
    ),
}

def _is_invoked(value: Any) -> bool:
    # Treat None/empty string/whitespace as not invoked.
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    return bool(value)

def remaining_agents_from_state(state: dict) -> List[str]:
    remaining = []
    for agent_name, (_, field_name) in AGENT_CATALOG.items():
        invoked = _is_invoked(state.get(field_name))
        if not invoked:
            remaining.append(agent_name)
    return remaining

def build_system_instructions(state: dict) -> str:
    remaining = remaining_agents_from_state(state)

    if remaining:
        lines = [
            "You are a coordinator agent that routes requests to specialized agents.",
            "",
            "Available agents:",
        ]
        for name in remaining:
            desc = AGENT_CATALOG[name][0]
            lines.append(f"- {name}: {desc}")
        lines.extend([
            "",
            "Rules:",
            f"- Only choose one of: {', '.join(remaining)}.",
            "- Choose 'complete' if the user's request has been fully addressed.",
            "- There's no need to use all of the agents once. Only use agents that are needed to fulfill the request.",
            "- Do not choose agents that are not listed as available.",
        ])
    else:
        # Nothing left to call.
        lines = [
            "You are a coordinator agent that routes requests to specialized agents.",
            "",
            "Available agents:",
            "- None remaining; all specialized agents have already been invoked.",
            "",
            "Rules:",
            "- Choose 'complete' if the user's request has been fully addressed.",
            "- There's no need to use all of the agents once. Only use agents that are needed to fulfill the request.",
            "- Do not choose agents that are not listed as available.",
        ]
    return "\n".join(lines)

def coordinator_node(state: AgentState) -> AgentState:
    """Decide routing and store only JSON-serializable data in state."""
    logging.getLogger().info(f"Using the following state to route the request: {state}")

    # Build dynamic coordinator instructions based on which agents remain.
    dynamic_system = build_system_instructions(state)

    # Build messages without nesting and ensure elements are BaseMessage only.
    messages = [
        SystemMessage(content=dynamic_system),
        SystemMessage(content=f"Context: The current authenticated customer's ID is {state['customer_id']}. Never change this ID when calling tools."),
    ]

    prior = state.get("messages", [])
    logging.getLogger().debug("Prior messages type: %s", type(prior))

    if isinstance(prior, BaseMessage):
        messages.append(prior)
    elif isinstance(prior, list):
        # Filter out any non-BaseMessage items (e.g., avoid storing RoutingDecision here)
        for m in prior:
            if isinstance(m, BaseMessage):
                messages.append(m)
            else:
                logging.getLogger().warning("Skipping non-message item in prior messages: %s", type(m))
    else:
        logging.getLogger().warning("Unexpected 'messages' value in state: %s", type(prior))

    logging.getLogger().info("About to invoke the agent with %d messages", len(messages))

    logging.getLogger().info("messages types/reprs: %s",
        [(type(m).__name__, repr(m)[:200]) for m in messages])

    decision = agent.invoke({"messages": messages})

    logging.info("Routing decision (not serialized): %s", decision)

    next_agent = decision["structured_response"].next_agent

    # validate the model's choice to avoid calling agents already used.
    remaining = set(remaining_agents_from_state(state))
    if next_agent not in remaining and next_agent != "complete":
        logger.warning(
            "Model chose unavailable agent '%s'. Remaining: %s. Coercing to 'complete'.",
            next_agent, sorted(remaining)
        )
        next_agent = "complete"

    state["next_agent"] = next_agent

    logging.info("Returning state: %s", state)
    return state

def route_based_on_state(state: AgentState) -> str:
    """Simple function that reads from state"""
    return state["next_agent"]