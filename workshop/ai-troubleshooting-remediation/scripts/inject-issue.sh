#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-latency-errors}"
read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"

case "$MODE" in
  healthy|latency|errors|latency-errors|crashloop)
    ;;
  *)
    echo "Usage: $0 [healthy|latency|errors|latency-errors|crashloop]" >&2
    exit 1
    ;;
esac

"${KUBECTL[@]}" -n ai-remediation set env deployment/inventory-service "ISSUE_MODE=$MODE"

if [[ "$MODE" == "crashloop" ]]; then
  echo "ISSUE_MODE=crashloop applied. The inventory-service pods are expected to restart."
  "${KUBECTL[@]}" -n ai-remediation get pods -l app=inventory-service
else
  "${KUBECTL[@]}" -n ai-remediation rollout status deployment/inventory-service --timeout=5m
  echo "ISSUE_MODE=$MODE applied to inventory-service."
fi
