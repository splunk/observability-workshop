#!/usr/bin/env bash
set -euo pipefail
#set -x   # prints each command as it runs

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-uninstall-collector.sh --access-token TOKEN --hec-url URL --hec-token TOKEN --cluster-api URL --password PASS [options]

Required:
  --access-token TOKEN
  --hec-url URL
  --hec-token TOKEN
  --cluster-api URL
  --password PASS

Options:
  --realm REALM                 (default: us1)
  --splunk-index INDEX          (default: splunk4rookies-workshop)
  --users N                     (default: 30)
  --max-parallel N              (default: 10)
  --values FILE                 (default: ../otel-collector/otel-collector-values-with-portworx.yaml)
  --chart PATH                  (default: splunk-otel-collector-chart/splunk-otel-collector)
EOF
}

# Defaults
SPLUNK_INDEX="splunk4rookies-workshop"
REALM="us1"
USERS=30
MAX_PARALLEL=10
VALUES_FILE="../otel-collector/otel-collector-values-with-portworx.yaml"
CHART="splunk-otel-collector-chart/splunk-otel-collector"

ACCESS_TOKEN=""
HEC_URL=""
HEC_TOKEN=""
PASSWORD=""
CLUSTER_API=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --splunk-index) SPLUNK_INDEX="$2"; shift 2 ;;
    --access-token) ACCESS_TOKEN="$2"; shift 2 ;;
    --realm) REALM="$2"; shift 2 ;;
    --hec-url) HEC_URL="$2"; shift 2 ;;
    --hec-token) HEC_TOKEN="$2"; shift 2 ;;
    --password) PASSWORD="$2"; shift 2 ;;
    --cluster-api) CLUSTER_API="$2"; shift 2 ;;
    --users) USERS="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    --values) VALUES_FILE="$2"; shift 2 ;;
    --chart) CHART="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

# Validate required args
if [[ -z "$ACCESS_TOKEN" || -z "$HEC_URL" || -z "$HEC_TOKEN" || -z "$PASSWORD" || -z "$CLUSTER_API" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 2
fi

install_for_user () {
  local i="$1"
  local user="participant${i}"
  local namespace="workshop-participant-${i}"
  local cluster_name="ai-pod-${namespace}"
  local environment_name="ai-pod-${namespace}"
  local release="splunk-otel-collector"

  local kubeconfig
  kubeconfig="$(mktemp)"
  trap 'rm -f "$kubeconfig"' RETURN

  echo "[$user] login..."
  KUBECONFIG="$kubeconfig" oc login "$CLUSTER_API" -u "$user" -p "$PASSWORD" --request-timeout=30s
  echo "[$user] logged in as: $(KUBECONFIG="$kubeconfig" oc whoami)"

  echo "[$user] helm uninstall..."
  KUBECONFIG="$kubeconfig" helm uninstall "$release"

  echo "[$user] done"
}

# Throttle parallelism
for i in $(seq 1 "$USERS"); do
  install_for_user "$i" &
  while (( $(jobs -pr | wc -l) >= MAX_PARALLEL )); do
    sleep 0.5
  done
done

wait
echo "All installs completed and pods are Ready."