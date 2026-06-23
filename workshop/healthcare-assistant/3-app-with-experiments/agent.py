"""LangGraph agent for the healthcare assistant."""
import asyncio
import inspect
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, List, Dict, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from config import TOOLS_DIR, load_config, load_system_prompt
from rag import create_rag_tool
from tools import logic as tools_logic

import os
from galileo import galileo_context
from galileo.handlers.langchain import GalileoAsyncCallback
from galileo.utils.log_config import enable_console_logging

enable_console_logging()

class State(TypedDict):
    messages: Annotated[list, add_messages]


def _run_async(coro):
    """Run an async coroutine from sync code (e.g. Streamlit)."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, coro).result()


class HealthcareAgent:
    """LangGraph healthcare assistant."""

    def __init__(
        self,
        session_id: str | None = None,
        model_override: Optional[str] = None,
    ):
        self.config = load_config()
        self.session_id = session_id or str(uuid.uuid4())
        self.model_override = model_override
        self.system_prompt = load_system_prompt()
        self.tools = []
        self.graph: CompiledStateGraph | None = None
        self.langgraph_config = {"configurable": {"thread_id": self.session_id}}

    def load_tools(self) -> None:
        tool_schema_path = TOOLS_DIR / "schema.json"
        with tool_schema_path.open(encoding="utf-8") as f:
            tool_schema = json.load(f)

        self.tools = []
        for tool_func in tools_logic.TOOLS:
            tool_schema_dict = next(
                (schema for schema in tool_schema if schema.get("name") == tool_func.__name__),
                None,
            )
            tool_kwargs = {
                "name": tool_func.__name__,
                "description": (
                    tool_schema_dict.get("description")
                    if tool_schema_dict
                    else tool_func.__doc__ or f"Tool: {tool_func.__name__}"
                ),
                "args_schema": tool_schema_dict.get("parameters") if tool_schema_dict else None,
            }
            if inspect.iscoroutinefunction(tool_func):
                langchain_tool = StructuredTool.from_function(coroutine=tool_func, **tool_kwargs)
            else:
                langchain_tool = StructuredTool.from_function(func=tool_func, **tool_kwargs)
            self.tools.append(langchain_tool)

        rag_config = self.config.get("rag", {})
        if rag_config.get("enabled", False):
            top_k = rag_config.get("top_k", 5)
            model_config = self.config.get("model", {})
            effective_model = (
                self.model_override
                or model_config.get("default_model")
                or model_config.get("model_name")
            )
            rag_tool = create_rag_tool(top_k, model_name=effective_model)
            self.tools.append(rag_tool)

        print(f"✓ Loaded {len(self.tools)} tools")

    def _build_graph(self) -> CompiledStateGraph:
        if not self.tools:
            raise ValueError("Tools not loaded. Call load_tools() first.")

        model_config = self.config.get("model", {})
        effective_model = (
            self.model_override
            or model_config.get("default_model")
            or model_config.get("model_name")
        )
        temperature = model_config.get("temperature", 0.1)

        llm_with_tools = ChatOpenAI(
            model=effective_model,
            temperature=temperature,
            name="Healthcare Assistant",
        ).bind_tools(self.tools)

        async def invoke_chatbot(state, config: RunnableConfig):
            messages = list(state["messages"])
            if self.system_prompt:
                messages = [SystemMessage(content=self.system_prompt)] + messages
            message = await llm_with_tools.ainvoke(messages, config)
            return {"messages": [message]}

        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", invoke_chatbot)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        return graph_builder.compile()

    async def _invoke_graph(
        self,
        langchain_messages: List[BaseMessage],
        *,
        in_experiment: bool,
        galileo_logger=None,
    ):
        if in_experiment:
            callback = GalileoAsyncCallback(
                galileo_logger,
                start_new_trace=False,
                flush_on_chain_end=False,
            )
        else:
            galileo_context.start_session(external_id=self.session_id)
            callback = GalileoAsyncCallback()

        run_config = {**self.langgraph_config, "callbacks": [callback]}
        return await self.graph.ainvoke({"messages": langchain_messages}, run_config)

    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        # Detect experiment mode before opening a log-stream context. Nested
        # galileo_context(project=..., log_stream=...) switches the singleton
        # logger key from experiment_id to log_stream, which hides the active
        # experiment trace and prevents LangGraph spans from nesting correctly.
        experiment_logger = galileo_context.get_logger_instance()
        in_experiment = experiment_logger.experiment_id is not None

        if in_experiment:
            result = await self._invoke_graph(
                langchain_messages,
                in_experiment=True,
                galileo_logger=experiment_logger,
            )
        else:
            with galileo_context(
                project=os.getenv("GALILEO_PROJECT"),
                log_stream=os.getenv("GALILEO_LOG_STREAM"),
            ):
                result = await self._invoke_graph(langchain_messages, in_experiment=False)

        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"

    def process_query(self, messages: List[Dict[str, str]]) -> str:
        try:
            return _run_async(self._process_query_async(messages))
        except Exception as e:
            print(f"[ERROR] Error processing query: {e}")
            import traceback

            traceback.print_exc()
            return f"Error processing your request: {str(e)}"
