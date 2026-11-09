"""Shared logging setup: timestamped lines on stdout for `kubectl logs`."""
import logging
import sys

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def get_logger(name: str) -> logging.Logger:
    """Return a logger with its own timestamped stdout handler (idempotent).

    Streamlit never configures logging for us, and uvicorn only configures its
    own loggers, so attach a handler explicitly rather than relying on root.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def timestamp_uvicorn_logs() -> None:
    """Add timestamps to uvicorn's own loggers and drop probe noise.

    uvicorn's default formatters have no time, and kubelet's /ready + /healthz
    probes every few seconds otherwise drown out real requests.
    """
    fmt = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        for h in logging.getLogger(name).handlers:
            h.setFormatter(fmt)

    class _DropProbes(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            msg = record.getMessage()
            return not ("GET /ready " in msg or "GET /healthz " in msg)

    logging.getLogger("uvicorn.access").addFilter(_DropProbes())
