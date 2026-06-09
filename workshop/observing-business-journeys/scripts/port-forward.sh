#!/usr/bin/env bash
set -euo pipefail

APP_NAMESPACE="${APP_NAMESPACE:-otel-demo}"
APP_RELEASE="${APP_RELEASE:-astronomy-shop}"
LOCAL_PORT="${LOCAL_PORT:-8080}"

echo "Forwarding http://localhost:$LOCAL_PORT to $APP_RELEASE-frontend-proxy."
echo "Feature flag UI: http://localhost:$LOCAL_PORT/feature"
kubectl -n "$APP_NAMESPACE" port-forward "svc/$APP_RELEASE-frontend-proxy" "$LOCAL_PORT:8080"
