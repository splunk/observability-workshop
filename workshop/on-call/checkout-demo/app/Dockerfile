FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OTEL_PROPAGATORS=tracecontext,baggage

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    opentelemetry-bootstrap -a install

COPY checkout_service.py inventory_service.py loadgen.py ./

CMD ["opentelemetry-instrument", "uvicorn", "checkout_service:app", "--host", "0.0.0.0", "--port", "8080"]
