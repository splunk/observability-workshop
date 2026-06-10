#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-latency-errors}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

case "$MODE" in
  healthy|latency|errors|latency-errors)
    ;;
  *)
    echo "Usage: $0 [healthy|latency|errors|latency-errors]" >&2
    exit 1
    ;;
esac

cd "$DEMO_DIR"
set -a
[[ -f .env ]] && source .env
set +a

curl -sS -X POST "http://127.0.0.1:${CHECKOUT_APP_PORT:-18080}/admin/issue-mode?mode=${MODE}"
echo ""
echo "Issue mode set to ${MODE}."
