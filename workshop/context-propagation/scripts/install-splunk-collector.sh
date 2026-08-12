#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Host exports (workshop VM): REALM, ACCESS_TOKEN, CLUSTER_NAME, DEPLOYMENT_ENV=workshop-${INSTANCE}
REALM="${REALM:?REALM must be exported on the host}"
ACCESS_TOKEN="${ACCESS_TOKEN:?ACCESS_TOKEN must be exported on the host}"

CLUSTER_NAME="${CLUSTER_NAME:-${INSTANCE:+${INSTANCE}-cluster}}"
CLUSTER_NAME="${CLUSTER_NAME:-cosmic-shop-cluster}"

DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-${INSTANCE:+workshop-${INSTANCE}}}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-workshop-context-prop}"

# Helm chart field `environment` → deployment.environment in Splunk (must match make deploy / app otel.env)
ENVIRONMENT="${DEPLOYMENT_ENV}"

VALUES_FILE="${ROOT_DIR}/deploy/helm/splunk-otel-values.yaml"

echo "Installing Splunk OTel Collector with:"
echo "  realm=${REALM}"
echo "  clusterName=${CLUSTER_NAME}"
echo "  environment=${ENVIRONMENT}"

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
echo "Ensure app pods use the same values (make deploy generates otel-config from exported env)."
