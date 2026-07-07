# Multi-stage build for Healthcare Assistant
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

RUN pip install uv

# Copy requirements and install dependencies
COPY 1-base-app/requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r requirements.txt

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
COPY 1-base-app/ /app/
COPY docs/ /app/docs/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

# Expose port for Streamlit
EXPOSE 8501

# Run the server
CMD ["streamlit", "run", "app.py"]
