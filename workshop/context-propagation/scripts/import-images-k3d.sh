#!/usr/bin/env bash
# Import workshop images into k3d so pods use local images (no registry pull).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"
TAG="${TAG:-latest}"
DEFAULT_APPS=(catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend)

if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"

if [[ $# -gt 0 ]]; then
  APPS=("$@")
else
  APPS=("${DEFAULT_APPS[@]}")
fi

if ! command -v k3d >/dev/null 2>&1; then
  echo "k3d is not installed."
  exit 1
fi

if ! k3d cluster list 2>/dev/null | grep -q "^${K3D_CLUSTER_NAME} "; then
  echo "k3d cluster '${K3D_CLUSTER_NAME}' not found."
  echo ""
  k3d cluster list 2>/dev/null || true
  echo ""
  echo "Set K3D_CLUSTER_NAME in .env (default: cosmic-shop). Run 'make setup-k3d' first."
  exit 1
fi

echo "Importing images into k3d cluster '${K3D_CLUSTER_NAME}'..."
for app in "${APPS[@]}"; do
  if ! docker image inspect "cosmic-shop/${app}:${TAG}" >/dev/null 2>&1; then
    echo "  MISSING local image cosmic-shop/${app}:${TAG} — run 'make build' first"
    exit 1
  fi
  echo "  Importing cosmic-shop/${app}:${TAG}..."
  k3d image import "cosmic-shop/${app}:${TAG}" -c "${K3D_CLUSTER_NAME}"
done

echo ""
echo "Verifying images on k3d node..."
if docker exec "k3d-${K3D_CLUSTER_NAME}-server-0" crictl images 2>/dev/null | grep -E "cosmic-shop/(order-api|payment-gateway)"; then
  echo "OK: images present on cluster node."
else
  echo "Warning: could not verify via crictl (import may still have succeeded)."
fi

echo ""
echo "Done. Restart deployments to pick up new images:"
echo "  kubectl -n cosmic-shop rollout restart deployment/<service>"
