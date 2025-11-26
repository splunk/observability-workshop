from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langchain_core.tools import BaseTool
from models.schemas import AgentState
from tools.inventory_tool import get_inventory_for_products_and_stores, batch_decrement_inventory, batch_upsert_increment_inventory
from shared.create_llm import _create_llm

from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

llm = _create_llm("inventory_agent", temperature=0.2, session_id=None)

agent = _create_react_agent(llm, tools=[get_inventory_for_products_and_stores, batch_decrement_inventory, batch_upsert_increment_inventory]).with_config(
    {
        "run_name": "inventory_agent",
        "tags": ["agent", "agent:inventory_agent"],
        "metadata": {
            "agent_name": "inventory_agent",
        },
    }
)

SYSTEM_INSTRUCTIONS = (
    "You are an inventory specialist.  Answer questions about product inventory. "
    "Decrement inventory by the specified quantity for a specific product_sku and store_id when a new order is placed. "
    "Increment inventory by the specified quantity for a specific product_sku and store_id when requested as part of inventory replenishment. "
    "Use tools when they can improve accuracy. "
    "Do not fabricate inventory details. Keep answers concise and actionable."
)

TOOLS_BY_NAME: Dict[str, BaseTool] = {t.name: t for t in [get_inventory_for_products_and_stores, batch_decrement_inventory, batch_upsert_increment_inventory]}

def inventory_agent(state: AgentState):
    """Handle inventory-related requests"""
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

    # keep track of the response from the inventory agent separately
    state["inventory_summary"] = (
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


