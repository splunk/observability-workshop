#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_REALM:?Set SPLUNK_REALM before running this script.}"
: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before running this script.}"

MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-business-journey}"
MINIKUBE_CPUS="${MINIKUBE_CPUS:-4}"
MINIKUBE_MEMORY="${MINIKUBE_MEMORY:-8192}"
MINIKUBE_DISK_SIZE="${MINIKUBE_DISK_SIZE:-30g}"
CLUSTER_NAME="${CLUSTER_NAME:-business-journey-minikube}"
DEPLOYMENT_ENVIRONMENT="${DEPLOYMENT_ENVIRONMENT:-business-journey-workshop}"
COLLECTOR_NAMESPACE="${COLLECTOR_NAMESPACE:-splunk-otel}"
APP_NAMESPACE="${APP_NAMESPACE:-otel-demo}"
COLLECTOR_RELEASE="${COLLECTOR_RELEASE:-splunk-otel-collector}"
APP_RELEASE="${APP_RELEASE:-astronomy-shop}"
SPLUNK_OTEL_CHART_VERSION="${SPLUNK_OTEL_CHART_VERSION:-0.153.1}"
OTEL_DEMO_CHART_VERSION="${OTEL_DEMO_CHART_VERSION:-0.40.9}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "$1 is required." >&2
    exit 1
  fi
}

require_command docker
require_command minikube
require_command kubectl
require_command helm
require_command jq

start_args=(
  -p "$MINIKUBE_PROFILE"
  --cpus "$MINIKUBE_CPUS"
  --memory "$MINIKUBE_MEMORY"
  --disk-size "$MINIKUBE_DISK_SIZE"
)

if [[ -n "${MINIKUBE_DRIVER:-}" ]]; then
  start_args+=(--driver "$MINIKUBE_DRIVER")
fi

if ! minikube status -p "$MINIKUBE_PROFILE" >/dev/null 2>&1; then
  minikube start "${start_args[@]}"
else
  minikube update-context -p "$MINIKUBE_PROFILE"
fi

helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts >/dev/null
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart >/dev/null
helm repo update open-telemetry splunk-otel-collector-chart >/dev/null

helm upgrade --install "$COLLECTOR_RELEASE" \
  splunk-otel-collector-chart/splunk-otel-collector \
  --namespace "$COLLECTOR_NAMESPACE" \
  --create-namespace \
  --version "$SPLUNK_OTEL_CHART_VERSION" \
  --set "splunkObservability.realm=$SPLUNK_REALM" \
  --set "splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
  --set "clusterName=$CLUSTER_NAME" \
  --set "environment=$DEPLOYMENT_ENVIRONMENT" \
  -f "$WORKSHOP_DIR/values/splunk-otel-collector-values.yaml"

kubectl -n "$COLLECTOR_NAMESPACE" rollout status daemonset/"$COLLECTOR_RELEASE-agent" --timeout=5m
kubectl -n "$COLLECTOR_NAMESPACE" rollout status deployment/"$COLLECTOR_RELEASE-k8s-cluster-receiver" --timeout=5m

helm upgrade --install "$APP_RELEASE" \
  open-telemetry/opentelemetry-demo \
  --namespace "$APP_NAMESPACE" \
  --create-namespace \
  --version "$OTEL_DEMO_CHART_VERSION" \
  -f "$WORKSHOP_DIR/values/otel-demo-values.yaml"

kubectl -n "$APP_NAMESPACE" wait --for=condition=available deployment --all --timeout=10m

echo ""
echo "Astronomy Shop deployed."
echo "Minikube profile: $MINIKUBE_PROFILE"
echo "Cluster name: $CLUSTER_NAME"
echo "Environment: $DEPLOYMENT_ENVIRONMENT"
echo ""
echo "Open the shop with:"
echo "  minikube -p $MINIKUBE_PROFILE service -n $APP_NAMESPACE $APP_RELEASE-frontend-proxy --url"
echo ""
echo "Feature flags:"
echo "  ./scripts/set-flag.sh checkout"
echo "  ./scripts/set-flag.sh cart"
echo "  ./scripts/set-flag.sh catalog"
echo "  ./scripts/set-flag.sh healthy"
