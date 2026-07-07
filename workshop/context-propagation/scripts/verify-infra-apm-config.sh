#!/usr/bin/env bash
# Verify local and cluster configuration for Splunk Infrastructure ↔ APM correlation.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0

pass() { echo "  OK: $*"; }
fail() { echo "  FAIL: $*"; FAIL=1; }
warn() { echo "  WARN: $*"; }

echo "=== Splunk Infrastructure & APM correlation config ==="
echo ""

if [[ ! -f "${ROOT_DIR}/.env" ]]; then
  fail "Missing .env — copy .env.example and configure Splunk credentials"
  exit 1
fi

set -a
# shellcheck disable=SC1091
source "${ROOT_DIR}/.env"
set +a

CLUSTER_NAME="${CLUSTER_NAME:-cosmic-shop-cluster}"
SPLUNK_DEPLOYMENT_ENV="${SPLUNK_DEPLOYMENT_ENV:-workshop-context-prop}"

echo "1. .env alignment (collector + apps must share these values)"
if [[ -n "${SPLUNK_REALM:-}" ]]; then
  pass "SPLUNK_REALM=${SPLUNK_REALM}"
else
  fail "SPLUNK_REALM is not set"
fi

if [[ -n "${SPLUNK_ACCESS_TOKEN:-}" ]]; then
  pass "SPLUNK_ACCESS_TOKEN is set"
else
  fail "SPLUNK_ACCESS_TOKEN is not set"
fi

pass "CLUSTER_NAME=${CLUSTER_NAME} (Infrastructure navigator + k8s.cluster.name on spans)"
pass "SPLUNK_DEPLOYMENT_ENV=${SPLUNK_DEPLOYMENT_ENV} (deployment.environment on spans + RUM)"

if [[ "${SPLUNK_DEPLOYMENT_ENV}" == "workshop" ]]; then
  warn "SPLUNK_DEPLOYMENT_ENV=workshop — frontend Dockerfile default; prefer workshop-context-prop for correlation"
fi

echo ""
echo "2. Generated otel.env (applied on deploy via Kustomize configMapGenerator)"
OTEL_ENV="${ROOT_DIR}/deploy/k8s/otel.env"
if [[ -f "${OTEL_ENV}" ]]; then
  if grep -q "k8s.cluster.name=${CLUSTER_NAME}" "${OTEL_ENV}" \
    && grep -q "deployment.environment=${SPLUNK_DEPLOYMENT_ENV}" "${OTEL_ENV}"; then
    pass "otel.env contains matching cluster and environment attributes"
  else
    fail "otel.env is stale — run 'make deploy' to regenerate from .env"
  fi
else
  warn "otel.env not found — run 'make deploy' to generate before checking cluster ConfigMap"
fi

echo ""
echo "3. Kubernetes cluster (optional — requires kubectl + deployed stack)"
if ! command -v kubectl >/dev/null 2>&1; then
  warn "kubectl not available — skipping cluster checks"
elif ! kubectl get namespace cosmic-shop >/dev/null 2>&1; then
  warn "namespace cosmic-shop not found — run 'make setup-k3d && make collector && make deploy'"
else
  CM_ATTRS="$(kubectl -n cosmic-shop get configmap otel-config -o jsonpath='{.data.OTEL_RESOURCE_ATTRIBUTES}' 2>/dev/null || true)"
  if [[ -z "${CM_ATTRS}" ]]; then
    fail "ConfigMap otel-config missing or has no OTEL_RESOURCE_ATTRIBUTES"
  elif [[ "${CM_ATTRS}" == *"k8s.cluster.name=${CLUSTER_NAME}"* ]] \
    && [[ "${CM_ATTRS}" == *"deployment.environment=${SPLUNK_DEPLOYMENT_ENV}"* ]]; then
    pass "otel-config ConfigMap matches .env"
  else
    fail "otel-config ConfigMap out of sync with .env — run 'make deploy'"
    echo "       current: ${CM_ATTRS}"
  fi

  if command -v helm >/dev/null 2>&1 && helm list -n cosmic-shop 2>/dev/null | grep -q splunk-otel-collector; then
    HELM_CLUSTER="$(helm get values splunk-otel-collector -n cosmic-shop -o json 2>/dev/null \
      | python3 -c "import json,sys; v=json.load(sys.stdin); print(v.get('clusterName',''))" 2>/dev/null || true)"
    HELM_ENV="$(helm get values splunk-otel-collector -n cosmic-shop -o json 2>/dev/null \
      | python3 -c "import json,sys; v=json.load(sys.stdin); print(v.get('environment',''))" 2>/dev/null || true)"

    if [[ "${HELM_CLUSTER}" == "${CLUSTER_NAME}" ]]; then
      pass "Helm clusterName=${HELM_CLUSTER}"
    else
      fail "Helm clusterName='${HELM_CLUSTER}' != .env CLUSTER_NAME='${CLUSTER_NAME}' — run 'make collector'"
    fi

    if [[ "${HELM_ENV}" == "${SPLUNK_DEPLOYMENT_ENV}" ]]; then
      pass "Helm environment=${HELM_ENV}"
    else
      fail "Helm environment='${HELM_ENV}' != .env SPLUNK_DEPLOYMENT_ENV='${SPLUNK_DEPLOYMENT_ENV}' — run 'make collector'"
    fi
  else
    warn "Splunk OTel Collector Helm release not found — run 'make collector'"
  fi

  for app in catalog-api frontend-api order-api payment-gateway payment-api fulfillment-worker; do
    SVC="$(kubectl -n cosmic-shop get deployment "${app}" -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="OTEL_SERVICE_NAME")].value}' 2>/dev/null || true)"
    if [[ "${SVC}" == "${app}" ]]; then
      pass "${app} OTEL_SERVICE_NAME=${SVC}"
    elif [[ -n "${SVC}" ]]; then
      warn "${app} OTEL_SERVICE_NAME=${SVC} (expected ${app})"
    else
      warn "${app} deployment not found or missing OTEL_SERVICE_NAME"
    fi
  done
fi

echo ""
echo "4. Splunk Observability Cloud checks (manual)"
echo "   - Infrastructure → Kubernetes → Clusters: look for '${CLUSTER_NAME}'"
echo "   - APM → filter deployment.environment=${SPLUNK_DEPLOYMENT_ENV}"
echo "   - APM service page → Related Content → Kubernetes pod (requires k8s.cluster.name + k8s.pod.name on spans)"
echo "   - RUM → session → Backend Trace link (after propagation fixes in steps 07–09)"
echo ""

if [[ "${FAIL}" -eq 1 ]]; then
  echo "Result: configuration issues found — fix failures above, then run 'make collector && make deploy'"
  exit 1
fi

echo "Result: configuration looks aligned for Infrastructure & APM correlation."
exit 0
