"""
Agent Control helper functions for runtime guardrails.
"""
import functools
import inspect
import json
import logging
import os
import sys
from typing import Any, Callable, Optional

import agent_control
from agent_control import ControlSteerError, ControlViolationError, control

logger = logging.getLogger(__name__)


def _ensure_logger_visible() -> None:
    """Attach a stdout handler so these logs show up in ``kubectl logs``.

    splunk_ao's ``enable_console_logging()`` only wires the ``splunk_ao`` logger
    (with propagate disabled), and the app never configures the root logger, so
    without this our records would be dropped. Runs once and stays out of the way
    if logging has already been configured for this module.
    """
    if logger.handlers or logger.level != logging.NOTSET:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # our own handler; avoid duplicates if root is later configured


_ensure_logger_visible()

_initialized = False
_env_logged = False
_http_logging_installed = False

# Header/env values that must be masked in logs (credentials / tokens). Header
# *names* ending in _HEADER are safe; only their values would be secret.
_SENSITIVE_HEADERS = frozenset({
    "x-sf-token", "authorization", "splunk-ao-api-key", "galileo-api-key",
    "x-api-key", "x-agent-control-runtime-token",
})
_SENSITIVE_ENV_SUBSTR = ("TOKEN", "API_KEY", "SECRET", "PASSWORD")


def _env_flag(name: str, default: bool = False) -> bool:
    """Parse a boolean-ish environment variable."""
    raw = (os.environ.get(name) or "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def _mask_secret(value: Optional[str]) -> str:
    """Mask a credential for logging while leaving it recognizable."""
    if not value:
        return "<empty>"
    if len(value) <= 8:
        return f"*** (len={len(value)})"
    return f"{value[:4]}…{value[-4:]} (len={len(value)})"


def _format_headers_for_log(headers, *, unmask: bool = False) -> str:
    rendered = []
    for name, value in headers.items():
        if not unmask and name.lower() in _SENSITIVE_HEADERS:
            value = _mask_secret(value)
        rendered.append(f"{name}: {value}")
    return " | ".join(rendered)


def _log_agent_control_env() -> None:
    """Log (once) the AGENT_CONTROL_*/SPLUNK_AO_* env vars the app sees, secrets masked."""
    global _env_logged
    if _env_logged:
        return
    _env_logged = True
    logger.info("Agent Control init — environment variables visible to the app:")
    for name in sorted(os.environ):
        if not name.startswith(("AGENT_CONTROL_", "SPLUNK_AO_")):
            continue
        value = os.environ[name]
        if not name.endswith("_HEADER") and any(s in name for s in _SENSITIVE_ENV_SUBSTR):
            value = _mask_secret(value)
        logger.info("    %s=%s", name, value)


def _install_agent_control_http_logging() -> None:
    """Log every Agent Control HTTP request/response (URL, headers, body) via httpx hooks.

    Patches ``httpx.AsyncClient`` once to attach event hooks. The hooks only act on
    agent-control URLs, so other httpx traffic (OpenAI, Splunk AO) is left alone.
    Credential headers are masked unless AGENT_CONTROL_DEBUG_HTTP_UNMASK is truthy.
    """
    global _http_logging_installed
    if _http_logging_installed:
        return
    try:
        import httpx
    except Exception as e:  # pragma: no cover - httpx is a hard dep of the SDK
        logger.warning("Agent Control HTTP logging unavailable (httpx import failed: %s)", e)
        return

    unmask = _env_flag("AGENT_CONTROL_DEBUG_UNMASK")

    async def _log_request(request) -> None:
        if "agent-control" not in str(request.url):
            return
        body = request.content.decode("utf-8", "replace") if request.content else ""
        logger.info(
            "→ Agent Control request: %s %s\n    headers: %s\n    body: %s",
            request.method, request.url,
            _format_headers_for_log(request.headers, unmask=unmask), body[:2000],
        )

    async def _log_response(response) -> None:
        if "agent-control" not in str(response.request.url):
            return
        await response.aread()
        logger.info(
            "← Agent Control response: HTTP %s %s\n    headers: %s\n    body: %s",
            response.status_code, response.request.url,
            _format_headers_for_log(response.headers, unmask=unmask), response.text[:2000],
        )

    original_init = httpx.AsyncClient.__init__

    @functools.wraps(original_init)
    def _patched_init(self, *args, **kwargs):
        hooks = dict(kwargs.get("event_hooks") or {})
        hooks["request"] = list(hooks.get("request", [])) + [_log_request]
        hooks["response"] = list(hooks.get("response", [])) + [_log_response]
        kwargs["event_hooks"] = hooks
        original_init(self, *args, **kwargs)

    httpx.AsyncClient.__init__ = _patched_init
    _http_logging_installed = True
    logger.info(
        "Agent Control HTTP logging enabled (httpx request/response hooks; "
        "credential headers %s)",
        "UNMASKED" if unmask else "masked (set AGENT_CONTROL_DEBUG_UNMASK=true to reveal)",
    )

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
    splunk_ao_logger,
    messages=None,
    *,
    trace_input: Optional[str] = None,
    trace_name: str = "Run Agent",
) -> None:
    """Start a trace when none is active (required before add_llm_span)."""
    if not splunk_ao_logger or splunk_ao_logger.current_parent() is not None:
        return
    if trace_input is None and messages is not None:
        trace_input = _extract_trace_input(messages)
    splunk_ao_logger.start_trace(input=trace_input or "", name=trace_name)


def finalize_trace(splunk_ao_logger, output: str) -> None:
    """Conclude and flush the active trace after a query completes."""
    if not splunk_ao_logger or splunk_ao_logger.current_parent() is None:
        return
    splunk_ao_logger.conclude(output=output)
    splunk_ao_logger.flush()


def notify_control_block(
    error: Exception,
    *,
    step_name: str,
    guardrail_result: str = "blocked",
) -> None:
    """Console notice for Agent Control blocks.

    LLM/tool spans come from LangChain callbacks (SplunkAOAsyncCallback).
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
    splunk_ao_logger,
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


def wrap_controlled_langchain_tool(tool, splunk_ao_logger, step_name: str = "retrieval_step"):
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
    splunk_ao_logger,
    project_name: str,
    agent_stream: str,
    agent_description: str = "Multi-domain demo agent",
    *,
    steps: Optional[list] = None,
    force: bool = False,
) -> bool:
    """Initialize Agent Control for the current Splunk AO logger/session.

    Configured per the Agent Control docs, identically for standalone and
    Observability Cloud:
    https://agent-observability-docs.splunk.com/how-to-guides/agent-control/initialize-and-configure-agent-control

    The deployment-specific server URL and API-key header come straight from the
    AGENT_CONTROL_* environment variables, and the control target is the agent
    stream ID the logger resolved when its session started (agent.py starts the
    session before calling this).
    """
    global _initialized

    if splunk_ao_logger is None:
        logger.warning("Agent Control not initialized (no Splunk AO logger)")
        return False

    server_url = os.environ.get("AGENT_CONTROL_URL")
    agent_name = os.environ.get("AGENT_CONTROL_AGENT_NAME", "default")
    api_key = os.environ.get("SPLUNK_AO_API_KEY") or os.environ.get("SPLUNK_AO_O11Y_TOKEN")
    api_key_header = os.environ.get("AGENT_CONTROL_API_KEY_HEADER", "Splunk-AO-API-Key")
    target_type = os.environ.get("AGENT_CONTROL_TARGET_TYPE", "agent_stream")
    observability_sink_name = os.environ.get("AGENT_CONTROL_OBSERVABILITY_SINK_NAME", "registered")
    target_id = getattr(splunk_ao_logger, "agent_stream_id", None)

    # Deep debugging (env dump + raw HTTP request/response logging) is opt-in and
    # off by default. Set AGENT_CONTROL_DEBUG=true to enable it when investigating.
    debug = _env_flag("AGENT_CONTROL_DEBUG")
    if debug:
        _log_agent_control_env()

    if not server_url or not api_key or not target_id:
        logger.warning(
            "Agent Control not configured (need AGENT_CONTROL_URL, a credential in "
            "SPLUNK_AO_API_KEY/SPLUNK_AO_O11Y_TOKEN, and a started session with a "
            "resolved agent_stream_id). server_url=%s api_key_set=%s target_id=%s",
            server_url, bool(api_key), target_id,
        )
        return False

    # Publish resolved IDs (matches the docs' os.environ pattern).
    os.environ["SPLUNK_AO_AGENT_STREAM_ID"] = str(target_id)
    if getattr(splunk_ao_logger, "project_id", None):
        os.environ["SPLUNK_AO_PROJECT_ID"] = str(splunk_ao_logger.project_id)

    session_key = (agent_name, project_name, agent_stream, server_url)
    if not force and getattr(init_agent_control, "_last_session_key", None) == session_key:
        logger.debug("Agent Control already initialized for this session; skipping re-init")
        return True

    # Control spans require splunk_ao_logger.enable_agent_control() (done in agent.py).
    control_steps = steps or STANDARD_AGENT_CONTROL_STEPS

    if debug:
        # Log the exact init parameters, then turn on wire logging so init()'s own
        # register/health calls (and later evaluation calls) are captured.
        logger.info(
            "Calling agent_control.init(): agent_name=%s server_url=%s api_key_header=%s "
            "api_key=%s target_type=%s target_id=%s observability_sink_name=%s steps=[%s]",
            agent_name, server_url, api_key_header, _mask_secret(api_key),
            target_type, target_id, observability_sink_name,
            ", ".join(s["name"] for s in control_steps),
        )
        _install_agent_control_http_logging()

    try:
        agent_control.init(
            agent_name=agent_name,
            agent_description=agent_description,
            server_url=server_url,
            api_key=api_key,
            api_key_header=api_key_header,
            observability_enabled=True,
            observability_sink_name=observability_sink_name,
            target_type=target_type,
            target_id=str(target_id),
            steps=control_steps,
        )
    except Exception as e:
        logger.warning("Agent Control init failed: %s", e, exc_info=True)
        return False

    _initialized = True
    init_agent_control._last_session_key = session_key
    step_names = ", ".join(s["name"] for s in control_steps)
    logger.info(
        "✅ Agent Control initialized for agent '%s' (project=%s agent_stream=%s "
        "server_url=%s api_key_header=%s target_type=%s target_id=%s steps=[%s])",
        agent_name, project_name, agent_stream, server_url, api_key_header,
        target_type, target_id, step_names,
    )
    return True
