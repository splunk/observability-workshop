#!/usr/bin/env bash
set -euo pipefail

setup_failed() {
  exit_code=$?
  trap - ERR
  echo >&2
  echo "Setup did not complete. Review the error above, then rerun the script." >&2
  exit "${exit_code}"
}
trap setup_failed ERR

collector_version="0.157.0"
repo_owner="chentaow-splunk"
repo_name="observability-workshop"
repo_ref="codex/advanced-collector-conf2026"
content_path="content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026"
workshop_root="${PWD}"
agent_dir="${workshop_root}/1-agent"
config_path="${agent_dir}/agent_config.yaml"
environment_path="${workshop_root}/workshop-env.sh"

echo
echo "Splunk Advanced OpenTelemetry Workshop .conf26"
echo "================================================"

for command_name in curl jq uname sed; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Required command not found: ${command_name}" >&2
    exit 1
  fi
done

case "$(uname -s)" in
  Darwin)
    if [[ "$(uname -m)" != "arm64" ]]; then
      echo "This workshop supports Apple Silicon Macs, not Intel Macs." >&2
      exit 1
    fi
    xattr -dr com.apple.quarantine otelcol loadgen 2>/dev/null || true
    echo "Apple Silicon macOS detected."
    ;;
  Linux)
    case "$(uname -m)" in
      x86_64|amd64|aarch64|arm64) ;;
      *)
        echo "Unsupported Linux CPU architecture: $(uname -m)" >&2
        exit 1
        ;;
    esac
    echo "Linux $(uname -m) detected."
    ;;
  *)
    echo "Unsupported platform. Use Linux or an Apple Silicon Mac." >&2
    exit 1
    ;;
esac

if [[ ! -f otelcol || ! -f loadgen ]]; then
  echo "otelcol and loadgen must be in the current directory." >&2
  exit 1
fi

chmod +x otelcol loadgen

if installed_version="$(./otelcol --version 2>&1)"; then
  :
else
  echo "The Collector binary does not run on $(uname -s)/$(uname -m)." >&2
  exit 1
fi

if [[ "${installed_version}" != *"${collector_version}"* ]]; then
  echo "Expected Collector ${collector_version}, but found: ${installed_version}" >&2
  exit 1
fi

if ! loadgen_help="$(./loadgen --help 2>&1)"; then
  echo "The load generator does not run on $(uname -s)/$(uname -m)." >&2
  exit 1
fi
if [[ "${loadgen_help}" != *"-preview"* ]]; then
  echo "This workshop requires the conf2026 load generator with -preview support." >&2
  echo "Download the loadgen binary from the conf2026 path in Prerequisites." >&2
  exit 1
fi
unset loadgen_help

cloud_setting="${CONF2026_CLOUD_ENABLED:-}"
if [[ -z "${cloud_setting}" ]]; then
  read -r -p "Also send metrics and traces to Splunk Observability Cloud? [y/N]: " cloud_setting
fi

case "${cloud_setting}" in
  y|Y|yes|YES|Yes|true|TRUE|True|1)
    cloud_enabled=true
    ;;
  ""|n|N|no|NO|No|false|FALSE|False|0)
    cloud_enabled=false
    ;;
  *)
    echo "Enter y or n." >&2
    exit 1
    ;;
esac

realm="${REALM:-}"
splunk_access_token="${SPLUNK_ACCESS_TOKEN:-${ACCESS_TOKEN:-}}"
splunk_api_url="${SPLUNK_API_URL:-}"
splunk_ingest_url="${SPLUNK_INGEST_URL:-}"
splunk_hec_token="${SPLUNK_HEC_TOKEN:-not-configured}"
splunk_hec_url="${SPLUNK_HEC_URL:-https://127.0.0.1:8088/services/collector}"
splunk_listen_interface="${SPLUNK_LISTEN_INTERFACE:-127.0.0.1}"
splunk_memory_limit_mib="${SPLUNK_MEMORY_LIMIT_MIB:-512}"

if [[ "${cloud_enabled}" == "true" ]]; then
  if [[ -z "${realm}" ]]; then
    read -r -p "Splunk Observability Cloud realm (for example us1): " realm
  fi
  if [[ -z "${realm}" ]]; then
    echo "A realm is required for cloud export." >&2
    exit 1
  fi

  if [[ -z "${splunk_access_token}" ]]; then
    read -r -s -p "Splunk Observability Cloud access token with ingest authorization: " splunk_access_token
    echo
  fi
  if [[ -z "${splunk_access_token}" ]]; then
    echo "An access token with ingest authorization is required for cloud export." >&2
    exit 1
  fi

  splunk_api_url="${splunk_api_url:-https://api.${realm}.observability.splunkcloud.com}"
  splunk_ingest_url="${splunk_ingest_url:-https://ingest.${realm}.observability.splunkcloud.com}"
else
  realm=""
  splunk_access_token="not-configured"
  splunk_api_url="http://127.0.0.1:18089"
  splunk_ingest_url="http://127.0.0.1:18089"
fi

mkdir -p "${agent_dir}"
config_url="https://github.com/${repo_owner}/${repo_name}/raw/refs/heads/${repo_ref}/${content_path}/agent_config.yaml"
curl -fL --retry 3 "${config_url}" -o "${config_path}"

# Keep all eight pipelines in one configuration. Without cloud export, replace
# active cloud destinations with nop while the workshop pipelines continue
# local debug and file validation.
if [[ "${cloud_enabled}" == "false" ]]; then
  sed -i.bak \
    -e 's/exporters: \[debug, file\/traces, otlp_http\]/exporters: [debug, file\/traces]/' \
    -e 's/exporters: \[signalfx\]/exporters: [nop]/' \
    -e 's/exporters: \[otlp_http\/entities\]/exporters: [nop]/' \
    -e 's/extensions: \[headers_setter, health_check, http_forwarder, http_forwarder\/opamp_splunk_o11y, opamp\/splunk_o11y, zpages\]/extensions: [health_check, zpages]/' \
    "${config_path}"
  rm -f "${config_path}.bak"
fi

# Remove the obsolete overlay if setup is rerun in an earlier workshop folder.
rm -f "${agent_dir}/agent_config.local.yaml"

{
  printf 'export REALM=%q\n' "${realm}"
  printf 'export ACCESS_TOKEN=%q\n' "${splunk_access_token}"
  printf 'export SPLUNK_ACCESS_TOKEN=%q\n' "${splunk_access_token}"
  printf 'export SPLUNK_API_URL=%q\n' "${splunk_api_url}"
  printf 'export SPLUNK_INGEST_URL=%q\n' "${splunk_ingest_url}"
  printf 'export SPLUNK_HEC_TOKEN=%q\n' "${splunk_hec_token}"
  printf 'export SPLUNK_HEC_URL=%q\n' "${splunk_hec_url}"
  printf 'export SPLUNK_LISTEN_INTERFACE=%q\n' "${splunk_listen_interface}"
  printf 'export SPLUNK_MEMORY_LIMIT_MIB=%q\n' "${splunk_memory_limit_mib}"
  printf 'export CONF2026_CLOUD_ENABLED=%q\n' "${cloud_enabled}"
} > "${environment_path}"
chmod 600 "${environment_path}"
unset splunk_access_token splunk_hec_token
trap - ERR

echo
echo "Workshop setup complete."
echo "Collector: ${installed_version}"
echo "Cloud export: ${cloud_enabled}"
echo
echo "Start the Agent:"
echo "  cd 1-agent"
echo "  source ../workshop-env.sh"
echo "  ../otelcol --config=agent_config.yaml"
