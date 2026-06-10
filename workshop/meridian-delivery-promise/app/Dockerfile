FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OTEL_METRICS_EXPORTER=none \
    OTEL_LOGS_EXPORTER=none \
    OTEL_PROPAGATORS=tracecontext,baggage

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    opentelemetry-bootstrap -a install

COPY meridian_service.py .

CMD ["opentelemetry-instrument", "python", "meridian_service.py"]
