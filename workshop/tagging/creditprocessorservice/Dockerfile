FROM python:3.11-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install gcc -y

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main app
COPY main.py .

# Bootstrap OTel
RUN splunk-py-trace-bootstrap

# Set the entrypoint command to run the application
CMD ["./start.sh"]
