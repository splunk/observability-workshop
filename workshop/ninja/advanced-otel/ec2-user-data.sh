#!/usr/bin/env bash
set -euo pipefail

# Use as EC2 user data or run as root on a clean Amazon Linux 2023/Ubuntu host.
# It stages binaries only. Never put an attendee token in user data or an AMI.

collector_version="0.157.0"
repo_url="${WORKSHOP_REPO_URL:-https://github.com/chentaow-splunk/observability-workshop.git}"
repo_ref="${WORKSHOP_REPO_REF:-codex/advanced-collector-conf2026}"
repo_dir="${WORKSHOP_REPO_DIR:-/opt/observability-workshop}"

if command -v dnf >/dev/null 2>&1; then
  dnf install -y git curl jq
elif command -v yum >/dev/null 2>&1; then
  yum install -y git curl jq
elif command -v apt-get >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y git curl jq ca-certificates
else
  echo "Supported package manager not found." >&2
  exit 1
fi

if [[ ! -d "${repo_dir}/.git" ]]; then
  git clone --branch "${repo_ref}" --depth 1 "${repo_url}" "${repo_dir}"
fi

login_user="ec2-user"
if id ubuntu >/dev/null 2>&1; then
  login_user="ubuntu"
fi
lab_dir="${WORKSHOP_DIR:-/home/${login_user}/advanced-otel-workshop}"

case "$(uname -m)" in
  x86_64|amd64)
    collector_asset="otelcol_linux_amd64"
    loadgen_asset="loadgen-linux-amd64"
    ;;
  aarch64|arm64)
    collector_asset="otelcol_linux_arm64"
    loadgen_asset="loadgen-linux-arm64"
    ;;
  *)
    echo "Unsupported architecture: $(uname -m)" >&2
    exit 1
    ;;
esac

mkdir -p "${lab_dir}"
curl -fL --retry 3 \
  "https://github.com/signalfx/splunk-otel-collector/releases/download/v${collector_version}/${collector_asset}" \
  -o "${lab_dir}/otelcol"
install -m 0755 \
  "${repo_dir}/workshop/ninja/advanced-otel/loadgen/build/${loadgen_asset}" \
  "${lab_dir}/loadgen"
install -m 0755 \
  "${repo_dir}/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/setup-workshop-conf2026.sh" \
  "${lab_dir}/setup-workshop.sh"
chmod 0755 "${lab_dir}/otelcol"
chown -R "${login_user}:${login_user}" "${lab_dir}"

echo "Workshop files are ready for ${login_user} in ${lab_dir}."
echo "After signing in: cd ~/advanced-otel-workshop && ./setup-workshop.sh"
