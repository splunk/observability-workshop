#!/usr/bin/env bash
set -euo pipefail
# set -x

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-install-app.sh --csv FILE --azure-openai-key KEY --ai-defense-url URL [options]

Required:
  --csv FILE
  --azure-openai-key TOKEN
  --ai-defense-url URL

Options:
  --max-parallel N              (default: 10)
  --ssh-timeout SECONDS         (default: 30)
  --insecure-hostkey            (disable strict host key checking)
EOF
}

# Defaults
CSV_FILE=""
AZURE_OPENAI_KEY=""
AI_DEFENSE_URL=""
MAX_PARALLEL=10
SSH_TIMEOUT=30
INSECURE_HOSTKEY="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv) CSV_FILE="$2"; shift 2 ;;
    --azure-openai-key) AZURE_OPENAI_KEY="$2"; shift 2 ;;
    --ai-defense-url) AI_DEFENSE_URL="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    --ssh-timeout) SSH_TIMEOUT="$2"; shift 2 ;;
    --insecure-hostkey) INSECURE_HOSTKEY="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$CSV_FILE" || -z "$AZURE_OPENAI_KEY" || -z "$AI_DEFENSE_URL" ]]; then
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
    AZURE_OPENAI_KEY="$AZURE_OPENAI_KEY" \
    AI_DEFENSE_URL="$AI_DEFENSE_URL" \
    'bash -s' <<'REMOTE_EOF'
set -x
set -euo pipefail

echo "INSTANCE=${INSTANCE:-<unset>}"

kubectl create ns travel-agent

kubectl create secret generic azure-openai-api -n travel-agent --from-literal=azure-openai-api-key=$AZURE_OPENAI_KEY
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-gateway-url=$AI_DEFENSE_URL

kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent

cd /home/splunk/workshop/agentic-ai/app-with-security-risk

kubectl apply -f /home/splunk/workshop/agentic-ai/app-with-security-risk/k8s.yaml

echo "Waiting for application pods to be ready on $(hostname)"

kubectl -n travel-agent wait --for=condition=Ready pod --all --timeout=10m

echo "Application pods are ready on ${INSTANCE}"
echo "Sending test request on ${INSTANCE}"

echo "Install complete on ${INSTANCE}"
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
  echo "One or more remote app installs FAILED."
  exit 1
fi

echo "All remote app installs completed successfully."