"""Workshop helpers for Splunk AO OTLP export troubleshooting."""
from __future__ import annotations

import json
import logging

_logger = logging.getLogger("splunk_ao.workshop")


def enable_otlp_rejection_detail_logging() -> None:
    """Log partialSuccess.errorMessage omitted by splunk_ao.exporter.diagnostics."""
    import splunk_ao.exporter.diagnostics as diagnostics

    if getattr(diagnostics, "_workshop_rejection_patch", False):
        return

    original_json = diagnostics._classify_json_acknowledgement
    original_protobuf = diagnostics._classify_protobuf_acknowledgement

    def _log_json_error_message(body: bytes) -> None:
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return
        if not isinstance(payload, dict):
            return
        partial_success = payload.get("partialSuccess")
        if not isinstance(partial_success, dict):
            return
        error_message = partial_success.get("errorMessage")
        if error_message:
            _logger.error("OTLP partialSuccess.errorMessage: %s", error_message)

    def _log_protobuf_error_message(response) -> None:
        partial_success = response.partial_success
        if partial_success.rejected_spans > 0 and partial_success.error_message:
            _logger.error("OTLP partialSuccess.errorMessage: %s", partial_success.error_message)

    def patched_json(body: bytes, status_code: int):
        _log_json_error_message(body)
        return original_json(body, status_code)

    def patched_protobuf(body: bytes, status_code: int):
        from google.protobuf.message import DecodeError
        from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
            ExportTraceServiceResponse,
        )

        response = ExportTraceServiceResponse()
        try:
            response.ParseFromString(body)
            _log_protobuf_error_message(response)
        except DecodeError:
            pass
        return original_protobuf(body, status_code)

    diagnostics._classify_json_acknowledgement = patched_json
    diagnostics._classify_protobuf_acknowledgement = patched_protobuf
    diagnostics._workshop_rejection_patch = True


def log_export_health(logger, *, label: str) -> None:
    """Log export_health.last_failure after a flush attempt."""
    health = logger.export_health
    if health.last_failure is not None:
        _logger.error(
            "%s export_health: healthy=%s consecutive_failures=%s message=%s",
            label,
            health.healthy,
            health.consecutive_failures,
            health.last_failure.message,
        )
    elif health.healthy is True:
        _logger.info("%s export_health: healthy=True", label)
    else:
        _logger.debug("%s export_health: healthy=%s", label, health.healthy)
