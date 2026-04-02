---
title: Instrument the Agentic AI Application
linkTitle: 6. Instrument the Agentic AI Application
weight: 6
time: 20 minutes
---

There are a few steps required to instrument our Agentic AI application 
with OpenTelemetry and deploy it to Kubernetes: 

1. Add the instrumentation packages to the `requirements.txt` file 
2. Update the Dockerfile that invokes the application using `opentelemetry-instrument`
3. Build a new Docker image with the instrumentation packages 
4. Update the Kubernetes manifest with environment variables 
5. Deploy the Kubernetes manifest

## Add Instrumentation Packages

Next, we need to install several instrumentation packages. We can achieve this by 
opening the `~/workshop/agentic-ai/base-app/requirements.txt` for editing and adding 
the following packages: 

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
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
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

### Update the Kubernetes Manifest 

OpenTelemetry instrumentation, and AI Agent Monitoring in particular, require a number of environment 
variables to be set that define how instrumentation data is collected, processed, and 
exported. 

Before updating the Kubernetes manifest file, let's create a config map that uses the 
`INSTANCE` environment variable on our EC2 instance to populate the `OTEL_RESOURCE_ATTRIBUTES` 
environment variable in the Kubernetes manifest: 

```bash
kubectl create configmap instance-config --from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE -n travel-agent
```

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing and 
add the following environment variables: 

```yaml
            # Service Name
            - name: OTEL_SERVICE_NAME
              value: "travel-planner"
            # Additional OTEL configuration
            - name: OTEL_RESOURCE_ATTRIBUTES
              valueFrom:
                configMapKeyRef:
                  name: instance-config
                  key: OTEL_RESOURCE_ATTRIBUTES
            - name: SPLUNK_OTEL_AGENT
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):4317"
            - name: OTEL_EXPORTER_OTLP_PROTOCOL
              value: "grpc"
            - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
              value: "DELTA"
            - name: OTEL_PYTHON_EXCLUDED_URLS
              value: "^(https?://)?[^/]+(/health)?$"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
              value: "SPAN"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
              value: "span_metric,splunk"
            - name: SPLUNK_PROFILER_ENABLED
              value: "true"

```

In the same file, update the image to ensure we're using the one with the 
instrumentation: 

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

### Deploy the Updated Application 

We can deploy the updated application using the manifest file as follows:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

Ensure the new application pod has started successfully and the old pod is no longer present.

Then, run the following command to test the application:

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```