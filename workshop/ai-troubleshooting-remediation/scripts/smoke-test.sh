#!/usr/bin/env bash
set -euo pipefail

read -r -a KUBECTL <<< "${KUBECTL_CMD:-kubectl}"

"${KUBECTL[@]}" -n ai-remediation port-forward service/checkout-service 18080:8080 >/tmp/ai-remediation-port-forward.log 2>&1 &
PF_PID="$!"
trap 'kill "$PF_PID" >/dev/null 2>&1 || true' EXIT

sleep 3

for _ in $(seq 1 10); do
  curl -sS "http://127.0.0.1:18080/checkout?cart=smoke" >/dev/null || true
done

echo "Smoke traffic sent to checkout-service. If ISSUE_MODE=latency-errors, some requests are expected to fail."
