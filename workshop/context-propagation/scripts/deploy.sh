#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${REGISTRY:-localhost:5111}"
TAG="${TAG:-latest}"
APPS=(catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker frontend)

# Host exports (workshop VM): REALM, ACCESS_TOKEN, CLUSTER_NAME, DEPLOYMENT_ENV=workshop-${INSTANCE}
CLUSTER_NAME="${CLUSTER_NAME:-${INSTANCE:+${INSTANCE}-cluster}}"
CLUSTER_NAME="${CLUSTER_NAME:-cosmic-shop-cluster}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-${INSTANCE:+workshop-${INSTANCE}}}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-workshop-context-prop}"

k3d_cluster_exists() {
  local name="$1"
  command -v k3d >/dev/null 2>&1 && k3d cluster list 2>/dev/null | grep -q "^${name} "
}

# Pick the k3d cluster that actually exists (CLUSTER_NAME before bare INSTANCE).
K3D_CLUSTER_OVERRIDE="${K3D_CLUSTER_NAME:-}"
K3D_CLUSTER_NAME=""
for candidate in "${CLUSTER_NAME}" "${K3D_CLUSTER_OVERRIDE}" "${INSTANCE:+${INSTANCE}-cluster}" "${INSTANCE:-}" "cosmic-shop"; do
  [[ -z "${candidate}" ]] && continue
  if k3d_cluster_exists "${candidate}"; then
    K3D_CLUSTER_NAME="${candidate}"
    break
  fi
done
if [[ -z "${K3D_CLUSTER_NAME}" ]]; then
  if [[ -n "${INSTANCE:-}" ]]; then
    K3D_CLUSTER_NAME="${CLUSTER_NAME}"
  else
    K3D_CLUSTER_NAME="cosmic-shop"
  fi
fi

required_vars=(REALM ACCESS_TOKEN)
for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "Required variable ${var} is not exported on the host"
    exit 1
  fi
done

echo "Deploy config:"
echo "  realm=${REALM}"
echo "  clusterName=${CLUSTER_NAME}"
echo "  deployment.environment=${DEPLOYMENT_ENV}"
echo "  k3d cluster=${K3D_CLUSTER_NAME}"
echo ""

wait_rollout() {
  local deploy="$1"
  local timeout="$2"

  echo "Waiting for deployment/${deploy} (timeout ${timeout})..."
  if kubectl -n cosmic-shop rollout status "deployment/${deploy}" --timeout="${timeout}"; then
    return 0
  fi

  echo ""
  echo "ERROR: Rollout timed out for deployment/${deploy}"
  echo ""
  kubectl -n cosmic-shop get pods -l "app=${deploy}" -o wide 2>/dev/null || true
  echo ""
  kubectl -n cosmic-shop describe deployment "${deploy}" 2>/dev/null | tail -25 || true

  local pod
  pod="$(kubectl -n cosmic-shop get pods -l "app=${deploy}" \
    -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  if [[ -n "${pod}" ]]; then
    echo ""
    echo "Pod events for ${pod}:"
    kubectl -n cosmic-shop describe pod "${pod}" 2>/dev/null | sed -n '/Events:/,$p' || true
    echo ""
    echo "Recent logs for ${pod}:"
    kubectl -n cosmic-shop logs "${pod}" --tail=40 2>/dev/null \
      || kubectl -n cosmic-shop logs "${pod}" --previous --tail=40 2>/dev/null \
      || echo "(no logs available)"
  fi

  echo ""
  echo "Common fixes:"
  echo "  1. Run 'make build' before deploy (images must exist locally)"
  echo "  2. Run 'make collector' if Splunk OTel Collector is not installed"
  echo "  3. Check: kubectl -n cosmic-shop get secret splunk-otel"
  echo "  4. Reset stuck deployment: kubectl -n cosmic-shop rollout restart deployment/${deploy}"
  exit 1
}

collector_is_ready() {
  if ! kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent >/dev/null 2>&1; then
    return 1
  fi
  local ready desired
  ready="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent \
    -o jsonpath='{.status.numberReady}' 2>/dev/null || echo 0)"
  desired="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent \
    -o jsonpath='{.status.desiredNumberScheduled}' 2>/dev/null || echo 0)"
  [[ "${ready}" -ge 1 && "${ready}" == "${desired}" ]]
}

ensure_splunk_collector() {
  if collector_is_ready; then
    local ready desired
    ready="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent \
      -o jsonpath='{.status.numberReady}')"
    desired="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent \
      -o jsonpath='{.status.desiredNumberScheduled}')"
    echo "  OK: splunk-otel-collector-agent (${ready}/${desired} ready)"
    return 0
  fi

  if kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent >/dev/null 2>&1; then
    echo "  Collector DaemonSet found but not ready - waiting..."
  else
    echo "  Splunk OTel Collector not installed - running 'make collector'..."
    bash "${ROOT_DIR}/scripts/install-splunk-collector.sh"
  fi

  echo "  Waiting for collector agents (timeout 180s)..."
  if ! kubectl -n cosmic-shop wait --for=condition=Ready pod \
    -l 'app=splunk-otel-collector,component=otel-collector-agent' \
    --timeout=180s >/dev/null 2>&1; then
    echo ""
    echo "ERROR: Splunk OTel Collector did not become ready in time."
    echo "  Check: kubectl -n cosmic-shop get pods | grep splunk"
    echo "  Logs:  kubectl -n cosmic-shop logs -l app=splunk-otel-collector,component=otel-collector-agent --tail=30"
    exit 1
  fi
  echo "  OK: Splunk OTel Collector ready"
}

echo "Preflight: checking local images..."
missing=0
for app in "${APPS[@]}"; do
  if ! docker image inspect "cosmic-shop/${app}:${TAG}" >/dev/null 2>&1; then
    echo "  MISSING: cosmic-shop/${app}:${TAG} - run 'make build' first"
    missing=1
  else
    echo "  OK: cosmic-shop/${app}:${TAG}"
  fi
done
if [[ "${missing}" -eq 1 ]]; then
  exit 1
fi

echo ""
echo "Preflight: checking k3d cluster..."
if ! command -v k3d >/dev/null 2>&1 || ! k3d cluster list 2>/dev/null | grep -q "^${K3D_CLUSTER_NAME} "; then
  echo "ERROR: k3d cluster '${K3D_CLUSTER_NAME}' not found."
  echo ""
  echo "Available k3d clusters:"
  k3d cluster list 2>/dev/null || true
  echo ""
  echo "  make setup-k3d && make build && make deploy"
  exit 1
fi
echo "  OK: k3d cluster ${K3D_CLUSTER_NAME}"

echo ""
echo "Preflight: Splunk OTel Collector (apps export OTLP to node :4318)..."
ensure_splunk_collector

echo ""
echo "Deploying Cosmic Observatory Shop to Kubernetes..."

# Load images into k3d nodes — required; clusters cannot pull localhost:5111 from the host
IMAGE_PREFIX="cosmic-shop"
K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME}" bash "${ROOT_DIR}/scripts/import-images-k3d.sh"

# OTel resource attributes must match collector clusterName + environment for Infra <-> APM correlation
printf '%s\n' \
  "OTEL_RESOURCE_ATTRIBUTES=deployment.environment=${DEPLOYMENT_ENV},k8s.cluster.name=${CLUSTER_NAME},service.namespace=cosmic-shop" \
  "SPLUNK_METRICS_ENABLED=true" \
  "OTEL_PROPAGATORS=tracecontext,baggage" \
  > "${ROOT_DIR}/deploy/k8s/otel.env"
echo "Generated otel.env: deployment.environment=${DEPLOYMENT_ENV}, k8s.cluster.name=${CLUSTER_NAME}"

# Secret must exist before pods that reference splunk-otel start
kubectl apply -f "${ROOT_DIR}/deploy/k8s/namespace.yaml"
kubectl -n cosmic-shop create secret generic splunk-otel \
  --from-literal=accessToken="${ACCESS_TOKEN}" \
  --from-literal=realm="${REALM}" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -k "${ROOT_DIR}/deploy/k8s"

# Remove legacy deployments from prior workshop versions
kubectl -n cosmic-shop delete deployment storefront-api order-worker --ignore-not-found

for app in "${APPS[@]}"; do
  kubectl -n cosmic-shop set image "deployment/${app}" \
    "${app}=${IMAGE_PREFIX}/${app}:${TAG}"
  kubectl -n cosmic-shop patch deployment "${app}" --type=json \
    -p='[{"op":"replace","path":"/spec/template/spec/containers/0/imagePullPolicy","value":"Never"}]' \
    2>/dev/null || true
done

# Clear any pods stuck on old image references
kubectl -n cosmic-shop delete pod -l 'app in (catalog-api,frontend-api,order-api,payment-gateway,payment-api,fulfillment-worker,frontend)' \
  --force --grace-period=0 2>/dev/null || true

wait_rollout gateway 120s
wait_rollout rabbitmq 180s
wait_rollout catalog-api 180s
wait_rollout frontend-api 180s
wait_rollout order-api 180s
wait_rollout payment-gateway 180s
wait_rollout payment-api 240s
wait_rollout fulfillment-worker 240s
wait_rollout frontend 120s

echo ""
echo "Deployment complete."
echo "  Shop UI:      http://localhost:30080"
echo "  RabbitMQ UI:  http://localhost:15672  (guest/guest)"
echo "                  If UI does not load: docker ps --filter name=k3d-${K3D_CLUSTER_NAME}-serverlb --format '{{.Ports}}'"
echo "                  then: kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672"
echo ""
echo "Generate traffic by placing orders in the shop, then inspect traces in Splunk Observability Cloud."
