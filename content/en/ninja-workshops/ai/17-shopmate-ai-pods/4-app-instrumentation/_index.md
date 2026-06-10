---
title: App Instrumentation
linkTitle: 4. App Instrumentation
weight: 4
archetype: chapter
time: 50 minutes
description: Deploy ShopMate Sports, point it at the student collector, and verify AI assistant traces in Splunk Observability Cloud.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are an **application operator** validating AI workflow telemetry. Your goal is to find one complete ShopMate trace in Splunk.
{{% /notice %}}

## Deploy ShopMate Sports

Apply the provided manifest:

```bash
cd workshop/clus-shopmate-exercises
cp workshop/lab-files/shopmate-ai.yaml ./shopmate-ai.yaml
kubectl apply -n "$STUDENT_NAMESPACE" -f shopmate-ai.yaml
kubectl rollout status deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
```

Expected result:

- `deployment/shopmate-ai` exists in your namespace.
- Service `shopmate-ai` exposes port `8080`.

## Point The App At Your Collector

```bash
export OTEL_SERVICE_NAME=shopmate-ai
export OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

Apply the values if the manifest did not already include them:

```bash
kubectl set env deploy/shopmate-ai -n "$STUDENT_NAMESPACE" \
  OTEL_SERVICE_NAME="$OTEL_SERVICE_NAME" \
  OTEL_EXPORTER_OTLP_ENDPOINT="$OTEL_EXPORTER_OTLP_ENDPOINT" \
  OTEL_EXPORTER_OTLP_PROTOCOL="$OTEL_EXPORTER_OTLP_PROTOCOL"
```

Also confirm the resource attributes include your environment:

```bash
kubectl set env deploy/shopmate-ai -n "$STUDENT_NAMESPACE" \
  OTEL_RESOURCE_ATTRIBUTES="deployment.environment=${STUDENT_ID},k8s.namespace.name=${STUDENT_NAMESPACE},k8s.cluster.name=${LOGICAL_CLUSTER_NAME}"
```

Restart and validate:

```bash
kubectl rollout status deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
kubectl logs deploy/shopmate-ai -n "$STUDENT_NAMESPACE" --tail=100
```

## Auto Instrumentation Example

ShopMate uses Splunk-supported zero-code instrumentation for OpenAI Agents SDK and OpenAI-compatible NVIDIA NIM calls. In Kubernetes, the prebuilt image and manifest should already start the app with the instrumentation entrypoint. For local or maintainer validation, the same pattern is:

```bash
cd workshop/clus-shopmate-exercises
python3 -m pip install -r shopmate-sports/requirements.txt

export OTEL_SERVICE_NAME=shopmate-ai
export OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=${STUDENT_ID},k8s.namespace.name=${STUDENT_NAMESPACE},k8s.cluster.name=${LOGICAL_CLUSTER_NAME}"

export NIM_BASE_URL="http://nim-service.nim-system.svc.cluster.local:8000/v1"
export NIM_API_KEY="<nim-api-key-or-lab-placeholder>"
export NIM_MODEL="meta/llama-3.2-1b-instruct"

opentelemetry-instrument python shopmate-sports/server.py
```

Expected auto-instrumented evidence:

| Evidence | Why it matters |
| --- | --- |
| OpenAI Agents SDK spans | Shows agent orchestration and tool activity. |
| OpenAI-compatible NIM spans | Shows model request timing and token fields. |
| GenAI span metrics | Feeds Splunk AI Agent Monitoring and tokenomics views. |
| `deployment.environment` resource attribute | Separates each student's lab signals. |

## Custom Instrumentation Example

The app also adds small custom spans so the trace is easier to read as a retail workflow. These spans live in `workshop/clus-shopmate-exercises/shopmate-sports/server.py`.

```python { title="shopmate-sports/server.py" }
from opentelemetry import trace as otel_trace

CUSTOM_TRACER = otel_trace.get_tracer("shopmate.custom") if otel_trace else None

def workflow_span_context(message, history, specialist_count):
    if not CUSTOM_TRACER:
        return nullcontext(None)
    return CUSTOM_TRACER.start_as_current_span(
        "shopmate.workflow",
        attributes={
            "shopmate.workflow.name": "multi_agent_retail_assistant",
            "shopmate.model.system": "nvidia_nim",
            "shopmate.model.name": NIM_MODEL,
            "shopmate.coordinator.agent_name": "ShoppingAssistantAgent",
            "shopmate.request.preview": preview_text(message),
            "shopmate.history.user_messages": sum(
                1 for item in history if item.get("role") == "user"
            ),
            "shopmate.specialist.count": specialist_count,
        },
    )
```

The app uses the same tracer for specialist agent steps:

```python { title="shopmate-sports/server.py" }
def agent_step_span_context(agent_name, prompt):
    if not CUSTOM_TRACER:
        return nullcontext(None)
    return CUSTOM_TRACER.start_as_current_span(
        f"shopmate.agent.{agent_name}",
        attributes={
            "shopmate.agent.name": agent_name,
            "shopmate.model.system": "nvidia_nim",
            "shopmate.model.name": NIM_MODEL,
            "shopmate.agent.prompt.preview": preview_text(prompt, 400),
        },
    )
```

After the response is created, the workflow span records app-owned response context:

```python { title="shopmate-sports/server.py" }
workflow_span.set_attribute("shopmate.response.preview", preview_text(reply))
workflow_span.set_attribute("shopmate.response.tokens.estimated", estimate_tokens(reply))
workflow_span.set_attribute(
    "shopmate.specialist.names",
    ",".join([*specialist_outputs.keys(), "ShoppingAssistantAgent"]),
)
```

{{% notice title="Attribute Ownership" style="info" %}}
Auto instrumentation owns the standard `gen_ai.*` span and metric fields. The custom spans use `shopmate.*` attributes for app-owned workflow context, safe previews, and estimated response size without duplicating GenAI agent nodes.
{{% /notice %}}

## Open the Website

Port-forward the service:

```bash
kubectl port-forward -n "$STUDENT_NAMESPACE" svc/shopmate-ai 8080:8080
```

Open:

```text
http://127.0.0.1:8080/
```

Send a retail prompt:

```text
Find me waterproof trail running shoes under $200 and check pickup options.
```

Expected result:

- The website returns a shopping assistant response.
- The app emits a trace with `service.name=shopmate-ai`.
- The trace includes `deployment.environment=<STUDENT_ID>`.

## Find the Trace in Splunk

In Splunk Observability Cloud, use a recent time range and filter:

```text
service.name = shopmate-ai
deployment.environment = <your student id>
operation = POST /api/chat
```

Record:

| Field | Value |
| --- | --- |
| Trace start time | |
| Trace duration | |
| Number of spans | |
| Slowest span | |
| LLM or NIM span count | |

## Expected Trace Shape

The trace may include:

- ShopMate API span.
- Shopping assistant span.
- Catalog, inventory, policy, or store tool spans.
- NIM-backed LLM span.
- Token usage fields from Splunk AI Agent Monitoring instrumentation.
- Safe synthetic prompt or response content when capture is enabled for the lab.

{{% notice title="Monitoring Source of Truth" style="info" %}}
Use Splunk trace and metric data as the monitoring source of truth. Token counts shown in the ShopMate UI are helpful feedback, but the lab conclusions should come from telemetry.
{{% /notice %}}
