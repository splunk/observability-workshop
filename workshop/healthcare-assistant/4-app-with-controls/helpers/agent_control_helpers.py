"""
Agent Control helper functions for runtime guardrails.
"""
import functools
import inspect
import json
import os
from typing import Any, Callable, Optional

import agent_control
from agent_control import ControlSteerError, ControlViolationError, control
from galileo.log_streams import get_log_stream

_initialized = False

# Hardcoded fallback when no domain tool list is available.
STANDARD_AGENT_CONTROL_STEPS = [
    {"type": "llm", "name": "Bank Assistant"},
    {"type": "tool", "name": "get_customer_info"},
    {"type": "tool", "name": "delete_customer_record"},
    {"type": "tool", "name": "retrieval_step"},
]

def format_blocked_message(
    error: Exception,
    step_name: str = "tool_step",
    *,
    steered: bool = False,
) -> str:
    """Return a user-friendly message for Agent Control blocks."""
    if steered:
        return (
            "This action was adjusted by Agent Control. "
            f"{error}"
        )
    return (
        "I'm sorry, this action was blocked by Agent Control. "
        "Please rephrase your request or try a different approach."
    )


def _serialize_messages(messages) -> list:
    serialized = []
    for msg in messages:
        if hasattr(msg, "type") and hasattr(msg, "content"):
            serialized.append({"role": msg.type, "content": msg.content})
        elif isinstance(msg, dict):
            serialized.append(msg)
    return serialized


def _extract_trace_input(messages) -> str:
    """Return the latest user message for trace input (matches reference guardrails app)."""
    for msg in reversed(list(messages)):
        if hasattr(msg, "type") and msg.type == "human" and hasattr(msg, "content"):
            return str(msg.content)
        if isinstance(msg, dict) and msg.get("role") in ("user", "human"):
            return str(msg.get("content", ""))
    serialized = _serialize_messages(messages)
    return json.dumps(serialized) if serialized else ""


def ensure_trace_started(
    galileo_logger,
    messages=None,
    *,
    trace_input: Optional[str] = None,
    trace_name: str = "Run Agent",
) -> None:
    """Start a Galileo trace when none is active (required before add_llm_span)."""
    if not galileo_logger or galileo_logger.current_parent() is not None:
        return
    if trace_input is None and messages is not None:
        trace_input = _extract_trace_input(messages)
    galileo_logger.start_trace(input=trace_input or "", name=trace_name)


def finalize_trace(galileo_logger, output: str) -> None:
    """Conclude and flush the active trace after a query completes."""
    if not galileo_logger or galileo_logger.current_parent() is None:
        return
    galileo_logger.conclude(output=output)
    galileo_logger.flush()


def notify_control_block(
    error: Exception,
    *,
    step_name: str,
    guardrail_result: str = "blocked",
) -> None:
    """Console notice for Agent Control blocks.

    Galileo LLM/tool spans come from LangChain callbacks (GalileoCallback).
    Control evaluation spans are emitted by enable_agent_control() on the logger.
    """
    label = "STEERED" if guardrail_result == "steered" else "BLOCKED"
    print(f"  🚫 {label} by Agent Control ({step_name}): {error}")


def infer_control_step_name(func_name: str) -> str:
    """Map tool function names to Agent Control step names."""
    if func_name.startswith("search_") or func_name.startswith("retrieve_"):
        return "retrieval_step"
    return func_name


def _handle_control_error(
    error: Exception,
    *,
    step_name: str,
    steered: bool = False,
) -> str:
    """Return a friendly JSON tool response for Agent Control blocks."""
    notify_control_block(
        error,
        step_name=step_name,
        guardrail_result="steered" if steered else "blocked",
    )
    payload = {
        "error": format_blocked_message(error, step_name, steered=steered),
    }
    if steered:
        payload["steered_by_agent_control"] = True
    else:
        payload["blocked_by_agent_control"] = True
    return json.dumps(payload)


def build_agent_control_steps(llm_step_name: str, tool_names: list[str]) -> list[dict]:
    """
    Build Agent Control step registrations for a domain.

    Tool step names must match @control(step_name=...) on tool handlers.
    Search/retrieval tools use the shared retrieval_step name.
    """
    steps: list[dict] = [{"type": "llm", "name": llm_step_name}]
    registered = {llm_step_name}

    for name in tool_names:
        step_name = infer_control_step_name(name)
        if step_name in registered:
            continue
        steps.append({"type": "tool", "name": step_name})
        registered.add(step_name)

    return steps


def _mark_as_agent_control_tool(func: Callable, step_name: str, tool_name: Optional[str] = None) -> str:
    """
    Mark a function as a tool before @control() infers step type.

    Agent Control uses func.tool_name (or func.name) to emit span_type=tool steps
    with input kwargs (e.g. input.sql). Without this, nested SQL handlers are
    treated as generic calls and tool-scoped controls never fire.
    """
    effective_tool_name = tool_name or step_name
    func.tool_name = effective_tool_name
    func.name = effective_tool_name
    return effective_tool_name


def make_controlled_tool(
    func: Callable,
    step_name: str,
    *,
    tool_name: Optional[str] = None,
) -> Callable:
    """Apply @control and return friendly JSON errors for tool guardrail blocks."""
    effective_tool_name = _mark_as_agent_control_tool(func, step_name, tool_name)
    controlled_fn = control(step_name=step_name)(func)
    controlled_fn.tool_name = effective_tool_name
    controlled_fn.name = effective_tool_name

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await controlled_fn(*args, **kwargs)
            except ControlViolationError as e:
                return _handle_control_error(e, step_name=step_name)
            except ControlSteerError as e:
                return _handle_control_error(e, step_name=step_name, steered=True)

        async_wrapper._agent_control_step = step_name  # type: ignore[attr-defined]
        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return controlled_fn(*args, **kwargs)
        except ControlViolationError as e:
            return _handle_control_error(e, step_name=step_name)
        except ControlSteerError as e:
            return _handle_control_error(e, step_name=step_name, steered=True)

    sync_wrapper._agent_control_step = step_name  # type: ignore[attr-defined]
    return sync_wrapper


def uses_internal_sql_control(func_name: str) -> bool:
    """Tools that run SQL via an internal _execute_* handler already under @control."""
    return (
        (func_name.startswith("get_") and func_name.endswith("_info"))
        or (func_name.startswith("delete_") and func_name.endswith("_record"))
    )


def domain_controlled_tool(
    step_name: str = "tool_step",
    *,
    resolve_logger: Optional[Callable[..., Any]] = None,
    tool_name: Optional[str] = None,
):
    """
    Decorator for domain logic.py tools.

    Applies @control, catches Agent Control errors, and returns a friendly JSON response.
    Tool spans and control spans are recorded via LangChain callbacks + enable_agent_control().
    """

    def decorator(func: Callable) -> Callable:
        return make_controlled_tool(func, step_name, tool_name=tool_name)

    return decorator


def wrap_controlled_tool(
    func: Callable,
    galileo_logger,
    step_name: Optional[str] = None,
) -> Callable:
    """Catch ControlViolationError and return a friendly tool response."""
    step = step_name or infer_control_step_name(func.__name__)

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ControlViolationError as e:
                notify_control_block(e, step_name=step)
                return json.dumps(
                    {
                        "error": format_blocked_message(e, step),
                        "blocked_by_agent_control": True,
                    }
                )
            except ControlSteerError as e:
                notify_control_block(e, step_name=step, guardrail_result="steered")
                return json.dumps(
                    {
                        "error": format_blocked_message(e, step, steered=True),
                        "steered_by_agent_control": True,
                    }
                )

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ControlViolationError as e:
            notify_control_block(e, step_name=step)
            return json.dumps(
                {
                    "error": format_blocked_message(e, step),
                    "blocked_by_agent_control": True,
                }
            )
        except ControlSteerError as e:
            notify_control_block(e, step_name=step, guardrail_result="steered")
            return json.dumps(
                {
                    "error": format_blocked_message(e, step, steered=True),
                    "steered_by_agent_control": True,
                }
            )

    return sync_wrapper


def wrap_controlled_langchain_tool(tool, galileo_logger, step_name: str = "retrieval_step"):
    """Wrap a LangChain BaseTool coroutine/func with Agent Control error handling."""
    from langchain_core.tools import BaseTool

    if not isinstance(tool, BaseTool):
        return tool

    original = tool.coroutine or tool.func
    if original is None:
        return tool

    is_async = inspect.iscoroutinefunction(original)

    def _blocked_response(error, steered=False):
        notify_control_block(
            error,
            step_name=step_name,
            guardrail_result="steered" if steered else "blocked",
        )
        return format_blocked_message(error, step_name, steered=steered)

    if is_async:

        @functools.wraps(original)
        async def async_wrapper(*args, **kwargs):
            try:
                return await original(*args, **kwargs)
            except ControlViolationError as e:
                return _blocked_response(e)
            except ControlSteerError as e:
                return _blocked_response(e, steered=True)

        return type(tool)(
            name=tool.name,
            description=tool.description,
            coroutine=async_wrapper,
            args_schema=tool.args_schema,
        )

    @functools.wraps(original)
    def sync_wrapper(*args, **kwargs):
        try:
            return original(*args, **kwargs)
        except ControlViolationError as e:
            return _blocked_response(e)
        except ControlSteerError as e:
            return _blocked_response(e, steered=True)

    return type(tool)(
        name=tool.name,
        description=tool.description,
        func=sync_wrapper,
        args_schema=tool.args_schema,
    )


def init_agent_control(
    galileo_logger,
    project_name: str,
    log_stream: str,
    agent_description: str = "Multi-domain demo agent",
    *,
    steps: Optional[list] = None,
    force: bool = False,
) -> bool:
    """Initialize or refresh Agent Control for the current Galileo logger/session."""
    global _initialized

    if galileo_logger is None:
        print("⚠️ Agent Control not initialized (no Galileo logger)")
        return False

    server_url = os.environ.get("AGENT_CONTROL_URL")
    agent_name = os.environ.get("AGENT_CONTROL_AGENT_NAME")
    api_key = os.environ.get("GALILEO_API_KEY")
    api_key_header = os.environ.get("AGENT_CONTROL_API_KEY_HEADER", "Galileo-API-Key")

    if not all([server_url, agent_name, api_key]):
        print(
            "⚠️ Agent Control not configured "
            "(set AGENT_CONTROL_URL, AGENT_CONTROL_AGENT_NAME, and GALILEO_API_KEY)"
        )
        return False

    session_key = (agent_name, project_name, log_stream, server_url)
    if not force and getattr(init_agent_control, "_last_session_key", None) == session_key:
        return True

    # Control spans require galileo_logger.enable_agent_control() (done in app.py).

    try:
        log_stream_data = get_log_stream(name=log_stream, project_name=project_name)
    except Exception as e:
        print(f"⚠️ Agent Control: failed to resolve log stream '{log_stream}': {e}")
        return False

    control_steps = steps or STANDARD_AGENT_CONTROL_STEPS

    agent_control.init(
        agent_name=agent_name,
        agent_description=agent_description,
        server_url=server_url,
        api_key=api_key,
        api_key_header=api_key_header,
        observability_enabled=True,
        observability_sink_name="registered",
        target_type="log_stream",
        target_id=log_stream_data.id,
        steps=control_steps,
    )
    _initialized = True
    init_agent_control._last_session_key = session_key
    step_names = ", ".join(s["name"] for s in control_steps)
    print(
        f"✅ Agent Control initialized for agent '{agent_name}' "
        f"(project={project_name}, log_stream={log_stream}, steps={step_names})"
    )
    return True
