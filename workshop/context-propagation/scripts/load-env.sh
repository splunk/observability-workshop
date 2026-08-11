#!/usr/bin/env bash
# Shared .env loader for workshop scripts.
# Source after ROOT_DIR is set: source "${ROOT_DIR}/scripts/load-env.sh"

load_env() {
  local env_file="${1:?env file path required}"

  if [[ ! -f "${env_file}" ]]; then
    return 0
  fi

  if ! bash -n "${env_file}" 2>/dev/null; then
    echo "Warning: ${env_file} has shell syntax errors — skipping file, using exported environment variables." >&2
    echo "  Inspect: sed -n '1,20p' \"${env_file}\" | cat -A" >&2
    echo "  Common fixes: remove angle brackets around tokens, close open quotes, run: dos2unix .env" >&2
    return 0
  fi

  set -a
  # shellcheck disable=SC1090
  source "${env_file}"
  set +a
}
