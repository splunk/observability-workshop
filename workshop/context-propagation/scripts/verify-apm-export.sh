#!/usr/bin/env bash
# Verify Splunk APM export path: collector running and OTLP reachable from app pods.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0

pass() { echo "  OK: $*"; }
fail() { echo "  FAIL: $*"; FAIL=1; }
warn() { echo "  WARN: $*"; }

echo "=== Splunk APM export diagnostics ==="
echo ""

if ! command -v kubectl >/dev/null 2>&1; then
  fail "kubectl not found"
  exit 1
fi

if ! kubectl get namespace cosmic-shop >/dev/null 2>&1; then
  fail "namespace cosmic-shop not found — run 'make setup-k3d && make deploy'"
  exit 1
fi

echo "1. Splunk OTel Collector (required — apps send OTLP to node :4318)"
if kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent >/dev/null 2>&1; then
  READY="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent -o jsonpath='{.status.numberReady}')"
  DESIRED="$(kubectl -n cosmic-shop get daemonset splunk-otel-collector-agent -o jsonpath='{.status.desiredNumberScheduled}')"
  if [[ "${READY}" -ge 1 && "${READY}" == "${DESIRED}" ]]; then
    pass "splunk-otel-collector-agent DaemonSet (${READY}/${DESIRED} ready)"
  else
    fail "Collector DaemonSet not ready (${READY}/${DESIRED}) — run 'make collector' or 'make deploy'"
  fi
else
  fail "splunk-otel-collector-agent DaemonSet not found — run 'make collector' or 'make deploy'"
fi

COLLECTOR_PODS="$(kubectl -n cosmic-shop get pods -l 'app=splunk-otel-collector,component=otel-collector-agent' 2>/dev/null || true)"
if [[ -n "${COLLECTOR_PODS}" ]]; then
  echo "${COLLECTOR_PODS}" | sed 's/^/       /'
fi

if command -v helm >/dev/null 2>&1; then
  if helm list -n cosmic-shop 2>/dev/null | grep -q splunk-otel-collector; then
    pass "Helm release splunk-otel-collector in cosmic-shop"
  else
    warn "Helm release not in cosmic-shop namespace (collector may be elsewhere)"
  fi
fi

echo ""
echo "2. OTLP reachability from a backend pod"
APP_POD="$(kubectl -n cosmic-shop get pod -l app=catalog-api -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
if [[ -z "${APP_POD}" ]]; then
  warn "catalog-api pod not found — deploy apps first"
else
  NODE_IP="$(kubectl -n cosmic-shop get pod "${APP_POD}" -o jsonpath='{.status.hostIP}')"
  for PORT in 4318 4317; do
    if kubectl -n cosmic-shop exec "${APP_POD}" -- sh -c "wget -q --spider --timeout=2 http://${NODE_IP}:${PORT} 2>/dev/null || nc -z ${NODE_IP} ${PORT} 2>/dev/null"; then
      pass "Node ${NODE_IP}:${PORT} reachable from ${APP_POD}"
    else
      fail "Node ${NODE_IP}:${PORT} NOT reachable — collector agent not listening"
    fi
  done
fi

echo ""
echo "3. App telemetry env (catalog-api sample)"
if [[ -n "${APP_POD}" ]]; then
  OTEL_EP="$(kubectl -n cosmic-shop exec "${APP_POD}" -- printenv OTEL_EXPORTER_OTLP_ENDPOINT 2>/dev/null || true)"
  OTEL_SVC="$(kubectl -n cosmic-shop exec "${APP_POD}" -- printenv OTEL_SERVICE_NAME 2>/dev/null || true)"
  HAS_TOKEN="$(kubectl -n cosmic-shop exec "${APP_POD}" -- sh -c 'test -n "$SPLUNK_ACCESS_TOKEN" && echo yes || echo no' 2>/dev/null || true)"
  if [[ -n "${OTEL_EP}" ]]; then
    pass "OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EP}"
  else
    fail "OTEL_EXPORTER_OTLP_ENDPOINT not set on catalog-api"
  fi
  pass "OTEL_SERVICE_NAME=${OTEL_SVC}"
  if [[ "${HAS_TOKEN}" == "yes" ]]; then
    pass "SPLUNK_ACCESS_TOKEN is set on pod"
  else
    fail "SPLUNK_ACCESS_TOKEN missing on pod"
  fi
fi

echo ""
echo "4. Generate test traffic"
if [[ -n "${APP_POD}" ]]; then
  kubectl -n cosmic-shop exec "${APP_POD}" -- wget -qO- http://localhost:3002/health >/dev/null 2>&1 \
    && pass "Triggered catalog-api /health" \
    || warn "Could not hit catalog-api health endpoint"
fi

echo ""
if [[ "${FAIL}" -eq 1 ]]; then
  echo "Result: APM export path broken. Fix failures above, then:"
  echo "  make collector"
  echo "  kubectl -n cosmic-shop rollout restart deployment/catalog-api deployment/frontend-api deployment/order-api deployment/payment-gateway deployment/payment-api deployment/fulfillment-worker"
  echo ""
  echo "In Splunk O11y: APM → filter deployment.environment from .env (default workshop-context-prop)"
  exit 1
fi

echo "Result: APM export path looks healthy. Wait 1–2 min, then check Splunk APM → Services."
exit 0
