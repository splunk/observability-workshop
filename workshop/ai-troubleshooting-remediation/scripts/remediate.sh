#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/inject-issue.sh" healthy
kubectl -n ai-remediation rollout status deployment/inventory-service --timeout=5m

echo "inventory-service returned to healthy mode."

