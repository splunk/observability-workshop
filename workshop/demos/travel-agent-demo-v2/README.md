# Travel Agent Demo Application

## Run the Application Locally

### Deploy the OpenTelemetry Collector

To run the application locally, ensure an instance of the Splunk distribution of the OpenTelemetry 
collector is running and configured to report data to Splunk Observability Cloud and Splunk core. 

### Run the Application with Azure OpenAI

You can run the application using an OpenAI model hosted in Azure directly. 
This example uses the `gpt-4.1-mini` model running in Azure OpenAI. 

In the command terminal, configure the following environment variables:

``` bash
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
export AZURE_OPENAI_ENDPOINT=your_AI_defense_gateway_URL
export AZURE_OPENAI_API_VERSION=2025-01-01-preview
export AZURE_OPENAI_API_KEY=your_azure_openai_api_key
export OPENAI_MODEL=gpt-4.1-mini
# export TEMPERATURE=1 # gpt-5 models don't support temperature=0.0. Only temperature=1 is supported.
export OTEL_SERVICE_NAME=travel-planner
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=travel-planner-demo
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE="DELTA"
export OTEL_PYTHON_EXCLUDED_URLS="^(https?://)?[^/]+(/health)?$"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="true"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE="SPAN"
export OTEL_INSTRUMENTATION_GENAI_EVALS_RESULTS_AGGREGATION="true"
export OTEL_INSTRUMENTATION_GENAI_EMITTERS="span_metric,splunk"
export SPLUNK_PROFILER_ENABLED="true"
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
```

Send a request including poison config that forces a PCI violation: 

``` bash
  curl http://localhost:8080/travel/plan \
    -H "Content-Type: application/json" \
    -d '{
      "origin": "New York",
      "destination": "London",
      "user_request": "We are planning a week-long trip to New York from London. Looking for boutique hotel, business-class flights and unique experiences.",
      "travelers": 2,
      "poison_config": {
          "prob": "1.0",
          "types": ["pci_violation"],
          "max": "1",
          "seed": "9999"
      }
    }'
```

## Build Docker Images

The following commands were used to build Docker images for each of the application components. 

### Travel Agent App

To build the travel agent application image:

``` bash
cd app-with-ai-defense
docker build --platform linux/amd64 -t docker.io/derekmitchell399/travel-planner-demo-v2:1.0 .
docker push docker.io/derekmitchell399/travel-planner-demo-v2:1.0
```

### Load Generator

To build the travel agent load generator image:

``` bash
cd loadgen
docker build --platform linux/amd64 -t docker.io/derekmitchell399/travel-planner-loadgen-v2:1.0 .
docker push docker.io/derekmitchell399/travel-planner-loadgen-v2:1.0
```
