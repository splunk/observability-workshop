#!/usr/bin/env bash
set -euo pipefail
# set -x

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-build-app.sh --csv FILE [options]

Required:
  --csv FILE

Options:
  --max-parallel N              (default: 10)
  --ssh-timeout SECONDS         (default: 30)
  --insecure-hostkey            (disable strict host key checking)
EOF
}

# Defaults
CSV_FILE=""
MAX_PARALLEL=10
SSH_TIMEOUT=30
INSECURE_HOSTKEY="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv) CSV_FILE="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    --ssh-timeout) SSH_TIMEOUT="$2"; shift 2 ;;
    --insecure-hostkey) INSECURE_HOSTKEY="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$CSV_FILE" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 2
fi

if ! command -v sshpass >/dev/null 2>&1; then
  echo "ERROR: sshpass is required for password-based SSH." >&2
  exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
  echo "ERROR: CSV file not found: $CSV_FILE" >&2
  exit 1
fi

SSH_OPTS=(-o ConnectTimeout="$SSH_TIMEOUT")
if [[ "$INSECURE_HOSTKEY" == "true" ]]; then
  SSH_OPTS+=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
fi

run_for_row() {
  local rownum="$1"
  local sshPassword="$2"
  local sshCmd="$3"

  local ssh_user ssh_host ssh_port
  ssh_port=2222
  ssh_user="splunk"

  # Extract ssh host from ssh -p 2222 splunk@<ip address>
  ssh_host="$(awk '{print $NF}' <<< "$sshCmd")"   # last token
  ssh_host="${ssh_host#*@}"                       # remove user@

  echo "[row $rownum] Connecting to ${ssh_user}@${ssh_host}:${ssh_port}"

  set -x

  sshpass -p "$sshPassword" \
    ssh "${SSH_OPTS[@]}" -p "$ssh_port" "${ssh_user}@${ssh_host}" \
    'bash -s' <<'REMOTE_EOF'
set -x
set -euo pipefail

echo "INSTANCE=${INSTANCE:-<unset>}"

echo "Building app on ${INSTANCE}"

cd /home/splunk/workshop/agentic-ai/app-with-security-risk

docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk

echo "App build complete on ${INSTANCE}"
REMOTE_EOF

  echo "[row $rownum] done"
}

declare -a pids=()
fail=0

# Read CSV (skip header), expected columns:
# adminUsername,sshPass,sshUrl,sshPassword,ssh,o11yCloudID,url,adminPassword
rownum=0
while IFS=, read -r adminUsername sshPass sshUrl sshPassword sshCmd o11yCloudID url adminPassword; do
  rownum=$((rownum + 1))

  # Basic validation / skip incomplete rows
  if [[ -z "${sshCmd:-}" || -z "${sshPassword:-}" ]]; then
    echo "[row $rownum] skipping: missing sshCmd or sshPassword"
    continue
  fi

  run_for_row "$rownum" "$sshPassword" "$sshCmd" &
  pids+=("$!")

  while (( $(jobs -pr | wc -l) >= MAX_PARALLEL )); do
    sleep 0.5
  done
done < <(tail -n +2 "$CSV_FILE")

for pid in "${pids[@]:-}"; do
  [[ -n "$pid" ]] || continue
  if ! wait "$pid"; then
    fail=1
  fi
done

if (( fail )); then
  echo "One or more remote app builds FAILED."
  exit 1
fi

echo "All remote app builds completed successfully."