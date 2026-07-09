#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${REGISTRY:-localhost:5111}"
TAG="${TAG:-latest}"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

build_image() {
  local name="$1"
  local dockerfile="$2"
  local context="${3:-${ROOT_DIR}}"

  echo "Building ${name}:${TAG}..."
  docker build \
    --build-arg SPLUNK_REALM="${SPLUNK_REALM:-us0}" \
    --build-arg SPLUNK_RUM_ACCESS_TOKEN="${SPLUNK_RUM_ACCESS_TOKEN:-}" \
    --build-arg SPLUNK_RUM_APP_NAME="${SPLUNK_RUM_APP_NAME:-cosmic-observatory-shop}" \
    --build-arg SPLUNK_DEPLOYMENT_ENV="${SPLUNK_DEPLOYMENT_ENV:-workshop-context-prop}" \
    -t "cosmic-shop/${name}:${TAG}" \
    -f "${dockerfile}" \
    "${context}"
  docker tag "cosmic-shop/${name}:${TAG}" "${REGISTRY}/cosmic-shop/${name}:${TAG}"
  docker push "${REGISTRY}/cosmic-shop/${name}:${TAG}"
}

dockerfile_for() {
  case "$1" in
    catalog-api) echo "${ROOT_DIR}/services/catalog-api/Dockerfile" ;;
    frontend-api) echo "${ROOT_DIR}/services/frontend-api/Dockerfile" ;;
    order-api) echo "${ROOT_DIR}/services/order-api/Dockerfile" ;;
    payment-gateway) echo "${ROOT_DIR}/services/payment-gateway/Dockerfile" ;;
    payment-api) echo "${ROOT_DIR}/services/payment-api/Dockerfile" ;;
    fulfillment-worker) echo "${ROOT_DIR}/services/fulfillment-worker/Dockerfile" ;;
    frontend) echo "${ROOT_DIR}/services/frontend/Dockerfile" ;;
    *) return 1 ;;
  esac
}

DEFAULT_APPS=(catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend)

if [[ $# -gt 0 ]]; then
  APPS=("$@")
else
  APPS=("${DEFAULT_APPS[@]}")
fi

for app in "${APPS[@]}"; do
  dockerfile="$(dockerfile_for "${app}" || true)"
  if [[ -z "${dockerfile}" ]]; then
    echo "Unknown service: ${app}"
    echo "Valid services: catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend"
    exit 1
  fi
  build_image "${app}" "${dockerfile}"
done

echo "Built and pushed: ${APPS[*]} -> ${REGISTRY}"
