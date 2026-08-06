#!/usr/bin/env bash
set -euo pipefail

# Use as EC2 user data or run as root on a clean Amazon Linux 2023/Ubuntu host.
# Do not add Observability Cloud tokens here. Attendees export their own token
# after they connect.

repo_url="${WORKSHOP_REPO_URL:-https://github.com/splunk/observability-workshop.git}"
repo_ref="${WORKSHOP_REPO_REF:-main}"
repo_dir="${WORKSHOP_REPO_DIR:-/opt/observability-workshop}"
lab_dir="${WORKSHOP_DIR:-/opt/advanced-collector-delta}"

if command -v dnf >/dev/null 2>&1; then
  dnf install -y git curl
elif command -v yum >/dev/null 2>&1; then
  yum install -y git curl
elif command -v apt-get >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y git curl ca-certificates
else
  echo "Supported package manager not found." >&2
  exit 1
fi

if [[ ! -d "${repo_dir}/.git" ]]; then
  git clone --branch "${repo_ref}" --depth 1 "${repo_url}" "${repo_dir}"
fi

WORKSHOP_DIR="${lab_dir}" "${repo_dir}/workshop/ninja/advanced-otel/setup-workshop.sh" --ec2

login_user="ec2-user"
if id ubuntu >/dev/null 2>&1; then
  login_user="ubuntu"
fi
chown -R "${login_user}:${login_user}" "${lab_dir}"

echo "Single-agent workshop environment ready for ${login_user} in ${lab_dir}."
