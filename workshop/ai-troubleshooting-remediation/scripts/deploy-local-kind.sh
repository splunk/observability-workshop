#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before running this script.}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM before running this script.}"

KIND_CLUSTER_NAME="${KIND_CLUSTER_NAME:-ai-remediation}"
IMAGE="${IMAGE:-ai-remediation-app:local}"
export CLUSTER_NAME="${CLUSTER_NAME:-$KIND_CLUSTER_NAME}"
export ENVIRONMENT="${ENVIRONMENT:-ai-remediation-workshop}"
read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"

if ! command -v kind >/dev/null 2>&1; then
  echo "kind is required for local deployment. Install kind or use scripts/deploy-cloud.sh." >&2
  exit 1
fi

if ! kind get clusters | grep -qx "$KIND_CLUSTER_NAME"; then
  kind create cluster --name "$KIND_CLUSTER_NAME"
else
  kind export kubeconfig --name "$KIND_CLUSTER_NAME"
fi

docker build -t "$IMAGE" "$WORKSHOP_DIR/app"
kind load docker-image "$IMAGE" --name "$KIND_CLUSTER_NAME"

"$SCRIPT_DIR/install-collector.sh"

"${KUBECTL[@]}" apply -f "$WORKSHOP_DIR/k8s/namespace.yaml"
sed "s#ai-remediation-app:local#$IMAGE#g" "$WORKSHOP_DIR/k8s/app.yaml" | "${KUBECTL[@]}" apply -f -

"${KUBECTL[@]}" -n ai-remediation rollout status deployment/checkout-service --timeout=5m
"${KUBECTL[@]}" -n ai-remediation rollout status deployment/inventory-service --timeout=5m
"${KUBECTL[@]}" -n ai-remediation rollout status deployment/remediation-loadgen --timeout=5m

echo "Local lab app deployed to kind cluster=$KIND_CLUSTER_NAME"
echo "Run ./scripts/inject-issue.sh latency-errors to create the APM troubleshooting scenario."
