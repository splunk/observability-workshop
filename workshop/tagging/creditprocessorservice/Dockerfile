FROM python:3.11-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install --yes gcc python3-dev

ENV PIP_ROOT_USER_ACTION=ignore

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main app
COPY main.py .

# Bootstrap OTel
RUN splunk-py-trace-bootstrap

# Set the entrypoint command to run the application
CMD ["splunk-py-trace", "python3", "main.py"]
