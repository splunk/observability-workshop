#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$DEMO_DIR"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example."
  echo "Edit .env and set SPLUNK_ACCESS_TOKEN before rerunning this script."
  exit 1
fi

if grep -q "replace-with-your-observability-access-token" .env; then
  echo "Set SPLUNK_ACCESS_TOKEN in $DEMO_DIR/.env before starting the demo." >&2
  exit 1
fi

docker compose up -d --build
docker compose ps

echo ""
echo "Checkout demo is starting."
echo "Local checkout URL: http://127.0.0.1:${CHECKOUT_APP_PORT:-18080}/scenario"
echo "Run ./scripts/smoke-test.sh to send a few manual requests."
