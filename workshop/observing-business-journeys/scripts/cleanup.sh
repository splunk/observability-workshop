#!/usr/bin/env bash
set -euo pipefail

MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-business-journey}"
COLLECTOR_NAMESPACE="${COLLECTOR_NAMESPACE:-splunk-otel}"
APP_NAMESPACE="${APP_NAMESPACE:-otel-demo}"
COLLECTOR_RELEASE="${COLLECTOR_RELEASE:-splunk-otel-collector}"
APP_RELEASE="${APP_RELEASE:-astronomy-shop}"

helm -n "$APP_NAMESPACE" uninstall "$APP_RELEASE" >/dev/null 2>&1 || true
helm -n "$COLLECTOR_NAMESPACE" uninstall "$COLLECTOR_RELEASE" >/dev/null 2>&1 || true

kubectl delete namespace "$APP_NAMESPACE" --ignore-not-found=true
kubectl delete namespace "$COLLECTOR_NAMESPACE" --ignore-not-found=true

if [[ "${DELETE_MINIKUBE_PROFILE:-false}" == "true" ]]; then
  minikube delete -p "$MINIKUBE_PROFILE"
fi

echo "Workshop Kubernetes resources removed."
