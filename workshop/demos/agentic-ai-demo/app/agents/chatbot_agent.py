from typing import Any, Dict, List, Union, Optional
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from models.schemas import OrderRequest
from tools.order_tool import fetch_orders_for_customer
from shared.create_llm import _create_llm
from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)

llm = _create_llm("chat_agent", temperature=0.2, session_id=None)
llm_with_tools = llm.bind_tools([fetch_orders_for_customer])

agent = _create_react_agent(llm_with_tools, tools=[fetch_orders_for_customer]).with_config(
    {
        "run_name": "chat_agent",
        "tags": ["agent", "agent:chat_agent"],
        "metadata": {
            "agent_name": "chat_agent",
        },
    }
)


TOOLS_BY_NAME: Dict[str, BaseTool] = {t.name: t for t in [fetch_orders_for_customer]}

SYSTEM_INSTRUCTIONS = (
    "You are a helpful support chatbot. Use tools when they can improve accuracy. "
    "For any order-related questions, prefer the 'fetch_orders_for_customer' tool. "
    "Do not fabricate order details. Keep answers concise and actionable."
)

def chat(customer_id: int, question: str) -> str:
    """
    Answers a user's question. The model may call tools; we enforce the caller's customer_id.
    """
    messages = [
        SystemMessage(SYSTEM_INSTRUCTIONS),
        # Provide relevant context explicitly.
        SystemMessage(f"Context: The current authenticated customer's ID is {customer_id}. "
                      "Never change this ID when calling tools."),
        HumanMessage(question),
    ]

    # First pass: let the model decide whether to call a tool.
    ai_msg: AIMessage = llm_with_tools.invoke(messages)

    if not getattr(ai_msg, "tool_calls", None):
        # Model answered directly.
        return ai_msg.content or ""

    # Execute each tool call and collect ToolMessage responses.
    tool_messages: List[ToolMessage] = []

    for call in ai_msg.tool_calls:
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
    final_ai: AIMessage = llm_with_tools.invoke(messages + [ai_msg] + tool_messages)
    return final_ai.content or ""

