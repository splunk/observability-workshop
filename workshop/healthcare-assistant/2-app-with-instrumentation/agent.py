"""LangGraph agent for the healthcare assistant."""
import asyncio
import inspect
import json
import threading
import uuid
from typing import Annotated, List, Dict, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from opentelemetry import context as otel_context

from config import TOOLS_DIR, load_config, load_system_prompt
from rag import create_rag_tool
from tools import logic as tools_logic

import os
from splunk_ao import splunk_ao_context
from splunk_ao.deployment import DeploymentMode, resolve_deployment
from splunk_ao.handlers.langchain import SplunkAOAsyncCallback

from splunk_ao.utils.log_config import enable_console_logging

enable_console_logging()

class State(TypedDict):
    messages: Annotated[list, add_messages]


_agent_loop: asyncio.AbstractEventLoop | None = None
_agent_loop_thread: threading.Thread | None = None
_agent_loop_lock = threading.Lock()


def _clear_otel_context() -> None:
    """Drop any leaked OTel span context before starting a new trace."""
    otel_context.attach(otel_context.Context())


def _ensure_agent_loop() -> asyncio.AbstractEventLoop:
    """Run agent async work on a dedicated stdlib asyncio loop (not uvloop)."""
    global _agent_loop, _agent_loop_thread
    with _agent_loop_lock:
        if _agent_loop is None:
            loop = asyncio.new_event_loop()

            def _run_loop() -> None:
                asyncio.set_event_loop(loop)
                loop.run_forever()

            thread = threading.Thread(
                target=_run_loop,
                daemon=True,
                name="healthcare-agent-async",
            )
            thread.start()
            _agent_loop = loop
            _agent_loop_thread = thread
    return _agent_loop


def _run_async(coro):
    """Run async agent code off Streamlit's uvloop thread."""
    loop = _ensure_agent_loop()
    return asyncio.run_coroutine_threadsafe(coro, loop).result()


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
        self._splunk_ao_context_manager = None
        # Open one Splunk AO context for the whole chat on the agent asyncio thread.
        _run_async(self._open_splunk_ao_session())

    async def _open_splunk_ao_session(self) -> None:
        """Bind project/stream and session once; avoid per-turn context exit flushes."""
        if self._splunk_ao_context_manager is not None:
            return

        self._splunk_ao_context_manager = splunk_ao_context(
            project=os.getenv("SPLUNK_AO_PROJECT"),
            agent_stream=os.getenv("SPLUNK_AO_AGENT_STREAM"),
        )
        self._splunk_ao_context_manager.__enter__()

        if resolve_deployment() == DeploymentMode.STANDALONE:
            # Standalone validates session IDs through CRUD before accepting OTLP spans.
            backend_session_id = splunk_ao_context.start_session(
                external_id=self.session_id,
            )
            splunk_ao_context.set_session(backend_session_id)
        else:
            # O11y accepts the Streamlit chat UUID directly (official SDK pattern).
            splunk_ao_context.set_session(self.session_id)

    async def _retry_export_if_rejected(self, splunk_ao_logger) -> None:
        """Standalone can reject the first OTLP batch; retry once after a short pause."""
        if resolve_deployment() != DeploymentMode.STANDALONE:
            return
        if splunk_ao_logger.export_health.healthy is not False:
            return
        await asyncio.sleep(2)
        await splunk_ao_logger.async_flush()

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

        async def invoke_chatbot(state):
            messages = list(state["messages"])
            if self.system_prompt:
                messages = [SystemMessage(content=self.system_prompt)] + messages
            message = await llm_with_tools.ainvoke(messages)
            return {"messages": [message]}

        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", invoke_chatbot)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        return graph_builder.compile()

    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        if self.graph is None:
            self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        splunk_ao_logger = splunk_ao_context.get_logger_instance()
        splunk_ao_logger.reset_parent_tracking()
        _clear_otel_context()

        # One callback per request keeps each user turn in its own trace.
        callback = SplunkAOAsyncCallback(flush_on_chain_end=True)
        run_config = {
            "configurable": {"thread_id": str(uuid.uuid4())},
            "callbacks": [callback],
        }

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            run_config,
        )
        await self._retry_export_if_rejected(splunk_ao_logger)

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
