---
title: Instrument the Agentic AI Application
linkTitle: 6. Instrument the Agentic AI Application
weight: 6
time: 15 minutes
---

> Note: this section of the workshop requires changes to multiple files. 
> If you're not sure where to make the changes, or your application is no 
> longer working, please refer to the expected solution for this section 
> which is in the `~/workshop/agentic-ai/app-with-instrumentation` folder.

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
the following packages to the bottom of the file: 

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

These packages can be described as follows: 

* `splunk-opentelemetry`: this is the Splunk distribution of OpenTelemetry Python, which instruments a Python application to capture and report distributed traces to Splunk APM. 
* `splunk-otel-instrumentation-langchain`: this package provides OpenTelemetry instrumentation for LangChain LLM/chat workflows.
* `splunk-otel-genai-emitters-splunk`: this package provides emitters for Splunk schema for Evaluation Results logs to optimize storage and filtering in Splunk Platform.
* `splunk-otel-util-genai`: this package includes utility functions to provide APIs and data types to ease instrumentation of Generative AI workloads using OpenTelemetry semantic conventions.
* `opentelemetry-instrumentation-flask`: this library builds on the OpenTelemetry WSGI middleware to track web requests in Flask applications.

> Hint: run the following command to compare your changes with the expected solution:
> 
> `diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-instrumentation/requirements.txt`

## Update the Dockerfile 

Then, we need to enable OpenTelemetry instrumentation. This is done by updating the Dockerfile to 
ensure the application is started with `opentelemetry-instrument`. Open the `~/workshop/agentic-ai/base-app/Dockerfile` 
file for editing and update the last line as follows: 

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

> Hint: run the following command to compare your changes with the expected solution:
> 
> `diff ~/workshop/agentic-ai/base-app/Dockerfile ~/workshop/agentic-ai/app-with-instrumentation/Dockerfile`

### Build an Updated Docker Image

Build an updated Docker image with a new tag: 

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

> Tip: if the image is taking too long to build, consider using the pre-built
> image instead. To do so, update the image name in
> the `~/workshop/agentic-ai/base-app/k8s.yaml` file to `ghcr.io/splunk/agentic-ai-app:app-with-instrumentation`
> instead of `localhost:9999/agentic-ai-app:app-with-instrumentation`.

### Define the Config Map

When we deploy our application to Kubernetes, we want telemetry (metrics, traces, and logs) 
to be sent to Splunk Observability Cloud with a clear and unique environment identifier. 
This makes it easier to filter, compare, and troubleshoot data across different deployments.

To do this, we’ll set the OpenTelemetry resource attribute named `deployment.environment`. Rather 
than hard-coding the value, we’ll derive it from the `INSTANCE` environment variable that 
already exists on our EC2 instance. This ensures each deployment is automatically tagged 
with the correct environment name.

We’ll store this configuration in a Kubernetes ConfigMap, which can later be injected into 
our application pods as an environment variable.

Create the ConfigMap with the following command:

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

What this does:

* Defines the `OTEL_RESOURCE_ATTRIBUTES` environment variable expected by OpenTelemetry.
* Sets `deployment.environment` to a value like `agentic-ai-shw-1c43`, depending on the value of `$INSTANCE`.
* Creates the ConfigMap in the `travel-agent` namespace.

We’ll reference this ConfigMap in the next step when we configure our Kubernetes deployment.

### Update the Kubernetes Manifest 

OpenTelemetry instrumentation, and AI Agent Monitoring in particular, require a number of environment 
variables to be set that define how instrumentation data is collected, processed, and 
exported.

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing. Update the **image 
tag** to ensure we're using the image with the instrumentation:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

In the same file, add the following **environment variables** between the comments that say 
`Begin: Add Environment Variables` and `End: Add Environment Variables`: 

> Hint: Type `:set paste` before pasting the contents, to prevent `vi` from auto-indenting the pasted code.

```yaml
            # Begin: Add Environment Variables
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
            # End: Add Environment Variables
```

> Note: some of the text may not be visible without scrolling. 
> Use the `Copy text to clipboard` button on the top right-hand corner to 
> ensure you've copied all of the text.

> Note: indentation is critical with yaml; ensure the new environment variables 
> align with the existing environment variables.

The following environment variables are specific to Agentic AI monitoring 
and can be described as follows: 

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: this determines if the OTLP metric exporter reports cumulative totals, deltas, or low-memory-friendly temporality for emitted metrics. Setting this to `DELTA` is recommended for Agentic AI monitoring. 
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: this is used to enable/disable message capture from Agentic AI applications. We've set it to `true` for this workshop. 
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: this defines how messages should be captured. We've set it to `SPAN` for this workshop, which ensures messages are captured using the span event store. 
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: we've set this to `span_metric,splunk` for the workshop, which ensures that both span and metric data are captured, as well as Splunk-specific features. 

> Hint: run the following command to compare your changes with the expected solution:
> 
> `diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-instrumentation/k8s.yaml`

### Deploy the Updated Application 

We can deploy the updated application using the manifest file as follows:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

Ensure the new application pod has started successfully and the old pod is no longer present: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
````

{{% /tab %}}
{{< /tabs >}}

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

## Troubleshooting 

If you need to troubleshoot, use the following command to view the application logs: 

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```