from datetime import datetime
from typing import Any, Literal
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
    next_agent: Literal["product","order","complete"] = Field(
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

SYSTEM_INSTRUCTIONS = """You are a coordinator agent that routes requests to specialized agents.

Available agents:
- product: Handles product details, descriptions, pricing
- order: Handles new order creation, retrieving order history

Analyze the conversation history and determine which agent should handle the next step.
Choose 'complete' if the user's request has been fully addressed.
"""

def coordinator_node(state: AgentState) -> AgentState:
    """Decide routing and store only JSON-serializable data in state."""
    logging.getLogger().info(f"Using the following state to route the request: {state}")

    # Build messages without nesting and ensure elements are BaseMessage only.
    messages = [
        SystemMessage(content=SYSTEM_INSTRUCTIONS),
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

    state["next_agent"] = decision["structured_response"].next_agent

    logging.info("Returning state: %s", state)
    return state

def route_based_on_state(state: AgentState) -> str:
    """Simple function that reads from state"""
    return state["next_agent"]