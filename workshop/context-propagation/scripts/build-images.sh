#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${REGISTRY:-localhost:5111}"
TAG="${TAG:-latest}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-${INSTANCE:+workshop-${INSTANCE}}}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-workshop-context-prop}"
RUM_APP_NAME="${RUM_APP_NAME:-${INSTANCE:+workshop-${INSTANCE}}}"
RUM_APP_NAME="${RUM_APP_NAME:-cosmic-observatory-shop}"

build_image() {
  local name="$1"
  local dockerfile="$2"
  local context="${3:-${ROOT_DIR}}"

  echo "Building ${name}:${TAG}..."
  docker build \
    --build-arg REALM="${REALM:-us0}" \
    --build-arg RUM_TOKEN="${RUM_TOKEN:-}" \
    --build-arg RUM_APP_NAME="${RUM_APP_NAME}" \
    --build-arg DEPLOYMENT_ENV="${DEPLOYMENT_ENV}" \
    -t "cosmic-shop/${name}:${TAG}" \
    -f "${dockerfile}" \
    "${context}"

  # Deploy uses k3d image import from cosmic-shop/* tags — registry push is optional.
  if [[ "${PUSH_TO_REGISTRY:-0}" == "1" ]]; then
    if curl -sf "http://${REGISTRY}/v2/" >/dev/null 2>&1; then
      docker tag "cosmic-shop/${name}:${TAG}" "${REGISTRY}/cosmic-shop/${name}:${TAG}"
      docker push "${REGISTRY}/cosmic-shop/${name}:${TAG}"
    else
      echo "WARNING: PUSH_TO_REGISTRY=1 but ${REGISTRY} is not reachable — skipping push for ${name}."
      echo "         Run 'make setup-k3d' to create the k3d registry, or omit PUSH_TO_REGISTRY."
    fi
  fi
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

echo "Built: ${APPS[*]} (tags: cosmic-shop/<service>:${TAG})"
if [[ "${PUSH_TO_REGISTRY:-0}" == "1" ]]; then
  echo "Registry push enabled -> ${REGISTRY}"
fi
