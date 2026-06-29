"""LangGraph agent for the healthcare assistant."""
import asyncio
import inspect
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Any, Dict, List, Optional, TypedDict

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

from agent_control import ControlSteerError, ControlViolationError, control
from helpers.agent_control_helpers import (
    build_agent_control_steps,
    ensure_trace_started,
    finalize_trace,
    format_blocked_message,
    init_agent_control,
    infer_control_step_name,
    make_controlled_tool,
    notify_control_block,
    uses_internal_sql_control,
)

LLM_STEP_NAME = "Healthcare Assistant"
MAX_STEER_RETRIES = 3


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


def _message_content_text(message: BaseMessage) -> str:
    """Return plain text from an LLM message for steering retries."""
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)
        return "\n".join(part for part in text_parts if part)
    return str(content)


def _build_steering_retry_messages(
    messages: List[BaseMessage],
    original_output: AIMessage,
    steer_error: ControlSteerError,
) -> List[BaseMessage]:
    """Build a follow-up prompt with the original input, output, and steering guidance."""
    steering_instructions = (
        steer_error.steering_context
        or steer_error.message
        or str(steer_error)
    )
    original_text = _message_content_text(original_output)

    retry_messages = list(messages)
    retry_messages.append(
        AIMessage(
            content=original_text,
            tool_calls=getattr(original_output, "tool_calls", None) or [],
        )
    )
    retry_messages.append(
        HumanMessage(
            content=(
                "Your previous response was flagged by Agent Control and needs to be revised.\n\n"
                f"Your previous response:\n{original_text}\n\n"
                "Follow these instructions to generate a corrected response:\n"
                f"{steering_instructions}"
            )
        )
    )
    return retry_messages


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
        self._control_steps: list[dict] | None = None

    def _init_agent_control(self, galileo_logger) -> None:
        if galileo_logger is None or self._control_steps is None:
            return
        galileo_logger.enable_agent_control()
        init_agent_control(
            galileo_logger,
            project_name=os.getenv("GALILEO_PROJECT", ""),
            log_stream=os.getenv("GALILEO_LOG_STREAM", ""),
            agent_description="Healthcare assistant demo agent",
            steps=self._control_steps,
        )

    def load_tools(self) -> None:
        tool_schema_path = TOOLS_DIR / "schema.json"
        with tool_schema_path.open(encoding="utf-8") as f:
            tool_schema = json.load(f)

        tool_names = [schema.get("name") for schema in tool_schema if schema.get("name")]
        self._control_steps = build_agent_control_steps(LLM_STEP_NAME, tool_names)

        self.tools = []
        for tool_func in tools_logic.TOOLS:
            func_name = tool_func.__name__
            if not uses_internal_sql_control(func_name) and not getattr(
                tool_func, "_agent_control_step", None
            ):
                step_name = infer_control_step_name(func_name)
                tool_func = make_controlled_tool(tool_func, step_name)
                print(f"   🛡️ Agent Control step '{step_name}' → {func_name}")

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
            name=LLM_STEP_NAME,
        ).bind_tools(self.tools)

        last_llm_output: Dict[str, Any] = {"message": None}

        @control(step_name=LLM_STEP_NAME)
        async def _invoke_llm(msgs, config: RunnableConfig):
            result = await llm_with_tools.ainvoke(msgs, config)
            last_llm_output["message"] = result
            return result

        async def invoke_chatbot(state, config: RunnableConfig):
            messages = list(state["messages"])
            if self.system_prompt:
                messages = [SystemMessage(content=self.system_prompt)] + messages

            llm_messages = messages
            last_llm_output["message"] = None
            message = None

            for attempt in range(MAX_STEER_RETRIES):
                try:
                    message = await _invoke_llm(llm_messages, config)
                    break
                except ControlViolationError as e:
                    notify_control_block(e, step_name=LLM_STEP_NAME)
                    message = AIMessage(
                        content=format_blocked_message(e, step_name=LLM_STEP_NAME)
                    )
                    break
                except ControlSteerError as e:
                    notify_control_block(
                        e, step_name=LLM_STEP_NAME, guardrail_result="steered"
                    )
                    if attempt >= MAX_STEER_RETRIES - 1 or last_llm_output["message"] is None:
                        message = AIMessage(
                            content=format_blocked_message(
                                e, step_name=LLM_STEP_NAME, steered=True
                            )
                        )
                        break
                    llm_messages = _build_steering_retry_messages(
                        llm_messages, last_llm_output["message"], e
                    )
                    last_llm_output["message"] = None

            if message is None:
                message = AIMessage(content="No response generated")
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
        galileo_logger,
    ):
        if galileo_logger.experiment_id is None:
            galileo_context.start_session(external_id=self.session_id)

        # Nest LangGraph spans under the trace started by ensure_trace_started().
        callback = GalileoAsyncCallback(
            galileo_logger,
            start_new_trace=False,
            flush_on_chain_end=False,
        )
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

        response = "No response generated"

        if in_experiment:
            galileo_logger = experiment_logger
            self._init_agent_control(galileo_logger)
            ensure_trace_started(galileo_logger, langchain_messages, trace_name="Run Agent")
            try:
                result = await self._invoke_graph(
                    langchain_messages,
                    galileo_logger=galileo_logger,
                )
                if result["messages"]:
                    response = result["messages"][-1].content
                return response
            finally:
                finalize_trace(galileo_logger, response)
        else:
            with galileo_context(
                project=os.getenv("GALILEO_PROJECT"),
                log_stream=os.getenv("GALILEO_LOG_STREAM"),
            ):
                galileo_logger = galileo_context.get_logger_instance()
                self._init_agent_control(galileo_logger)
                ensure_trace_started(galileo_logger, langchain_messages, trace_name="Run Agent")
                try:
                    result = await self._invoke_graph(
                        langchain_messages,
                        galileo_logger=galileo_logger,
                    )
                    if result["messages"]:
                        response = result["messages"][-1].content
                    return response
                finally:
                    finalize_trace(galileo_logger, response)

    def process_query(self, messages: List[Dict[str, str]]) -> str:
        try:
            return _run_async(self._process_query_async(messages))
        except ControlViolationError as e:
            return format_blocked_message(e, step_name=LLM_STEP_NAME)
        except ControlSteerError as e:
            return format_blocked_message(e, step_name=LLM_STEP_NAME, steered=True)
        except Exception as e:
            print(f"[ERROR] Error processing query: {e}")
            import traceback

            traceback.print_exc()
            return f"Error processing your request: {str(e)}"
