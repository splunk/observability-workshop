FROM python:3.11-slim

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user (optional but recommended).
RUN addgroup --system app && adduser --system --group app

# Set work directory.
WORKDIR /app

# Install system dependencies (if needed).
# Uncomment and adjust if your dependencies require OS packages.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#  && rm -rf /var/lib/apt/lists/*

# Copy dependency definitions.
COPY requirements.txt /app/

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code.
COPY . /app

# Ensure files are owned by the non-root user.
RUN chown -R app:app /app

# Switch to non-root user.
USER app

# Expose the port FastAPI/uvicorn will run on.
EXPOSE 8000

# Start the FastAPI app with uvicorn.
# If your main file or app object is named differently, adjust "service:app".
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]