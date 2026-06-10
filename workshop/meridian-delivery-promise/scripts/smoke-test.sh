#!/usr/bin/env bash
set -euo pipefail

PORT="${MERIDIAN_PORT:-8090}"
BASE_URL="http://localhost:${PORT}"

echo "Checking patient portal health"
curl -fsS "${BASE_URL}/health" | sed 's/.*/  &/'

echo "Confirming one delivery in healthy mode"
curl -fsS -X POST "${BASE_URL}/workshop/incident/healthy" >/dev/null
curl -fsS -X POST "${BASE_URL}/api/confirm" | sed 's/.*/  &/'

echo "Injecting geocode latency"
curl -fsS -X POST "${BASE_URL}/workshop/incident/geocode-latency" >/dev/null
curl -fsS "${BASE_URL}/api/summary" | sed 's/.*/  &/'

echo "Resetting to healthy"
curl -fsS -X POST "${BASE_URL}/workshop/incident/healthy" >/dev/null
