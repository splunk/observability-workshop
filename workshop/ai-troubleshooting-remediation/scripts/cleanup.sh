#!/usr/bin/env bash
set -euo pipefail

KIND_CLUSTER_NAME="${KIND_CLUSTER_NAME:-ai-remediation}"
MINIKUBE_PROFILE="${MINIKUBE_PROFILE:-ai-remediation}"
read -r -a HELM <<< "${HELM_CMD:-helm}"
read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"

"${KUBECTL[@]}" delete namespace ai-remediation --ignore-not-found

if [[ "${DELETE_COLLECTOR:-false}" == "true" ]]; then
  "${HELM[@]}" uninstall splunk-otel-collector --ignore-not-found || true
fi

if [[ "${DELETE_KIND_CLUSTER:-false}" == "true" ]]; then
  if command -v kind >/dev/null 2>&1 && kind get clusters | grep -qx "$KIND_CLUSTER_NAME"; then
    kind delete cluster --name "$KIND_CLUSTER_NAME"
  fi
fi

if [[ "${DELETE_MINIKUBE_CLUSTER:-false}" == "true" ]]; then
  if command -v minikube >/dev/null 2>&1 && minikube profile list -o json | grep -q "\"Name\":\"$MINIKUBE_PROFILE\""; then
    minikube delete -p "$MINIKUBE_PROFILE"
  fi
fi

echo "Cleanup complete."
