from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langchain_core.tools import BaseTool
from models.schemas import AgentState
from tools.product_tool import get_products_by_sku, get_all_products
from shared.create_llm import _create_llm

from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

llm = _create_llm("product_agent", temperature=0.2, session_id=None)

agent = _create_react_agent(llm, tools=[get_products_by_sku, get_all_products]).with_config(
    {
        "run_name": "product_agent",
        "tags": ["agent", "agent:product_agent"],
        "metadata": {
            "agent_name": "product_agent",
        },
    }
)

SYSTEM_INSTRUCTIONS = (
    "You are an product specialist.  Answer questions about product details, specifications, and features. "
    "Use tools when they can improve accuracy. "
    "Do not fabricate product details. Keep answers concise and actionable."
)

TOOLS_BY_NAME: Dict[str, BaseTool] = {t.name: t for t in [get_products_by_sku, get_all_products]}

def product_agent(state: AgentState):
    """Handle product-related requests"""

    # Build messages without nesting.
    messages = [
        SystemMessage(content=SYSTEM_INSTRUCTIONS),
        SystemMessage(content=f"Context: The current authenticated customer's ID is {state['customer_id']}. Never change this ID when calling tools."),
    ]

    # If state["messages"] is a single BaseMessage, append it; if it's a list, extend.
    prior = state["messages"]

    if isinstance(prior, BaseMessage):
        messages.append(prior)
    else:
        messages.extend(prior)

    results = agent.invoke({"messages": messages})

    msgs = results["messages"]

    last_ai = next((m for m in reversed(msgs) if isinstance(m, AIMessage)), None)
    if last_ai is None:
        return ""

    logging.getLogger().info(f"last_ai: {last_ai}")

    if not getattr(last_ai, "tool_calls", None):
        # Model answered directly.
        return last_ai.content or ""

    # Execute each tool call and collect ToolMessage responses.
    tool_messages: List[ToolMessage] = []

    for call in last_ai.tool_calls:
        tool_name: str = call["name"]
        tool_args: Dict[str, Any] = call.get("args", {}) or {}

        tool = TOOLS_BY_NAME.get(tool_name)
        if tool is None:
            # Unknown tool; inform the model.
            tool_messages.append(
                ToolMessage(
                    content=f"Error: requested unknown tool '{tool_name}'.",
                    tool_call_id=call["id"],
                )
            )
            continue

        # Enforce customer_id from the authenticated session.
        tool_args["customer_id"] = customer_id

        try:
            result = tool.invoke(tool_args)  # Tools are Runnables in LangChain 0.2+
            # Keep the tool result compact; large payloads can be summarized first if needed.
            tool_messages.append(
                ToolMessage(
                    content=str(result),  # Or json.dumps(result) if you prefer strict JSON
                    tool_call_id=call["id"],
                )
            )
        except Exception as e:
            tool_messages.append(
                ToolMessage(
                    content=f"Tool execution failed: {type(e).__name__}: {e}",
                    tool_call_id=call["id"],
                )
            )

    # Second pass: give the model the tool outputs to produce a final answer.
    all_messages = initial_messages + [last_ai] + tool_messages
    response = agent.invoke({"messages": all_messages})

    return {"messages": [response]}


