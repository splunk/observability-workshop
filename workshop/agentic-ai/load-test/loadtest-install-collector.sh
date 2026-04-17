#!/usr/bin/env bash
set -euo pipefail
# set -x

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-install-collector.sh --csv FILE --access-token TOKEN --hec-url URL --hec-token TOKEN [options]

Required:
  --csv FILE
  --access-token TOKEN
  --hec-url URL
  --hec-token TOKEN

Options:
  --realm REALM                 (default: us1)
  --splunk-index INDEX          (default: splunk4rookies-workshop)
  --max-parallel N              (default: 10)
  --chart REF                   (default: splunk-otel-collector/splunk-otel-collector)
  --namespace NS                (default: default)
  --release NAME                (default: splunk-otel-collector)
  --ssh-timeout SECONDS         (default: 30)
  --insecure-hostkey            (disable strict host key checking)
EOF
}

# Defaults
CSV_FILE=""
ACCESS_TOKEN=""
HEC_URL=""
HEC_TOKEN=""
REALM="us1"
SPLUNK_INDEX="splunk4rookies-workshop"
MAX_PARALLEL=10
CHART="splunk-otel-collector-chart/splunk-otel-collector"
NAMESPACE="default"
RELEASE="splunk-otel-collector"
SSH_TIMEOUT=30
INSECURE_HOSTKEY="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv) CSV_FILE="$2"; shift 2 ;;
    --access-token) ACCESS_TOKEN="$2"; shift 2 ;;
    --hec-url) HEC_URL="$2"; shift 2 ;;
    --hec-token) HEC_TOKEN="$2"; shift 2 ;;
    --realm) REALM="$2"; shift 2 ;;
    --splunk-index) SPLUNK_INDEX="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    --chart) CHART="$2"; shift 2 ;;
    --namespace) NAMESPACE="$2"; shift 2 ;;
    --release) RELEASE="$2"; shift 2 ;;
    --ssh-timeout) SSH_TIMEOUT="$2"; shift 2 ;;
    --insecure-hostkey) INSECURE_HOSTKEY="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$CSV_FILE" || -z "$ACCESS_TOKEN" || -z "$HEC_URL" || -z "$HEC_TOKEN" ]]; then
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
    ACCESS_TOKEN="$ACCESS_TOKEN" \
    HEC_URL="$HEC_URL" \
    HEC_TOKEN="$HEC_TOKEN" \
    REALM="$REALM" \
    SPLUNK_INDEX="$SPLUNK_INDEX" \
    CHART="$CHART" \
    NAMESPACE="$NAMESPACE" \
    RELEASE="$RELEASE" \
    'bash -s' <<'REMOTE_EOF'
set -x
set -euo pipefail

echo "INSTANCE=${INSTANCE:-<unset>}"

echo "Remote host: $(hostname)"
kubectl version --client >/dev/null
helm version >/dev/null

# Optional: ensure namespace exists
kubectl get ns "$NAMESPACE" >/dev/null 2>&1 || kubectl create ns "$NAMESPACE"

helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update

cat <<EOF > values.yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
EOF

helm upgrade --install "$RELEASE" \
  --set "clusterName=${INSTANCE}-cluster" \
  --set "environment=agentic-ai-${INSTANCE}" \
  --set "splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set "splunkObservability.realm=$REALM" \
  --set "splunkPlatform.endpoint=$HEC_URL" \
  --set "splunkPlatform.token=$HEC_TOKEN" \
  --set "splunkPlatform.index=$SPLUNK_INDEX" \
  -f "./values.yaml" \
  "$CHART"

kubectl -n "$NAMESPACE" rollout status ds/splunk-otel-collector-agent --timeout=10m
kubectl -n "$NAMESPACE" wait --for=condition=Ready pod --all --timeout=10m
echo "Install complete on $(hostname)"
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
  echo "One or more remote installs FAILED."
  exit 1
fi

echo "All remote installs completed successfully."