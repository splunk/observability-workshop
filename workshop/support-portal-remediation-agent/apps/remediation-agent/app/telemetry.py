import json
import logging
import os
from pathlib import Path

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from splunk_otel import init_splunk_otel

try:
    from galileo import ExecutionStatus as GalileoExecutionStatus
    from galileo import Payload as GalileoPayload
    from galileo import Response as GalileoResponse
    from galileo import galileo_context
    from galileo import log as galileo_log
    from galileo.openai import openai as galileo_openai
    from galileo_core.schemas.protect.response import TraceMetadata as GalileoTraceMetadata
except ImportError:  # pragma: no cover - optional Galileo monitoring package
    GalileoExecutionStatus = None
    GalileoPayload = None
    GalileoResponse = None
    GalileoTraceMetadata = None
    galileo_context = None
    galileo_log = None
    galileo_openai = None

deployment_environment = os.getenv("DEPLOYMENT_ENVIRONMENT", "demo")
service_namespace = os.getenv("OTEL_SERVICE_NAMESPACE", "ibobs2002")
service_name = os.getenv("OTEL_SERVICE_NAME", "remediation-agent")
app_version = os.getenv("OTEL_SERVICE_VERSION", os.getenv("APP_VERSION", "0.1.0"))
galileo_project = os.getenv("GALILEO_PROJECT", "ciscolive26")
galileo_log_stream = os.getenv("GALILEO_LOG_STREAM", "remediation-agent")
_galileo_monitoring_started = False

_STANDARD_LOG_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


def log_directory() -> Path:
    return Path(os.getenv("IBOBS_LOG_DIR", Path(__file__).resolve().parents[3] / "var" / "log"))


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "severity_text": record.levelname,
            "message": record.getMessage(),
            "logger.name": record.name,
            "service.name": service_name,
            "service.namespace": service_namespace,
            "service.version": app_version,
            "app.version": app_version,
            "deployment.environment": deployment_environment,
        }

        trace_id = getattr(record, "otelTraceID", None)
        span_id = getattr(record, "otelSpanID", None)
        trace_sampled = getattr(record, "otelTraceSampled", None)
        if trace_id:
            payload["trace_id"] = trace_id
        if span_id:
            payload["span_id"] = span_id
        if trace_sampled is not None:
            payload["trace_sampled"] = trace_sampled

        for key, value in record.__dict__.items():
            if key in _STANDARD_LOG_FIELDS or key.startswith("_") or key.startswith("otel"):
                continue
            payload[key] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_agent_logger() -> logging.Logger:
    directory = log_directory()
    directory.mkdir(parents=True, exist_ok=True)

    formatter = JsonFormatter()
    logger = logging.getLogger(service_name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(directory / f"{service_name}.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


agent_logger = configure_agent_logger()


def telemetry_enabled() -> bool:
    return bool(
        os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        or (os.getenv("SPLUNK_ACCESS_TOKEN") and os.getenv("SPLUNK_REALM"))
    )


def init_agent_telemetry(app) -> bool:
    if not telemetry_enabled():
        return False

    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = merge_resource_attributes(
        os.getenv("OTEL_RESOURCE_ATTRIBUTES"),
        build_resource_attributes(),
    )
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    os.environ.setdefault(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        otlp_endpoint or f"https://ingest.{os.getenv('SPLUNK_REALM')}.signalfx.com",
    )
    os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
    if (not otlp_endpoint or "signalfx.com" in otlp_endpoint) and os.getenv("SPLUNK_ACCESS_TOKEN"):
        os.environ.setdefault("OTEL_EXPORTER_OTLP_HEADERS", f"x-sf-token={os.getenv('SPLUNK_ACCESS_TOKEN')}")
    os.environ.setdefault("OTEL_PROPAGATORS", "tracecontext,baggage,b3")

    init_splunk_otel()
    FastAPIInstrumentor.instrument_app(app)
    HTTPXClientInstrumentor().instrument()
    agent_logger.info("agent telemetry initialized", extra={"telemetry_enabled": True})
    return True


def read_secret_file(path: str) -> str:
    key_path = Path(path).expanduser()
    if key_path.is_absolute() or key_path.exists():
        return key_path.read_text(encoding="utf-8").strip()

    repo_relative_path = Path(__file__).resolve().parents[3] / key_path
    return repo_relative_path.read_text(encoding="utf-8").strip()


def load_galileo_api_key() -> bool:
    if os.getenv("GALILEO_API_KEY"):
        return True

    api_key_file = os.getenv("GALILEO_API_KEY_FILE")
    if not api_key_file:
        return False

    try:
        api_key = read_secret_file(api_key_file)
    except OSError as error:
        agent_logger.warning(
            "galileo api key file could not be read",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "galileo_api_key_file": api_key_file,
                "error": str(error),
            },
        )
        return False

    if not api_key:
        agent_logger.warning(
            "galileo api key file is empty",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "galileo_api_key_file": api_key_file,
            },
        )
        return False

    os.environ["GALILEO_API_KEY"] = api_key
    return True


def galileo_monitoring_enabled() -> bool:
    return bool(os.getenv("GALILEO_API_KEY") or os.getenv("GALILEO_API_KEY_FILE"))


def init_galileo_monitoring() -> bool:
    global _galileo_monitoring_started

    if not galileo_monitoring_enabled():
        _galileo_monitoring_started = False
        return False

    if not load_galileo_api_key():
        _galileo_monitoring_started = False
        return False

    if galileo_context is None or galileo_log is None or galileo_openai is None:
        agent_logger.warning(
            "galileo monitoring requested but Galileo SDK is unavailable",
            extra={"agent_monitoring_enabled": False, "agent_monitoring_provider": "galileo"},
        )
        _galileo_monitoring_started = False
        return False

    os.environ.setdefault("GALILEO_PROJECT", galileo_project)
    os.environ.setdefault("GALILEO_LOG_STREAM", galileo_log_stream)
    os.environ.setdefault("GALILEO_API_BASE", "https://api.galileo.ai")
    os.environ.setdefault("GALILEO_API_URL", os.getenv("GALILEO_API_BASE", "https://api.galileo.ai"))

    try:
        galileo_context.init(
            project=os.getenv("GALILEO_PROJECT", galileo_project),
            log_stream=os.getenv("GALILEO_LOG_STREAM", galileo_log_stream),
        )
    except Exception as error:
        agent_logger.warning(
            "galileo monitoring initialization failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(error),
            },
        )
        _galileo_monitoring_started = False
        return False

    _galileo_monitoring_started = True
    agent_logger.info(
        "galileo monitoring initialized",
        extra={
            "agent_monitoring_enabled": True,
            "agent_monitoring_provider": "galileo",
            "galileo_project": os.getenv("GALILEO_PROJECT"),
            "galileo_log_stream": os.getenv("GALILEO_LOG_STREAM"),
        },
    )
    return True


def galileo_openai_module():
    if _galileo_monitoring_started and galileo_openai is not None:
        return galileo_openai
    return None


def start_galileo_session(name: str, external_id: str, metadata: dict[str, str] | None = None) -> str | None:
    if not _galileo_monitoring_started or galileo_context is None:
        return None

    try:
        return galileo_context.start_session(name=name, external_id=external_id, metadata=metadata)
    except Exception as error:
        agent_logger.warning(
            "galileo session start failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(error),
            },
        )
        return None


def clear_galileo_session() -> None:
    if not _galileo_monitoring_started or galileo_context is None:
        return

    try:
        galileo_context.clear_session()
    except Exception as error:
        agent_logger.warning(
            "galileo session clear failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(error),
            },
        )


def add_galileo_protect_span(
    input_text: str,
    output_text: str,
    triggered: bool,
    metadata: dict[str, str] | None = None,
) -> bool:
    if (
        not _galileo_monitoring_started
        or galileo_context is None
        or GalileoPayload is None
        or GalileoResponse is None
        or GalileoExecutionStatus is None
        or GalileoTraceMetadata is None
    ):
        return False

    try:
        status = GalileoExecutionStatus.triggered if triggered else GalileoExecutionStatus.not_triggered
        response = GalileoResponse(
            text=output_text,
            trace_metadata=GalileoTraceMetadata(),
            status=status,
            rulesets=["unsafe_action_policy"] if triggered else ["bounded_remediation_policy"],
            action="block_and_require_human_review" if triggered else "allow",
        )
        galileo_context.get_logger_instance().add_protect_span(
            payload=GalileoPayload(input=input_text, output=output_text),
            response=response,
            metadata=metadata,
            status_code=200,
        )
        return True
    except Exception as error:
        agent_logger.warning(
            "galileo protect span failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(error),
            },
        )
        return False


def flush_galileo_monitoring() -> bool:
    if not _galileo_monitoring_started or galileo_context is None:
        return False

    flush_errors: list[Exception] = []

    def record_flush_error(error: Exception) -> None:
        flush_errors.append(error)

    try:
        galileo_context.flush(on_error=record_flush_error)
    except Exception as error:
        agent_logger.warning(
            "galileo monitoring flush failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(error),
            },
        )
        return False

    if flush_errors:
        agent_logger.warning(
            "galileo monitoring flush failed",
            extra={
                "agent_monitoring_enabled": False,
                "agent_monitoring_provider": "galileo",
                "error": str(flush_errors[-1]),
            },
        )
        return False

    agent_logger.info(
        "galileo monitoring flushed",
        extra={
            "agent_monitoring_enabled": True,
            "agent_monitoring_provider": "galileo",
            "galileo_project": os.getenv("GALILEO_PROJECT"),
            "galileo_log_stream": os.getenv("GALILEO_LOG_STREAM"),
        },
    )
    return True


def galileo_span(span_type: str, name: str):
    def decorator(func):
        if not _galileo_monitoring_started or galileo_log is None:
            return func
        return galileo_log(span_type=span_type, name=name)(func)

    return decorator


def build_resource_attributes() -> str:
    return ",".join(
        [
            f"service.namespace={service_namespace}",
            f"deployment.environment={deployment_environment}",
            f"service.version={app_version}",
            f"app.version={app_version}",
        ]
    )


def merge_resource_attributes(existing: str | None, required: str) -> str:
    attributes: dict[str, str] = {}
    order: list[str] = []

    for group in (existing, required):
        if not group:
            continue
        for item in group.split(","):
            key, separator, value = item.partition("=")
            key = key.strip()
            if not key or not separator:
                continue
            if key not in attributes:
                order.append(key)
            attributes[key] = value.strip()

    return ",".join(f"{key}={attributes[key]}" for key in order)


def annotate_current_span(attributes: dict[str, str]) -> None:
    span = trace.get_current_span()
    if not span:
        return

    for key, value in attributes.items():
        span.set_attribute(key, value)
