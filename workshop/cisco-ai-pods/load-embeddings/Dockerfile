# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY requirements.txt /app/

# Install dependencies separately
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Expose the application on port 8080
EXPOSE 8080

ENTRYPOINT ["python", "app.py"]