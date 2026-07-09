#!/usr/bin/env bash
# Remove workshop resources: k3d cluster, Splunk collector, app namespace, Compose stack, and optional local images.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"
REGISTRY_NAME="${REGISTRY_NAME:-cosmic-shop-registry}"
TAG="${TAG:-latest}"
APPS_ONLY=false
KEEP_IMAGES=false
SKIP_COMPOSE=false

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Remove resources created during the Context Propagation workshop.

Options:
  --apps-only     Delete Kubernetes namespace + Helm collector only (keep k3d cluster)
  --keep-images   Do not remove local cosmic-shop Docker images
  --skip-compose  Do not stop docker compose stack
  -h, --help      Show this help

Default (no flags): full teardown — Compose down, Helm uninstall, k3d cluster + registry, generated files, local images.

Your .env file is never deleted (Splunk credentials are preserved).
Telemetry already sent to Splunk Observability Cloud is not removed.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apps-only) APPS_ONLY=true; shift ;;
    --keep-images) KEEP_IMAGES=true; shift ;;
    --skip-compose) SKIP_COMPOSE=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-cosmic-shop}"
REGISTRY_NAME="${REGISTRY_NAME:-cosmic-shop-registry}"
TAG="${TAG:-latest}"

APPS=(catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend)

echo "=== Cosmic Observatory Shop — workshop cleanup ==="
echo ""

if [[ "${SKIP_COMPOSE}" == false ]] && [[ -f "${ROOT_DIR}/docker-compose.yml" ]]; then
  echo "1. Stopping Docker Compose stack (if running)..."
  if docker compose --env-file "${ROOT_DIR}/.env" -f "${ROOT_DIR}/docker-compose.yml" ps -q 2>/dev/null | grep -q .; then
    docker compose --env-file "${ROOT_DIR}/.env" -f "${ROOT_DIR}/docker-compose.yml" down --remove-orphans
    echo "   OK: docker compose down"
  else
    echo "   OK: no Compose containers running"
  fi
else
  echo "1. Skipping Docker Compose cleanup"
fi

echo ""
echo "2. Removing Splunk OTel Collector (Helm)..."
if command -v helm >/dev/null 2>&1 && helm list -n cosmic-shop 2>/dev/null | grep -q splunk-otel-collector; then
  helm uninstall splunk-otel-collector -n cosmic-shop
  echo "   OK: helm uninstall splunk-otel-collector"
else
  echo "   OK: no Helm release splunk-otel-collector in cosmic-shop"
fi

echo ""
if [[ "${APPS_ONLY}" == true ]]; then
  echo "3. Deleting Kubernetes namespace cosmic-shop (--apps-only)..."
  if kubectl get namespace cosmic-shop >/dev/null 2>&1; then
    kubectl delete namespace cosmic-shop --wait=true --timeout=120s
    echo "   OK: namespace cosmic-shop deleted"
  else
    echo "   OK: namespace cosmic-shop not found"
  fi
  echo ""
  echo "4. Skipping k3d cluster delete (--apps-only)"
else
  echo "3. Deleting k3d cluster '${K3D_CLUSTER_NAME}'..."
  if command -v k3d >/dev/null 2>&1 && k3d cluster list 2>/dev/null | grep -q "^${K3D_CLUSTER_NAME} "; then
    k3d cluster delete "${K3D_CLUSTER_NAME}"
    echo "   OK: k3d cluster deleted"
  else
    echo "   OK: k3d cluster '${K3D_CLUSTER_NAME}' not found"
  fi

  echo ""
  echo "4. Removing k3d registry '${REGISTRY_NAME}' (if present)..."
  if command -v k3d >/dev/null 2>&1 && k3d registry list 2>/dev/null | grep -q "${REGISTRY_NAME}"; then
    k3d registry delete "${REGISTRY_NAME}" 2>/dev/null || true
    echo "   OK: registry removed (or already gone with cluster)"
  else
    echo "   OK: registry '${REGISTRY_NAME}' not found"
  fi
fi

echo ""
echo "5. Removing generated local files..."
if [[ -f "${ROOT_DIR}/deploy/k8s/otel.env" ]]; then
  rm -f "${ROOT_DIR}/deploy/k8s/otel.env"
  echo "   OK: removed deploy/k8s/otel.env"
else
  echo "   OK: no generated otel.env"
fi

if [[ "${KEEP_IMAGES}" == false ]]; then
  echo ""
  echo "6. Removing local workshop Docker images..."
  removed=0
  for app in "${APPS[@]}"; do
    if docker image inspect "cosmic-shop/${app}:${TAG}" >/dev/null 2>&1; then
      docker rmi -f "cosmic-shop/${app}:${TAG}" >/dev/null 2>&1 && removed=$((removed + 1)) || true
    fi
    if docker image inspect "localhost:5111/cosmic-shop/${app}:${TAG}" >/dev/null 2>&1; then
      docker rmi -f "localhost:5111/cosmic-shop/${app}:${TAG}" >/dev/null 2>&1 && removed=$((removed + 1)) || true
    fi
  done
  echo "   OK: removed ${removed} image tag(s) (if any existed)"
else
  echo ""
  echo "6. Skipping Docker image removal (--keep-images)"
fi

echo ""
echo "=== Cleanup complete ==="
echo ""
echo "Preserved:"
echo "  - .env (Splunk credentials)"
echo "  - Source code and workshop docs"
echo "  - Data already ingested in Splunk Observability Cloud"
echo ""
if [[ "${APPS_ONLY}" == true ]]; then
  echo "k3d cluster '${K3D_CLUSTER_NAME}' is still running. Redeploy with:"
  echo "  make build && make deploy"
else
  echo "To run the workshop again from scratch:"
  echo "  make setup-k3d && make build && make deploy"
fi
echo ""
echo "Verify ports are free:"
echo "  lsof -i :30080 -i :15672 -i :5111 2>/dev/null || echo 'Ports 30080, 15672, 5111 are available'"
