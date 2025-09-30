# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY requirements.txt /app/

# Install dependencies separately
RUN pip install -r requirements.txt


# Add additional OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap --action=install

# Copy the application code
COPY . /app

# Expose the application on port 8080
EXPOSE 8080

ENTRYPOINT ["opentelemetry-instrument", "flask", "run", "-p", "8080", "--host", "0.0.0.0"]