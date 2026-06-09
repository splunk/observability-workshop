#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before running this script.}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM before running this script.}"

IMAGE="${IMAGE:-ai-remediation-app:local}"
export CLUSTER_NAME="${CLUSTER_NAME:-microk8s-ai-remediation}"
export ENVIRONMENT="${ENVIRONMENT:-ai-remediation-workshop}"
export KUBECTL_CMD="${KUBECTL_CMD:-microk8s kubectl}"
export HELM_CMD="${HELM_CMD:-microk8s helm3}"

if ! command -v microk8s >/dev/null 2>&1; then
  echo "microk8s is required for this deployment path." >&2
  exit 1
fi

microk8s status --wait-ready
microk8s enable dns helm3

docker build -t "$IMAGE" "$WORKSHOP_DIR/app"
tmp_image="$(mktemp -t ai-remediation-image.XXXXXX.tar)"
trap 'rm -f "$tmp_image"' EXIT
docker save "$IMAGE" -o "$tmp_image"
microk8s ctr image import "$tmp_image"

"$SCRIPT_DIR/install-collector.sh"

microk8s kubectl apply -f "$WORKSHOP_DIR/k8s/namespace.yaml"
sed "s#ai-remediation-app:local#$IMAGE#g" "$WORKSHOP_DIR/k8s/app.yaml" | microk8s kubectl apply -f -

microk8s kubectl -n ai-remediation rollout status deployment/checkout-service --timeout=5m
microk8s kubectl -n ai-remediation rollout status deployment/inventory-service --timeout=5m
microk8s kubectl -n ai-remediation rollout status deployment/remediation-loadgen --timeout=5m

echo "Local lab app deployed to MicroK8s cluster=$CLUSTER_NAME"
echo "For follow-up scripts, run with KUBECTL_CMD='microk8s kubectl' HELM_CMD='microk8s helm3'."
echo "Run KUBECTL_CMD='microk8s kubectl' ./scripts/inject-issue.sh latency-errors to create the APM troubleshooting scenario."

