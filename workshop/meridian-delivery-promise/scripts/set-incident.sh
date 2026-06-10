#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-healthy}"
PORT="${MERIDIAN_PORT:-8090}"

curl -fsS -X POST "http://localhost:${PORT}/workshop/incident/${MODE}"
echo
