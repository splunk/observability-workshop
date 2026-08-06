#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
local_only="false"

if [[ "${1:-}" == "--local-only" ]]; then
  local_only="true"
  shift
fi

config_path="${1:-${script_dir}/agent.yaml}"
if [[ "${config_path}" != /* ]]; then
  config_path="${script_dir}/${config_path}"
fi

if [[ ! -f "${config_path}" ]]; then
  echo "Configuration not found: ${config_path}" >&2
  exit 1
fi

export SPLUNK_LISTEN_INTERFACE="${SPLUNK_LISTEN_INTERFACE:-127.0.0.1}"
export SPLUNK_MEMORY_LIMIT_MIB="${SPLUNK_MEMORY_LIMIT_MIB:-256}"

collector_args=(--config="${config_path}")

if [[ "${local_only}" == "true" || -z "${SPLUNK_REALM:-}" || -z "${SPLUNK_ACCESS_TOKEN:-}" ]]; then
  echo "Local-only mode: cloud exporters are disabled; telemetry stays in Collector debug output."
  export SPLUNK_REALM="local"
  export SPLUNK_ACCESS_TOKEN="unused-local-token"
  export SPLUNK_API_URL="http://127.0.0.1:65535"
  export SPLUNK_INGEST_URL="http://127.0.0.1:65535"
  collector_args+=(
    '--set=service.pipelines.metrics.exporters=[debug]'
    '--set=service.pipelines.traces.exporters=[debug/detailed]'
  )
else
  export SPLUNK_API_URL="${SPLUNK_API_URL:-https://api.${SPLUNK_REALM}.observability.splunkcloud.com}"
  export SPLUNK_INGEST_URL="${SPLUNK_INGEST_URL:-https://ingest.${SPLUNK_REALM}.observability.splunkcloud.com}"
  echo "Cloud mode: exporting host metrics and traces to realm ${SPLUNK_REALM}."
fi

cd "${script_dir}"
exec ./otelcol "${collector_args[@]}"
