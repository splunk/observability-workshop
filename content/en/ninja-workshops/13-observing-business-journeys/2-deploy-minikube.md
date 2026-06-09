---
title: 2. Deploy Astronomy Shop
weight: 2
time: 25 minutes
---

In this section you deploy the Splunk OpenTelemetry Collector and the OpenTelemetry Astronomy Shop into Minikube.

The lab disables the demo's bundled collector, Jaeger, Prometheus, Grafana, and OpenSearch. Application telemetry goes to the node-local Splunk collector on ports `4317` and `4318`.

## Deploy

```bash
cd workshop/observing-business-journeys
./scripts/deploy-minikube.sh
```

The script performs these actions:

- Starts or reuses the `business-journey` Minikube profile.
- Adds the OpenTelemetry and Splunk OpenTelemetry Collector Helm repositories.
- Installs the Splunk OpenTelemetry Collector with trace enrichment rules.
- Installs Astronomy Shop in the `otel-demo` namespace.
- Waits for collector and application deployments to become available.

## Verify Kubernetes

```bash
./scripts/status.sh
```

Expected result:

```text
collector namespace: splunk-otel
application namespace: otel-demo
deployments: available
pods: running
```

## Open the Shop

Use the NodePort URL printed by the deployment script, or run:

```bash
minikube -p business-journey service -n otel-demo astronomy-shop-frontend-proxy --url
```

If the NodePort path is not available on your machine, use port forwarding:

```bash
./scripts/port-forward.sh
```

Then open:

```text
http://localhost:8080
```

The feature flag UI is available at:

```text
http://localhost:8080/feature
```

## Verify Splunk Observability Cloud

In Splunk Observability Cloud:

1. Go to **APM**.
2. Select the environment `business-journey-workshop`.
3. Confirm services such as `frontend`, `cart`, `checkout`, `payment`, and `product-catalog` are visible.
4. Open a trace and confirm these span attributes appear on matching spans:
   - `business.application`
   - `business.capability`
   - `business.transaction`
   - `business.criticality`

{{% notice title="Troubleshooting" style="warning" %}}
If services do not appear in APM after a few minutes, confirm the Splunk collector agent is running with host ports `4317` and `4318`, and confirm the demo pods have `OTEL_COLLECTOR_NAME` set from `status.hostIP`.
{{% /notice %}}
