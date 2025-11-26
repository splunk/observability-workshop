from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from models.schemas import AgentState
from tools.order_tool import create_order, fetch_orders_for_customer
from shared.create_llm import _create_llm

from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

llm = _create_llm("order_agent", temperature=0.2, session_id=None)

agent = _create_react_agent(llm, tools=[create_order, fetch_orders_for_customer]).with_config(
    {
        "run_name": "order_agent",
        "tags": ["agent", "agent:order_agent"],
        "metadata": {
            "agent_name": "order_agent",
        },
    }
)

SYSTEM_INSTRUCTIONS = (
    "You are an order specialist that can answer questions about existing orders. "
    "If instructed, create a new order or modify an existing one. "
    "Use tools when they can improve accuracy. "
    "Don't pass 'null' for optional tool arguments, just exclude them. "
    "Do not fabricate order details. Keep answers concise and actionable."
)

TOOLS_BY_NAME: Dict[str, BaseTool] = {t.name: t for t in [create_order, fetch_orders_for_customer]}

def order_agent(state: AgentState):
    """Handle order-related requests"""

    logging.getLogger().info(f"In {__file__} with state:{state}")

    # Build messages without nesting.
    initial_messages = [
        SystemMessage(content=SYSTEM_INSTRUCTIONS),
        SystemMessage(content=f"Context: The current authenticated customer's ID is {state['customer_id']}. Never change this ID when calling tools."),
    ]

    # If state["messages"] is a single BaseMessage, append it; if it's a list, extend.
    prior = state["messages"]

    if isinstance(prior, BaseMessage):
        initial_messages.append(prior)
    else:
        initial_messages.extend(prior)

    logging.getLogger().info(f"In {__file__}, invoking LLM with: {initial_messages}")

    result = agent.invoke({"messages": initial_messages})
    logging.getLogger().info(f"In {__file__}, LLM returned: {result}")

    final_message = result["messages"][-1]
    logging.getLogger().info(f"In {__file__}, final_message: {final_message}")

    # keep track of the response from the order agent separately
    state["order_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )

    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )

    logging.getLogger().info(f"In {__file__}, returning state: {state}")

    return state


