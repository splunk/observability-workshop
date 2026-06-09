#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before running this script.}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM before running this script.}"

MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-ai-remediation}"
IMAGE="${IMAGE:-ai-remediation-app:local}"
export CLUSTER_NAME="${CLUSTER_NAME:-$MINIKUBE_PROFILE}"
export ENVIRONMENT="${ENVIRONMENT:-ai-remediation-workshop}"

if ! command -v minikube >/dev/null 2>&1; then
  echo "minikube is required for this deployment path." >&2
  exit 1
fi

if ! minikube status -p "$MINIKUBE_PROFILE" >/dev/null 2>&1; then
  minikube start -p "$MINIKUBE_PROFILE"
else
  minikube update-context -p "$MINIKUBE_PROFILE"
fi

docker build -t "$IMAGE" "$WORKSHOP_DIR/app"
minikube image load "$IMAGE" -p "$MINIKUBE_PROFILE"

"$SCRIPT_DIR/install-collector.sh"

kubectl apply -f "$WORKSHOP_DIR/k8s/namespace.yaml"
sed "s#ai-remediation-app:local#$IMAGE#g" "$WORKSHOP_DIR/k8s/app.yaml" | kubectl apply -f -

kubectl -n ai-remediation rollout status deployment/checkout-service --timeout=5m
kubectl -n ai-remediation rollout status deployment/inventory-service --timeout=5m
kubectl -n ai-remediation rollout status deployment/remediation-loadgen --timeout=5m

echo "Local lab app deployed to Minikube profile=$MINIKUBE_PROFILE"
echo "Run ./scripts/inject-issue.sh latency-errors to create the APM troubleshooting scenario."

