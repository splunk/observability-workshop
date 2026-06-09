# AI Troubleshooting and Remediation Lab App

This directory contains the sample application used by the **AI Troubleshooting Agent and Remediation Plan** workshop.

The app is intentionally small:

- `checkout-service` receives checkout requests.
- `inventory-service` reserves inventory for checkout requests.
- `loadgen` continuously calls `checkout-service`.

The app supports two issue modes:

- `latency-errors`: `inventory-service` becomes slow and intermittently returns errors. Use this for an APM service alert.
- `crashloop`: `inventory-service` exits on startup. Use this for a Kubernetes infrastructure alert.

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
