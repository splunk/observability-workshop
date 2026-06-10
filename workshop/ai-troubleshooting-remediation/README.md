# AI Troubleshooting and Remediation Lab App

This directory contains the sample application used by the **AI Troubleshooting Agent and Remediation Plan** workshop.

The app is intentionally small:

- `checkout-service` receives checkout requests.
- `inventory-service` reserves inventory for checkout requests.
- `loadgen` continuously calls `checkout-service`.

## Application Flow

The lab models a checkout dependency chain:

```text
remediation-loadgen -> checkout-service /checkout -> inventory-service /reserve
```

`checkout-service` creates cart context such as cart type, SKU, quantity, and cart value. It then calls `inventory-service` to reserve inventory. `inventory-service` can run normally or simulate an incident by adding latency, returning errors, or exiting at startup to create Kubernetes restart signals.

## Instrumentation Model

The application is instrumented with Python OpenTelemetry and shows both automatic and custom instrumentation.

Automatic instrumentation:

- `app/requirements.txt` installs `opentelemetry-distro`, OTLP export, FastAPI instrumentation, `requests` instrumentation, and logging instrumentation.
- `app/Dockerfile` runs `opentelemetry-bootstrap -a install` so the instrumentation packages are configured in the image.
- `k8s/app.yaml` starts each process with `opentelemetry-instrument`, which creates spans for inbound FastAPI requests and outbound `requests` calls.
- `OTEL_SERVICE_NAME` names the APM services as `checkout-service`, `inventory-service`, and `remediation-loadgen`.
- `OTEL_RESOURCE_ATTRIBUTES` adds `deployment.environment=ai-remediation-workshop`, `service.version=1.0.0`, and `app.workshop=ai-troubleshooting-remediation`.
- `OTEL_EXPORTER_OTLP_ENDPOINT=http://$(NODE_IP):4317` sends OTLP traces to the node-local Splunk OpenTelemetry Collector agent.

Custom instrumentation:

- `checkout_service.py` uses `trace.get_current_span()` to add `app.cart.type`, `app.cart.value`, `app.sku`, and `service.version` to the active request span.
- `checkout_service.py` creates a child span named `checkout.reserve_inventory` around the inventory dependency call.
- `inventory_service.py` adds `app.issue_mode`, `app.sku`, `app.quantity`, and `app.cart.type` so traces show the injected failure context.
- Error paths call `record_exception()` and `set_status(StatusCode.ERROR, ...)` so failed requests are visible in trace analysis.

Those attributes give students concrete evidence to inspect while comparing the AI troubleshooting agent's hypothesis with traces, logs, service metrics, and Kubernetes infrastructure telemetry.

The app supports two issue modes:

- `latency-errors`: `inventory-service` becomes slow and intermittently returns errors. Use this for an APM service alert.
- `crashloop`: `inventory-service` exits on startup. Use this for a Kubernetes infrastructure alert.

## Quick Workshop CLI

Use `ai-remediation` as a BusyBox-style helper for quick demos and workshop resets. It wraps the scripts below and resolves its paths from the script location, so it can be invoked by relative or absolute path.

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<access-token>

./ai-remediation doctor kind
./ai-remediation start kind
```

The `start` command deploys the lab, sends smoke traffic, and injects the default `latency-errors` issue. You can also run each workshop step individually:

```bash
./ai-remediation deploy kind
./ai-remediation smoke kind
./ai-remediation issue latency-errors kind
./ai-remediation status kind
./ai-remediation remediate kind
./ai-remediation cleanup kind
```

For other runtimes, replace `kind` with `minikube`, `microk8s`, or `cloud`. For cloud deployments, set `IMAGE_REGISTRY` before running `deploy` or `start`.

## Install Laptop Tools

macOS:

```bash
./scripts/install-tools-macos.sh
```

Linux:

```bash
LOCAL_RUNTIME=kind ./scripts/install-tools-linux.sh
LOCAL_RUNTIME=minikube ./scripts/install-tools-linux.sh
LOCAL_RUNTIME=microk8s ./scripts/install-tools-linux.sh
```

Windows PowerShell:

```powershell
.\scripts\install-tools-windows.ps1
```

Windows students can also use WSL2 with Ubuntu:

```powershell
.\scripts\install-tools-windows.ps1 -IncludeWsl
```

## Quick Start: Local Laptop with kind

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<access-token>

cd workshop/ai-troubleshooting-remediation
./scripts/deploy-local-kind.sh
./scripts/inject-issue.sh latency-errors
```

## Quick Start: Local Laptop with Minikube

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<access-token>

cd workshop/ai-troubleshooting-remediation
./scripts/deploy-local-minikube.sh
./scripts/inject-issue.sh latency-errors
```

## Quick Start: Local Laptop with MicroK8s

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<access-token>

cd workshop/ai-troubleshooting-remediation
./scripts/deploy-local-microk8s.sh
KUBECTL_CMD="microk8s kubectl" ./scripts/inject-issue.sh latency-errors
```

## Quick Start: Cloud Kubernetes

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<access-token>
export IMAGE_REGISTRY=<registry>/<namespace>

cd workshop/ai-troubleshooting-remediation
./scripts/deploy-cloud.sh
./scripts/inject-issue.sh latency-errors
```

## Remediate

```bash
./scripts/remediate.sh
```

## Clean Up

```bash
./scripts/cleanup.sh
```

Set `DELETE_COLLECTOR=true` to uninstall the Splunk OpenTelemetry Collector. Set `DELETE_KIND_CLUSTER=true` to delete the local kind cluster.
