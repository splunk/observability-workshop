# Travel Agent Demo Application

## Prerequisites

To run the application locally, ensure an instance of the Splunk distribution of the OpenTelemetry 
collector is running and configured to report data to Splunk Observability Cloud and Splunk core. 

## Run the Proxy

This application uses a proxy service to proxy requests to Cisco's Circuit API 
using an OpenAI API compatible format. 

To test the proxy locally, we need to first configure the following environment variables: 

``` bash
export CISCO_CLIENT_ID=your_cisco_client_id
export CISCO_CLIENT_SECRET=your_cisco_client_secret
export CISCO_APP_KEY=your_cisco_app_key
```

Then run the proxy service as follows: 

``` bash
cd proxy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn service:app --host 0.0.0.0 --port 8000
```

Test the proxy service using curl: 

``` bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      { "role": "user", "content": "Hello, can you hear me?" }
    ]
  }'
````

## Run the Travel Agent with Proxy 

Ensure the proxy is running by following the steps above. 

Then, in a separate command terminal, configure the following environment variables: 

``` bash
export OPENAI_API_KEY=dummy
export OPENAI_MODEL=gpt-4o-mini
export OPENAI_BASE_URL=http://localhost:8000/v1
export OTEL_SERVICE_NAME=travel-planner
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=travel-planner-demo
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
export HOME="/tmp"
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE="DELTA"
export OTEL_LOGS_EXPORTER="otlp"
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"
export OTEL_PYTHON_EXCLUDED_URLS="^(https?://)?[^/]+(/health)?$"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="true"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE="SPAN_AND_EVENT"
export OTEL_INSTRUMENTATION_GENAI_EVALS_RESULTS_AGGREGATION="true"
export OTEL_INSTRUMENTATION_GENAI_EMITTERS="span_metric_event,splunk"
export OTEL_INSTRUMENTATION_GENAI_EMITTERS_EVALUATION="replace-category:SplunkEvaluationResults"
export OTEL_GENAI_EVAL_DEBUG_SKIPS="true"
export OTEL_GENAI_EVAL_DEBUG_EACH="false"
export OTEL_INSTRUMENTATION_GENAI_DEBUG="false"
export SPLUNK_PROFILER_ENABLED="true"
export DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE="300"
export DEEPEVAL_RETRY_MAX_ATTEMPTS="2"
export DEEPEVAL_FILE_SYSTEM="READ_ONLY"
```

Then run the travel agent as follows:

``` bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Test the proxy service using curl:

``` bash
curl http://localhost:8080/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
````