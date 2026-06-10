#!/usr/bin/env bash
set -euo pipefail

SECRET_NAME="${SECRET_NAME:-splunk-observability-token}"
STUDENT_NAMESPACE_PREFIX="${STUDENT_NAMESPACE_PREFIX:-student}"
STUDENT_COUNT="${STUDENT_COUNT:-20}"

if [[ -z "${SPLUNK_ACCESS_TOKEN:-}" ]]; then
  cat >&2 <<'EOF'
SPLUNK_ACCESS_TOKEN is required.

Usage:
  export SPLUNK_ACCESS_TOKEN='<lab-scoped-ingest-token>'
  infra/scripts/preload-splunk-observability-token.sh

The token is read from the environment and is not printed.
EOF
  exit 1
fi

if ! [[ "$STUDENT_COUNT" =~ ^[0-9]+$ ]] || (( STUDENT_COUNT < 1 || STUDENT_COUNT > 60 )); then
  echo "STUDENT_COUNT must be an integer between 1 and 60." >&2
  exit 1
fi

for index in $(seq 1 "$STUDENT_COUNT"); do
  namespace="$(printf '%s-%02d' "$STUDENT_NAMESPACE_PREFIX" "$index")"

  kubectl create secret generic "$SECRET_NAME" \
    --namespace "$namespace" \
    --from-literal="splunk_observability_access_token=$SPLUNK_ACCESS_TOKEN" \
    --from-literal="SPLUNK_ACCESS_TOKEN=$SPLUNK_ACCESS_TOKEN" \
    --dry-run=client \
    --output yaml \
    | kubectl apply --namespace "$namespace" --filename -
done

for index in $(seq 1 "$STUDENT_COUNT"); do
  namespace="$(printf '%s-%02d' "$STUDENT_NAMESPACE_PREFIX" "$index")"
  kubectl get secret "$SECRET_NAME" --namespace "$namespace"
done
