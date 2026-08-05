#!/usr/bin/env bash
set -euo pipefail

setup_failed() {
  exit_code=$?
  trap - ERR
  echo >&2
  echo "Setup did not complete. The 1-agent directory and workshop-env.sh" >&2
  echo "are created only after every prompt and download succeeds." >&2
  exit "${exit_code}"
}
trap setup_failed ERR

# Splunk Advanced OpenTelemetry Workshop .conf26 setup.
# Uses portable binaries like the upstream workshop; it does not install a
# system service or a Gateway Collector.

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
echo "███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗"
echo "██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗"
echo "███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗"
echo "╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝"
echo "███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝"
echo "╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝"
echo
echo "Welcome to the Splunk Advanced OpenTelemetry Workshop .conf26!"
echo "================================================================"
echo

for command_name in curl uname; do
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
    echo "Apple Silicon macOS detected. Removing quarantine attributes..."
    xattr -dr com.apple.quarantine otelcol loadgen 2>/dev/null || true
    ;;
  Linux)
    case "$(uname -m)" in
      x86_64|amd64|aarch64|arm64) ;;
      *)
        echo "Unsupported Linux CPU architecture: $(uname -m)" >&2
        exit 1
        ;;
    esac
    echo "Linux detected."
    ;;
  *)
    echo "Unsupported platform. Use Linux or an Apple Silicon Mac." >&2
    exit 1
    ;;
esac

if [[ ! -f otelcol || ! -f loadgen ]]; then
  echo "otelcol and loadgen must be downloaded before running this script." >&2
  exit 1
fi

chmod +x otelcol loadgen

installed_version="$(./otelcol --version 2>&1)"
if [[ "${installed_version}" != *"${collector_version}"* ]]; then
  echo "Expected Splunk OpenTelemetry Collector ${collector_version}, but found: ${installed_version}" >&2
  exit 1
fi

echo "${installed_version}"
./loadgen --help

realm="${REALM:-}"
splunk_access_token="${SPLUNK_ACCESS_TOKEN:-${ACCESS_TOKEN:-}}"
splunk_api_url="${SPLUNK_API_URL:-}"
splunk_hec_token="${SPLUNK_HEC_TOKEN:-}"
splunk_hec_url="${SPLUNK_HEC_URL:-}"
splunk_ingest_url="${SPLUNK_INGEST_URL:-}"
splunk_listen_interface="${SPLUNK_LISTEN_INTERFACE:-127.0.0.1}"
splunk_memory_limit_mib="${SPLUNK_MEMORY_LIMIT_MIB:-512}"

local_only_setting="${CONF2026_LOCAL_ONLY:-}"
if [[ -z "${local_only_setting}" ]]; then
  read -r -p "Use local-only mode and skip Splunk credentials? [y/N]: " local_only_setting
fi

case "${local_only_setting}" in
  y|Y|yes|YES|Yes|true|TRUE|True|1)
    local_only=true
    ;;
  ""|n|N|no|NO|No|false|FALSE|False|0)
    local_only=false
    ;;
  *)
    echo "Invalid local-only choice: ${local_only_setting}" >&2
    echo "Use y/yes/true/1 or n/no/false/0." >&2
    exit 1
    ;;
esac

cloud_enabled=true
hec_enabled=true

if [[ "${local_only}" == "true" ]]; then
  cloud_enabled=false
  hec_enabled=false
  realm=""
  splunk_access_token="not-configured"
  splunk_hec_token="not-configured"
  splunk_api_url="http://127.0.0.1:18089"
  splunk_ingest_url="http://127.0.0.1:18089"
  splunk_hec_url="http://127.0.0.1:18088/services/collector"
  echo "Local-only mode selected. Cloud and HEC prompts are skipped."
else
  if [[ -z "${realm}" ]]; then
    read -r -p "Splunk Observability realm (for example us1 or eu0): " realm
  fi

  if [[ -z "${realm}" ]]; then
    echo "A Splunk Observability realm is required in cloud mode." >&2
    echo "Rerun setup and answer y to the local-only prompt to work locally." >&2
    exit 1
  fi

  if [[ -z "${splunk_access_token}" ]]; then
    read -r -s -p "SPLUNK_ACCESS_TOKEN (Observability ingest token): " splunk_access_token
    echo
  fi
  if [[ -z "${splunk_access_token}" ]]; then
    echo "A Splunk Observability ingest token is required in cloud mode." >&2
    echo "Rerun setup and answer y to the local-only prompt to work locally." >&2
    exit 1
  fi

  default_api_url="https://api.${realm}.observability.splunkcloud.com"
  default_ingest_url="https://ingest.${realm}.observability.splunkcloud.com"
  if [[ -z "${splunk_api_url}" ]]; then
    read -r -p "SPLUNK_API_URL [${default_api_url}]: " splunk_api_url
    splunk_api_url="${splunk_api_url:-${default_api_url}}"
  fi

  if [[ -z "${splunk_ingest_url}" ]]; then
    splunk_ingest_url="${default_ingest_url}"
  fi

  if [[ -z "${splunk_hec_token}" ]]; then
    read -r -s -p "Optional SPLUNK_HEC_TOKEN for a non-production Splunk HEC (Enter to skip): " splunk_hec_token
    echo
  fi
  if [[ -z "${splunk_hec_url}" ]]; then
    read -r -p "Optional SPLUNK_HEC_URL, including /services/collector (Enter to skip): " splunk_hec_url
  fi

  if [[ -z "${splunk_hec_token}" || -z "${splunk_hec_url}" ]]; then
    hec_enabled=false
    # Valid local placeholders let the default logs pipeline start. The local
    # debug and file exporters still work; the HEC exporter can be configured as
    # a take-home exercise with a non-production Splunk instance.
    splunk_hec_token="not-configured"
    splunk_hec_url="http://127.0.0.1:18088/services/collector"
    echo "Splunk HEC is not configured. Use the local log exporters during the workshop."
  fi
fi

mkdir -p "${agent_dir}"
config_url="https://github.com/${repo_owner}/${repo_name}/raw/refs/heads/${repo_ref}/${content_path}/agent_config.yaml"
curl -fL --retry 3 "${config_url}" -o "${config_path}"

{
  printf 'export REALM=%q\n' "${realm}"
  printf 'export ACCESS_TOKEN=%q\n' "${splunk_access_token}"
  printf 'export SPLUNK_ACCESS_TOKEN=%q\n' "${splunk_access_token}"
  printf 'export SPLUNK_API_URL=%q\n' "${splunk_api_url}"
  printf 'export SPLUNK_HEC_TOKEN=%q\n' "${splunk_hec_token}"
  printf 'export SPLUNK_HEC_URL=%q\n' "${splunk_hec_url}"
  printf 'export SPLUNK_INGEST_URL=%q\n' "${splunk_ingest_url}"
  printf 'export SPLUNK_LISTEN_INTERFACE=%q\n' "${splunk_listen_interface}"
  printf 'export SPLUNK_MEMORY_LIMIT_MIB=%q\n' "${splunk_memory_limit_mib}"
  printf 'export CONF2026_LOCAL_ONLY=%q\n' "${local_only}"
  printf 'export CONF2026_CLOUD_ENABLED=%q\n' "${cloud_enabled}"
  printf 'export CONF2026_HEC_ENABLED=%q\n' "${hec_enabled}"
} > "${environment_path}"
chmod 600 "${environment_path}"
unset splunk_access_token splunk_hec_token
trap - ERR

echo
echo "Workshop environment setup complete."
echo "Collector version: ${collector_version}"
echo "Collector mode: agent"
echo "Local-only mode: ${local_only}"
echo
echo "Directory structure:"
echo "  1-agent/"
echo "    └── agent_config.yaml"
echo "  loadgen"
echo "  otelcol"
echo "  setup-workshop.sh"
echo "  workshop-env.sh"
echo
echo "Observability Cloud export enabled: ${cloud_enabled}"
echo "Splunk HEC export enabled: ${hec_enabled}"
echo "Local debug and file exporters are enabled for every hands-on exercise."
echo "Start the Agent with:"
echo "  cd 1-agent"
echo "  source ../workshop-env.sh"
echo "  ../otelcol --config=agent_config.yaml"
