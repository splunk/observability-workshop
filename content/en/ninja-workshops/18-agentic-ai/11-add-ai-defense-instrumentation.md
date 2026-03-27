---
title: Add AI Defense Instrumentation
linkTitle: 11. Add AI Defense Instrumentation
weight: 11
time: 20 minutes
---

Splunk AI Security Monitoring integrates Splunk Observability for 
[AI with Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html). 
It provides a consolidated view of [security and privacy risks](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita) 
detected at runtime for your AI agents, allowing you to monitor performance and risks in one place.

Splunk AI Security Monitoring helps you to:

* Identify which agents, interactions, and services involve detected or blocked security and privacy risks, such as prompt injection and PII leakage
* Track risk trends alongside latency, errors, and other performance metrics over time
* Investigate risky interactions in trace context, down to specific prompts and responses

In this section, we'll add the AI Defense integration to our Agentic AI application and 
review the resulting data in Splunk Observability Cloud. 

## How It Works 

Splunk AI Security Monitoring provides an instrumentation library, 
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense), 
to automate security and privacy risk tracing for Python-based AI agents. 
This library captures and attaches security telemetry to calls that your 
AI agents make to LLMs (such as OpenAI) and orchestration frameworks 
(such as LangChain) to ensure that every prompt and response can be 
audited against security guardrails and recorded within a unified 
OpenTelemetry trace. It does this by adding the 
`gen_ai.security.event_id attribute` to LLM or workflow spans.

## SDK vs. Gateway Mode

The `opentelemetry-instrumentation-aidefense` library can operate in either SDK mode or gateway mode:

* With the SDK mode, the developer adds explicit security checks using `inspect_prompt()`. This option is best for developers that want full control how security checks are implemented and how issues are addressed. 
* With Gateway mode, LLM calls proxied through Cisco AI Defense Gateway so application code changes are not required. This mode is supported for popular commercial LLMs such as OpenAI, Anthropic, etc. 

This workshop utilizes Gateway mode with Azure OpenAI. 

## Setup the Cisco AI Defense Integration

The first step is to [Set up an integration with Cisco AI Defense](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense). 

If you navigate to **Data Management -> Deployed integrations** and search for `AI Defense`, 
you'll see that this integration has already been configured: 

![AI Defense Config](../images/AIDefenseConfig.png)

## Add Instrumentation Packages

Next, we need to install several instrumentation packages. We can achieve this by
opening the `~/workshop/agentic-ai/base-app/requirements.txt` for editing and adding
the following packages: 

````
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
````

### Build an Updated Docker Image

Build an updated Docker image with a new tag:

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

### Update the Kubernetes Manifest

Before updating the Kubernetes manifest file, let's create a secret to store the 
AI Defense Gateway URL: 

> Note: your instructor will provide the actual AI Defense URL to be used while creating the secret

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-gateway-url='https://us.gateway.aidefense.security.cisco.com/{tenant}/connections/{conn}'
```

Open the `~/workshop/agentic-ai/base-app/k8s.yaml` file for editing and
ensure that only the following environment variables are included:

> Note that `AZURE_OPENAI_ENDPOINT` is now configured to use the AI Defense Gateway URL, to ensure any 
> requests destined for Azure OpenAI are instead sent through the gateway 

```yaml
            - name: AZURE_OPENAI_DEPLOYMENT_NAME
              value: "gpt-4.1-mini"
            - name: AZURE_OPENAI_ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: ai-defense-secret
                  key: ai-defense-gateway-url
            - name: AZURE_OPENAI_API_VERSION
              value: "2024-12-01-preview"
            - name: AZURE_OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: azure-openai-api
                  key: azure-openai-api-key
            # OpenAI Model
            - name: OPENAI_MODEL
              value: "gpt-4.1-mini"
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
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

### Deploy the Updated Application

We can deploy the updated application using the manifest file as follows:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

Run the following command to test the application, including a (fake) credit card 
number to trigger AI Defense's PII detection:

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences. My credit card number is 4111 1111 1111 1111.",
    "travelers": 2
  }'
```

## View Events in Cisco AI Defense

If we login to the AI Defense application directly, we can see that an event was logged for 
our request, and that AI Defense has automatically redacted the credit card number 
we included in the prompt: 

![AI Defense Events](../images/AIDefenseEvents.png)

Note that policies can be configured AI Defense to specify whether we want to monitor 
or block specific types of security issues. In this case, we've chosen to just monitor 
PCI-related issues. 

## View Data in Splunk Observability Cloud

Let's return to Splunk Observability Cloud to see how the trace looks now.

Navigate to `APM` and then select `Agents`. Ensure your environment name
is selected (e.g. `agentic-ai-$INSTANCE`). You'll notice that the page
includes security risks now! 

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

Navigate to `APM -> Trace Analyzer`.

Ensure your environment name is selected (e.g. `agentic-ai-$INSTANCE`).  
Select one of the newer traces. We see that the trace includes security risks now!
Specifically, we can see that a **Privacy - PCI risk ** has been detected for our 
application (but not blocked): 

![Trace with Security Risks](../images/TraceWithSecurityRisks.png)
