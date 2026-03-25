---
title: Instrument the Agentic AI Application
linkTitle: 6. Instrument the Agentic AI Application
weight: 6
time: 20 minutes
---

There are a few steps required to instrument our Agentic AI application 
with OpenTelemetry and deploy it to Kubernetes: 

1. Configure the LangChain/LangGraph application for AI agent monitoring
2. Add the instrumentation packages to the `requirements.txt` file 
3. Update the Dockerfile that invokes the application using `opentelemetry-instrument`
4. Build a new Docker image with the instrumentation packages 
5. Update the Kubernetes manifest with environment variables 
6. Deploy the Kubernetes manifest

## Configure the Application for AI Agent Monitoring 

[Configure zero-code instrumentation for Python AI applications](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation#ariaid-title1)
explains how to configure zero-code instrumentation for Python AI applications that utilize 
various frameworks. 

The first thing we'll need to do is configure our application for AI Agent Monitoring. 

Currently, our application creates an LLM and invokes it as follows: 

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    ...
    result = llm.invoke(messages)
    ...
```

For AI Agent Monitoring, we need to instead create an agent that includes metadata 
with the agent name, and then invoke the agent rather than the LLM: 

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    
    ### NEW CODE
    agent = _create_react_agent(llm, tools=[]).with_config(
        {
            "run_name": "flight_specialist",
            "tags": ["agent", "agent:flight_specialist"],
            "metadata": {
                "agent_name": "flight_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    ### NEW CODE 
    ...
    result = agent.invoke(messages)
    ...
```

Repeat the above changes for the `coordinator`, `hotel_specialist`, `activity_specialist`, 
and `plan_synthesizer` nodes. 

We also need to add the following import near the top of the `main.py` file: 

```python
from langchain.agents import (
create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
```

## Add Instrumentation Packages

Next, we need to install several instrumentation packages. We can achieve this by 
opening the `~/workshop/agentic-ai/base-app/requirements.txt` for editing and adding 
the following packages: 

````
deepeval
litellm==1.82.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
splunk-otel-util-genai-evals==0.1.8
splunk-otel-genai-evals-deepeval==0.1.13
````

## Update the Dockerfile 

Then, we need to update the Dockerfile to ensure the container image is started 
with `opentelemetry-instrument`. Open the `~/workshop/agentic-ai/base-app/Dockerfile` 
file for editing and update the last line as follows: 

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

### Build an Updated Docker Image

Build an updated Docker image with a new tag: 

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation.
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

### Update the Kubernetes Manifest 

OpenTelemetry instrumentation, and AI Agent Monitoring in particular, require a number of environment 
variables to be set that define how instrumentation data is collected, processed, and 
exported. 

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing and 
add the following environment variables: 

```yaml
            - name: DEEPEVAL_LLM_BASE_URL
              valueFrom:
                secretKeyRef:
                  name: deepeval-secret
                  key: deepeval-llm-base-url
            - name: DEEPEVAL_LLM_MODEL
              value: "gpt-4.1-mini"
            - name: DEEPEVAL_LLM_PROVIDER
              value: "azure"
            - name: DEEPEVAL_LLM_API_KEY
              valueFrom:
                secretKeyRef:
                  name: azure-openai-api
                  key: azure-openai-api-key
            - name: DEEPEVAL_LLM_EXTRA_HEADERS
              value: '{"api_version":"2024-01-01-preview"}'
            # Service Name
            - name: OTEL_SERVICE_NAME
              value: "travel-planner"
            # Additional OTEL configuration
            - name: OTEL_RESOURCE_ATTRIBUTES
              value: "deployment.environment=travel-planner-demo"
            - name: SPLUNK_OTEL_AGENT
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):4317"
            - name: OTEL_EXPORTER_OTLP_PROTOCOL
              value: "grpc"
            - name: HOME
              value: "/tmp"
            - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
              value: "DELTA"
            - name: OTEL_LOGS_EXPORTER
              value: "otlp"
            - name: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED
              value: "true"
            - name: OTEL_PYTHON_EXCLUDED_URLS
              value: "^(https?://)?[^/]+(/health)?$"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
              value: "SPAN_AND_EVENT"
            - name: OTEL_INSTRUMENTATION_GENAI_EVALS_RESULTS_AGGREGATION
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
              value: "span_metric_event,splunk"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS_EVALUATION
              value: "replace-category:SplunkEvaluationResults"
            - name: OTEL_GENAI_EVAL_DEBUG_SKIPS
              value: "true"
            - name: OTEL_GENAI_EVAL_DEBUG_EACH
              value: "false"
            - name: OTEL_INSTRUMENTATION_GENAI_DEBUG
              value: "false"
            - name: SPLUNK_PROFILER_ENABLED
              value: "true"
            - name: DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE
              value: "300"
            - name: DEEPEVAL_RETRY_MAX_ATTEMPTS
              value: "2"
            - name: DEEPEVAL_FILE_SYSTEM
              value: "READ_ONLY"
```

In the same file, update the image to ensure we're using the one with the 
instrumentation: 

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

### Deploy the Updated Application 

We can deploy the updated application using the manifest file as follows:

``` bash
kubectl deploy -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

Run the following command to test the application:

``` bash
curl http://travel-planner:8080/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```