#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"
REGISTRY_PORT="${REGISTRY_PORT:-5111}"
REGISTRY_NAME="${REGISTRY_NAME:-cosmic-shop-registry}"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"

echo "Creating k3d cluster '${K3D_CLUSTER_NAME}' with local registry on port ${REGISTRY_PORT}..."

if k3d cluster list | grep -q "^${K3D_CLUSTER_NAME} "; then
  echo "Cluster '${K3D_CLUSTER_NAME}' already exists. Skipping creation."
else
  k3d cluster create "${K3D_CLUSTER_NAME}" \
    --agents 1 \
    --registry-create "${REGISTRY_NAME}:${REGISTRY_PORT}" \
    --port "30080:30080@loadbalancer" \
    --port "15672:31672@loadbalancer" \
    --k3s-arg "--disable=traefik@server:0"
fi

kubectl cluster-info
echo "k3d cluster '${K3D_CLUSTER_NAME}' ready."
