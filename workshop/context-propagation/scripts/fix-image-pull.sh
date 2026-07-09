#!/usr/bin/env bash
# Fix ImagePullBackOff: import images and reset app deployments.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TAG="${TAG:-latest}"
APPS=(catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend)

bash "${ROOT_DIR}/scripts/import-images-k3d.sh"

echo ""
echo "Patching deployments to use local images (imagePullPolicy: Never)..."
for app in "${APPS[@]}"; do
  kubectl -n cosmic-shop set image "deployment/${app}" \
    "${app}=cosmic-shop/${app}:${TAG}" 2>/dev/null || true
  kubectl -n cosmic-shop patch deployment "${app}" --type=json \
    -p='[{"op":"replace","path":"/spec/template/spec/containers/0/imagePullPolicy","value":"Never"}]' \
    2>/dev/null || true
done

echo "Removing stuck pods..."
kubectl -n cosmic-shop delete pod -l 'app in (catalog-api,order-api,payment-gateway,payment-api,fulfillment-worker,frontend)' \
  --force --grace-period=0 2>/dev/null || true

echo ""
echo "Waiting for rollouts..."
for app in "${APPS[@]}"; do
  kubectl -n cosmic-shop rollout status "deployment/${app}" --timeout=180s 2>/dev/null || true
done

kubectl -n cosmic-shop get pods
