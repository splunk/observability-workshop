#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

: "${SPLUNK_ACCESS_TOKEN:?Set SPLUNK_ACCESS_TOKEN before running this script.}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM before running this script.}"
: "${IMAGE_REGISTRY:?Set IMAGE_REGISTRY to a writable registry path, for example ghcr.io/my-org.}"

IMAGE_TAG="${IMAGE_TAG:-latest}"
IMAGE="${IMAGE_REGISTRY%/}/ai-remediation-app:$IMAGE_TAG"
read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"
export CLUSTER_NAME="${CLUSTER_NAME:-$("${KUBECTL[@]}" config current-context | tr '/:@' '---')}"
export ENVIRONMENT="${ENVIRONMENT:-ai-remediation-workshop}"

docker build -t "$IMAGE" "$WORKSHOP_DIR/app"
docker push "$IMAGE"

"$SCRIPT_DIR/install-collector.sh"

"${KUBECTL[@]}" apply -f "$WORKSHOP_DIR/k8s/namespace.yaml"
sed "s#ai-remediation-app:local#$IMAGE#g" "$WORKSHOP_DIR/k8s/app.yaml" | "${KUBECTL[@]}" apply -f -

"${KUBECTL[@]}" -n ai-remediation rollout status deployment/checkout-service --timeout=5m
"${KUBECTL[@]}" -n ai-remediation rollout status deployment/inventory-service --timeout=5m
"${KUBECTL[@]}" -n ai-remediation rollout status deployment/remediation-loadgen --timeout=5m

echo "Cloud lab app deployed with image=$IMAGE"
echo "Run ./scripts/inject-issue.sh latency-errors to create the APM troubleshooting scenario."
