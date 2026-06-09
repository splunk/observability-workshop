#!/usr/bin/env bash
set -euo pipefail

MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-business-journey}"
COLLECTOR_NAMESPACE="${COLLECTOR_NAMESPACE:-splunk-otel}"
APP_NAMESPACE="${APP_NAMESPACE:-otel-demo}"

require_command() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "ok: $1"
  else
    echo "missing: $1" >&2
    return 1
  fi
}

doctor() {
  local missing=0
  require_command docker || missing=1
  require_command minikube || missing=1
  require_command kubectl || missing=1
  require_command helm || missing=1
  require_command jq || missing=1

  if [[ -n "${SPLUNK_REALM:-}" ]]; then
    echo "ok: SPLUNK_REALM"
  else
    echo "missing: SPLUNK_REALM" >&2
    missing=1
  fi

  if [[ -n "${SPLUNK_ACCESS_TOKEN:-}" ]]; then
    echo "ok: SPLUNK_ACCESS_TOKEN"
  else
    echo "missing: SPLUNK_ACCESS_TOKEN" >&2
    missing=1
  fi

  if [[ "$missing" -ne 0 ]]; then
    exit 1
  fi
}

if [[ "${1:-}" == "doctor" ]]; then
  doctor
  exit 0
fi

if minikube status -p "$MINIKUBE_PROFILE" >/dev/null 2>&1; then
  minikube update-context -p "$MINIKUBE_PROFILE" >/dev/null
else
  echo "Minikube profile '$MINIKUBE_PROFILE' is not running." >&2
  exit 1
fi

echo "collector namespace: $COLLECTOR_NAMESPACE"
kubectl -n "$COLLECTOR_NAMESPACE" get pods

echo ""
echo "application namespace: $APP_NAMESPACE"
kubectl -n "$APP_NAMESPACE" get pods

echo ""
echo "frontend service:"
kubectl -n "$APP_NAMESPACE" get svc astronomy-shop-frontend-proxy 2>/dev/null || true
