#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$DEMO_DIR"
set -a
[[ -f .env ]] && source .env
set +a

for _ in $(seq 1 10); do
  curl -sS "http://127.0.0.1:${CHECKOUT_APP_PORT:-18080}/checkout?cart=smoke" >/dev/null || true
done

echo "Sent smoke checkout traffic to http://127.0.0.1:${CHECKOUT_APP_PORT:-18080}/checkout."
