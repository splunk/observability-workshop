---
title: 10. Instrumentation Examples
weight: 10
time: 20 minutes
---

This workshop uses collector transforms so you can demonstrate business impact without changing Astronomy Shop source code. In production, use a mix of auto instrumentation and custom application instrumentation.

## Choose the Right Instrumentation Path

| Path | Best for | Limitation |
|---|---|---|
| Auto instrumentation | Fast baseline traces for supported runtimes. | It cannot know the business transaction unless you add route or code context. |
| Collector enrichment | Temporary mapping from routes, services, or Kubernetes metadata. | It is less precise than application-owned business context. |
| Custom instrumentation | Business transaction, owner, order value, customer segment, and criticality. | Requires code ownership and release process. |

## Auto Instrumentation Example

Astronomy Shop is already instrumented, so the auto instrumentation example is optional. Use it when you add an uninstrumented service to the lab or when teaching how a customer could onboard an existing service.

Enable the OpenTelemetry Operator during deploy:

```bash
cd workshop/observing-business-journeys

export ENABLE_OTEL_OPERATOR=true
./scripts/deploy-minikube.sh
```

Apply the example `Instrumentation` custom resource and example deployment:

```bash
kubectl apply -f instrumentation/auto-instrumentation-example.yaml
```

The example uses this collector endpoint:

```text
http://splunk-otel-collector-agent.splunk-otel.svc.cluster.local:4317
```

To auto-instrument a real workload, copy the annotation that matches its runtime:

```yaml
metadata:
  annotations:
    instrumentation.opentelemetry.io/inject-java: "otel-demo/astronomy-shop-auto"
    instrumentation.opentelemetry.io/inject-nodejs: "otel-demo/astronomy-shop-auto"
    instrumentation.opentelemetry.io/inject-python: "otel-demo/astronomy-shop-auto"
    instrumentation.opentelemetry.io/inject-dotnet: "otel-demo/astronomy-shop-auto"
```

Use only one runtime annotation per workload.

## Custom Instrumentation Example

Custom instrumentation is where the business map becomes most accurate. For example, checkout code can set the transaction once it knows the operation is an order submission:

```python
from opentelemetry import trace

tracer = trace.get_tracer("checkout")

def checkout(order):
    with tracer.start_as_current_span("checkout.submit") as span:
        span.set_attribute("business.application", "astronomy-shop")
        span.set_attribute("business.transaction", "Complete Checkout")
        span.set_attribute("business.capability", "checkout")
        span.set_attribute("business.criticality", "critical")
        span.set_attribute("business.owner", "revenue-operations")
        span.set_attribute("order.value", order.total)

        return submit_order(order)
```

More examples are in:

```text
workshop/observing-business-journeys/instrumentation/custom-instrumentation-examples.md
```

## Production Guidance

- Use auto instrumentation first to establish trace coverage.
- Add custom span attributes for true business context.
- Use collector transforms as a bridge, not the long-term source of truth.
- Keep MetricSet dimensions low-cardinality.
- Align attribute names with the ITSI service model and detector routing.

{{% notice title="Cardinality" style="warning" %}}
Do not put unique order IDs, user IDs, email addresses, or session IDs into APM MetricSet dimensions. Put those in logs or searchable traces only when privacy and retention policies allow it.
{{% /notice %}}
