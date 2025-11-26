from datetime import datetime
from typing import Any, Literal, Dict, Tuple, List
from pydantic import BaseModel, Field
from models.schemas import AgentState
from shared.create_llm import _create_llm
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)

import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# New structured response for final selection (invoked only after next_agent == 'complete').
class FinalAnswerDecision(BaseModel):
    selected_agent: Literal["product", "order", "inventory", "payment", "none"] = Field(
        description="Agent whose summary best fulfills the user's request; use 'none' if none suffice."
    )
    final_answer: str = Field(
        description="User-facing answer derived from the selected agent's summary (concise, natural language)."
    )
    reasoning: str = Field(description="Brief justification for the selection")


# 2) Create a dedicated, deterministic LLM/agent to select the final answer.
final_selector_llm = _create_llm("final_selector_agent", temperature=0.0, session_id=None)

final_selector_agent = _create_react_agent(
    final_selector_llm,
    tools=[],
    response_format=FinalAnswerDecision,
).with_config(
    {
        "run_name": "final_selector_agent",
        "tags": ["agent", "agent:final_selector_agent"],
        "metadata": {"agent_name": "final_selector_agent"},
    }
)


def build_final_selector_instructions(invoked_summaries: Dict[str, str]) -> str:
    lines = [
        "You are a final-answer selector. Choose the single best user-facing answer from the provided agent summaries.",
        "",
        "Candidate summaries:",
    ]
    for agent_name, summary in invoked_summaries.items():
        lines.append(f"- {agent_name}: {summary}")
    lines.extend([
        "",
        "Rules:",
        "- Consider only the candidate summaries above; do not invent facts.",
        "- Choose the summary that most directly and completely answers the user's request.",
        "- If none suffice, choose 'none'.",
        "- Return a single FinalAnswerDecision with selected_agent, final_answer, and reasoning.",
    ])
    return "\n".join(lines)

class RoutingDecision(BaseModel):
    """Decision about which agent to route to next"""
    next_agent: Literal["product","order","inventory","payment","complete"] = Field(
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
    "payment": (
        "Handles payment requests, such as processing a payment when a new order is created.",
        "payment_summary",
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
            "- Include on a single RoutingDecision in your response.",
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
            "- Include on a single RoutingDecision in your response.",
            "- Do not choose agents that are not listed as available.",
        ]
    return "\n".join(lines)

def coordinator_node(state: AgentState) -> AgentState:
    """Decide routing; only run final selector after the coordinator decides 'complete'."""
    logger.info("Using the following state to route the request: %s", state)

    # 1) Build coordinator messages and invoke routing decision as before.
    dynamic_system = build_system_instructions(state)
    messages: List[BaseMessage] = [
        SystemMessage(content=dynamic_system),
        SystemMessage(content=f"Context: The current authenticated customer's ID is {state['customer_id']}. Never change this ID when calling tools."),
    ]

    prior = state.get("messages", [])
    if isinstance(prior, BaseMessage):
        messages.append(prior)
    elif isinstance(prior, list):
        for m in prior:
            if isinstance(m, BaseMessage):
                messages.append(m)
            else:
                logger.warning("Skipping non-message item in prior messages: %s", type(m))
    else:
        logger.warning("Unexpected 'messages' value in state: %s", type(prior))

    logger.info("About to invoke the coordinator with %d messages", len(messages))
    decision = agent.invoke({"messages": messages})
    logger.info("Routing decision (not serialized): %s", decision)

    next_agent = decision["structured_response"].next_agent
    remaining = set(remaining_agents_from_state(state))
    if next_agent not in remaining and next_agent != "complete":
        logger.warning(
            "Model chose unavailable agent '%s'. Remaining: %s. Coercing to 'complete'.",
            next_agent, sorted(remaining)
        )
        next_agent = "complete"
    state["next_agent"] = next_agent

    # 2) Only now, if the coordinator chose 'complete', run the final selector once.
    if next_agent == "complete" and not state.get("finalized_by_selector"):
        # Gather candidate summaries that were actually populated.
        invoked_summaries: Dict[str, str] = {}
        for agent_name, (_, field_name) in AGENT_CATALOG.items():
            val = state.get(field_name)
            if _is_invoked(val):
                invoked_summaries[agent_name] = str(val)

        if invoked_summaries:
            selector_system = build_final_selector_instructions(invoked_summaries)

            # Include the original user message for alignment.
            user_msg = None
            for m in messages:
                if isinstance(m, HumanMessage):
                    user_msg = m
                    break

            selector_messages: List[BaseMessage] = [SystemMessage(content=selector_system)]
            if user_msg is not None:
                selector_messages.append(user_msg)
            else:
                logger.warning("No HumanMessage found; final selector will rely on summaries only.")

            sel_decision = final_selector_agent.invoke({"messages": selector_messages})

            selected_agent = sel_decision["structured_response"].selected_agent
            final_answer = sel_decision["structured_response"].final_answer

            if selected_agent != "none" and final_answer and final_answer.strip():
                state["final_answer"] = final_answer
                state["fulfilled_by"] = selected_agent
                state["finalized_by_selector"] = True
            else:
                # Fallback: choose a deterministic summary if selector can't decide.
                priority = ["order", "product", "inventory", "payment"]
                for p in priority:
                    if p in invoked_summaries and invoked_summaries[p].strip():
                        state["final_answer"] = invoked_summaries[p]
                        state["fulfilled_by"] = p
                        state["finalized_by_selector"] = True
                        break

                if not state.get("final_answer"):
                    logger.warning("Final selector returned 'none' and no fallback available.")

    logger.info("Returning state: %s", state)
    return state

def route_based_on_state(state: AgentState) -> str:
    """Simple function that reads from state"""
    return state["next_agent"]