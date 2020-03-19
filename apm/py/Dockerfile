FROM python:3.7-slim

WORKDIR /app
COPY /app/requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt
RUN sfx-py-trace-bootstrap
COPY /app .

EXPOSE 5000
ENV SIGNALFX_SERVICE_NAME=AS-py-echo
CMD ["sfx-py-trace", "/app/main.py"]
