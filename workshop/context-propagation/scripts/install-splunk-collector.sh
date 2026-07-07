#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -f "${ROOT_DIR}/.env" ]]; then
  echo "Missing .env file. Copy .env.example to .env first."
  exit 1
fi

set -a
# shellcheck disable=SC1091
source "${ROOT_DIR}/.env"
set +a

REALM="${SPLUNK_REALM:?SPLUNK_REALM required}"
ACCESS_TOKEN="${SPLUNK_ACCESS_TOKEN:?SPLUNK_ACCESS_TOKEN required}"
CLUSTER_NAME="${CLUSTER_NAME:-cosmic-shop-cluster}"
ENVIRONMENT="${SPLUNK_DEPLOYMENT_ENV:-workshop-context-prop}"
VALUES_FILE="${ROOT_DIR}/deploy/helm/splunk-otel-values.yaml"

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart 2>/dev/null || true
helm repo update

helm upgrade --install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace cosmic-shop \
  --create-namespace \
  -f "${VALUES_FILE}" \
  --set="splunkObservability.realm=${REALM}" \
  --set="splunkObservability.accessToken=${ACCESS_TOKEN}" \
  --set="clusterName=${CLUSTER_NAME}" \
  --set="environment=${ENVIRONMENT}"

echo "Splunk OTel Collector installed in namespace cosmic-shop."
echo "Waiting for collector agents to be ready..."
if kubectl -n cosmic-shop wait --for=condition=Ready pod \
  -l 'app=splunk-otel-collector,component=otel-collector-agent' \
  --timeout=180s 2>/dev/null; then
  echo "Collector agents ready."
else
  echo "WARNING: Collector agents not ready yet — check: kubectl -n cosmic-shop get pods | grep splunk"
fi
echo ""
echo "Infrastructure ↔ APM correlation tags:"
echo "  clusterName=${CLUSTER_NAME}  → k8s.cluster.name in Infrastructure navigator"
echo "  environment=${ENVIRONMENT}     → deployment.environment on collector telemetry"
echo ""
echo "Ensure app pods use the same values (make deploy generates otel-config from .env)."
echo "Verify: bash scripts/verify-infra-apm-config.sh"
