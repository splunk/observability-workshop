---
title: Instrument the LLM Application
linkTitle: 9. Instrument the LLM Application
weight: 9
time: 10 minutes
---

## Instrument the Application with OpenTelemetry

### Instrumentation Packages

To capture metrics, traces, and logs from our application, we've instrumented it with OpenTelemetry.
This required adding the following package to the `requirements.txt` file (which ultimately gets
installed with `pip install`):

````
splunk-opentelemetry==2.8.0
````

We also added the following to the `Dockerfile` used to build the
container image for this application, to install additional OpenTelemetry
instrumentation packages:

``` dockerfile
# Add additional OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap --action=install
```

Then we modified the `ENTRYPOINT` in the `Dockerfile` to call `opentelemetry-instrument`
when running the application:

``` dockerfile
ENTRYPOINT ["opentelemetry-instrument", "flask", "run", "-p", "8080", "--host", "0.0.0.0"]
```

Finally, to enhance the traces and metrics collected with OpenTelemetry from this
LangChain application, we added additional Splunk instrumentation packages:

````
splunk-otel-instrumentation-langchain==0.1.4
splunk-otel-util-genai==0.1.4
````

### Environment Variables 

To instrument the application with OpenTelemetry, we also included several 
environment variables in the Kubernetes manifest file used to deploy the application:

``` yaml
  env:
    - name: OTEL_SERVICE_NAME
      value: "llm-app"
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: "http://splunk-otel-collector-agent:4317"
    - name: OTEL_EXPORTER_OTLP_PROTOCOL
      value: "grpc"
      # filter out health check requests to the root URL
    - name: OTEL_PYTHON_EXCLUDED_URLS
      value: "^(https?://)?[^/]+(/)?$"
    - name: OTEL_PYTHON_DISABLED_INSTRUMENTATIONS
      value: "httpx,requests"
    - name: OTEL_INSTRUMENTATION_LANGCHAIN_CAPTURE_MESSAGE_CONTENT
      value: "true"
    - name: OTEL_LOGS_EXPORTER
      value: "otlp"
    - name: OTEL_PYTHON_LOG_CORRELATION
      value: "true"
    - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
      value: "delta"
    - name: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED
      value: "true"
    - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
      value: "true"
    - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
      value: "SPAN_AND_EVENT"
    - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
      value: "span_metric_event,splunk"
    - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS_EVALUATION
      value: "replace-category:SplunkEvaluationResults"
    - name: SPLUNK_PROFILER_ENABLED
      value: "true"
```

Note that the `OTEL_INSTRUMENTATION_LANGCHAIN_CAPTURE_MESSAGE_CONTENT` and 
`OTEL_INSTRUMENTATION_GENAI_*` environment variables are specific to the 
LangChain instrumentation we've used. 