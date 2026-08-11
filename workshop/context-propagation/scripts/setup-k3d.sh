#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY_PORT="${REGISTRY_PORT:-5111}"
REGISTRY_NAME="${REGISTRY_NAME:-cosmic-shop-registry}"

CLUSTER_NAME="${CLUSTER_NAME:-${INSTANCE:+${INSTANCE}-cluster}}"
CLUSTER_NAME="${CLUSTER_NAME:-cosmic-shop-cluster}"

k3d_cluster_exists() {
  local name="$1"
  command -v k3d >/dev/null 2>&1 && k3d cluster list 2>/dev/null | grep -q "^${name} "
}

if [[ -z "${K3D_CLUSTER_NAME:-}" ]]; then
  for candidate in "${CLUSTER_NAME}" "${INSTANCE:+${INSTANCE}-cluster}" "${INSTANCE:-}" "cosmic-shop"; do
    [[ -z "${candidate}" ]] && continue
    if k3d_cluster_exists "${candidate}"; then
      K3D_CLUSTER_NAME="${candidate}"
      break
    fi
  done
  if [[ -z "${K3D_CLUSTER_NAME:-}" ]]; then
    if [[ -n "${INSTANCE:-}" ]]; then
      K3D_CLUSTER_NAME="${CLUSTER_NAME}"
    else
      K3D_CLUSTER_NAME="cosmic-shop"
    fi
  fi
fi

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
