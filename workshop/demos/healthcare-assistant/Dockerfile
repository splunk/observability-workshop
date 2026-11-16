# Multi-stage build for Healthcare Assistant
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

RUN pip install uv

# Copy requirements and install dependencies
COPY ./requirements.txt /app/
RUN uv pip install --system --no-cache -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and data
COPY ./ /app/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

# Front-end (Streamlit) listens on 8501; back-end (uvicorn) on 8000.
# One image, two roles: the back-end Deployment overrides `command` to run
# `uvicorn server:app` (see orchestrator.py); the default below is the front-end.
EXPOSE 8501
EXPOSE 8000

CMD ["streamlit", "run", "app.py"]
