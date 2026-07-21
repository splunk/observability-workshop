#!/usr/bin/env bash
set -euo pipefail
# set -x

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-install-app.sh --csv FILE --galileo-api-key KEY [options]

Required:
  --csv FILE
  --galileo-api-key KEY

Options:
  --max-parallel N              (default: 10)
  --ssh-timeout SECONDS         (default: 30)
  --insecure-hostkey            (disable strict host key checking)
EOF
}

# Defaults
CSV_FILE=""
GALILEO_API_KEY=""
MAX_PARALLEL=10
SSH_TIMEOUT=30
INSECURE_HOSTKEY="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv) CSV_FILE="$2"; shift 2 ;;
    --galileo-api-key) GALILEO_API_KEY="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    --ssh-timeout) SSH_TIMEOUT="$2"; shift 2 ;;
    --insecure-hostkey) INSECURE_HOSTKEY="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$CSV_FILE" || -z "$GALILEO_API_KEY" ]]; then
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
  local ssh="$3"

  local ssh_user ssh_host ssh_port
  ssh_port=2222
  ssh_user="splunk"

  # Extract ssh host from ssh -p 2222 splunk@<ip address>
  ssh_host="$(awk '{print $NF}' <<< "$ssh")"   # last token
  ssh_host="${ssh_host#*@}"                       # remove user@

  echo "[row $rownum] Connecting to ${ssh_user}@${ssh_host}:${ssh_port}"

  set -x

  sshpass -p "$sshPassword" \
    ssh "${SSH_OPTS[@]}" -p "$ssh_port" "${ssh_user}@${ssh_host}" \
    PARTICIPANT_NUMBER="$rownum" \
    GALILEO_API_KEY="$GALILEO_API_KEY" \
    'bash -s' <<'REMOTE_EOF'
set -x
set -euo pipefail

echo "INSTANCE=${INSTANCE:-<unset>}"

kubectl create secret generic openai-api \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  --from-literal=openai-api-endpoint="$OPENAI_BASE_URL"

cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f healthcare-assistant-config.yaml

cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f postgres.yaml

cd ~/workshop/healthcare-assistant
docker build -f 4-app-with-controls/Dockerfile -t localhost:9999/healthcare-assistant:app-with-controls .
docker push localhost:9999/healthcare-assistant:app-with-controls

cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f setup-job.yaml

export GALILEO_CONSOLE_URL="https://console.multitenant.galileocloud.io"

kubectl create secret generic galileo-secret \
  --from-literal=GALILEO_API_KEY="$GALILEO_API_KEY"

kubectl create configmap galileo-config \
  --from-literal=GALILEO_CONSOLE_URL="$GALILEO_CONSOLE_URL" \
  --from-literal=GALILEO_PROJECT="project-$PARTICIPANT_NUMBER" \
  --from-literal=GALILEO_LOG_STREAM="default"

kubectl create configmap galileo-agent-control-config \
  --from-literal=GALILEO_API_URL="https://api.multitenant.galileocloud.io" \
  --from-literal=AGENT_CONTROL_URL="https://console.multitenant.galileocloud.io/api/agent-control" \
  --from-literal=AGENT_CONTROL_AGENT_NAME="agent-control-example" \
  --from-literal=AGENT_CONTROL_API_KEY_HEADER="Galileo-API-Key" \
  --from-literal=AGENT_CONTROL_RUNTIME_AUTH_MODE="jwt" \
  --from-literal=AGENT_CONTROL_TARGET_TYPE="log_stream"

cd ~/workshop/healthcare-assistant/4-app-with-controls
kubectl apply -f k8s.yaml

echo "Waiting for application pods to be ready on $(hostname)"

kubectl wait --for=condition=Ready pod --all --timeout=10m

echo "Application pods are ready on ${INSTANCE}"

REMOTE_EOF

  echo "[row $rownum] done"
}

declare -a pids=()
fail=0

# Read CSV (skip header), expected columns:
# adminUsername,sshPass,sshUrl,sshPassword,ssh,o11yCloudID,url,adminPassword
rownum=0
while IFS=, read -r adminUsername sshPass sshUrl sshPassword ssh o11yCloudID url adminPassword; do
  rownum=$((rownum + 1))

  # Basic validation / skip incomplete rows
  if [[ -z "${ssh:-}" || -z "${sshPassword:-}" ]]; then
    echo "[row $rownum] skipping: missing ssh or sshPassword"
    continue
  fi

  run_for_row "$rownum" "$sshPassword" "$ssh" &
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
  echo "One or more remote app installs FAILED."
  exit 1
fi

echo "All remote app installs completed successfully."