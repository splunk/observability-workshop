# Observing Business Journeys Workshop

This lab deploys the OpenTelemetry Astronomy Shop into Minikube, sends telemetry to Splunk Observability Cloud through the Splunk OpenTelemetry Collector, and provides mapping material for modeling business impact in ITSI.

## Quick Start

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<your-access-token>

cd workshop/observing-business-journeys
./scripts/deploy-minikube.sh
```

Open the shop:

```bash
minikube -p business-journey service -n otel-demo astronomy-shop-frontend-proxy --url
```

Or use port forwarding:

```bash
./scripts/port-forward.sh
```

## Failure Scenarios

```bash
./scripts/set-flag.sh checkout
./scripts/set-flag.sh cart
./scripts/set-flag.sh catalog
./scripts/set-flag.sh healthy
```

## Demo ITSI Data Without Live Detectors

If the real Observability Cloud detector integration is not ready, push small demo alert events directly to the Splunk platform HEC endpoint used by ITSI:

```bash
export SPLUNK_HEC_URL=https://<splunk-host>:8088
export SPLUNK_HEC_TOKEN=<hec-token>
export SPLUNK_HEC_INDEX=o11y_alerts
export SPLUNK_HEC_INSECURE=true

./scripts/push-demo-events.sh trigger checkout
./scripts/push-demo-events.sh clear checkout
```

This sends only detector-like alert events. It does not send traces, metrics, or logs to Splunk Enterprise.

## Instrumentation Examples

Optional examples are in:

```text
instrumentation/
```

- `auto-instrumentation-example.yaml` shows how to use the OpenTelemetry Operator for an added uninstrumented service.
- `custom-instrumentation-examples.md` shows Python, Node.js, and Java snippets for app-owned business span attributes.

## Workshop Content

The Hugo workshop pages are in:

```text
content/en/ninja-workshops/13-observing-business-journeys/
```

## Cleanup

```bash
./scripts/cleanup.sh
```

Set `DELETE_MINIKUBE_PROFILE=true` if you also want to delete the Minikube profile.
