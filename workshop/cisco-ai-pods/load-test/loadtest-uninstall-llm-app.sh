#!/usr/bin/env bash
set -euo pipefail
#set -x   # prints each command as it runs

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-uninstall-llm-app.sh --cluster-api URL --password PASS [options]

Required:
  --cluster-api URL
  --password PASS

Options:
  --users N                     (default: 30)
  --max-parallel N              (default: 10)
EOF
}

# Defaults
USERS=30
MAX_PARALLEL=10

PASSWORD=""
CLUSTER_API=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --password) PASSWORD="$2"; shift 2 ;;
    --cluster-api) CLUSTER_API="$2"; shift 2 ;;
    --users) USERS="$2"; shift 2 ;;
    --max-parallel) MAX_PARALLEL="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

# Validate required args
if [[ -z "$PASSWORD" || -z "$CLUSTER_API" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 2
fi

install_for_user () {
  local i="$1"
  local user="participant${i}"

  local kubeconfig
  kubeconfig="$(mktemp)"
  trap 'rm -f "$kubeconfig"' RETURN

  echo "[$user] login..."
  KUBECONFIG="$kubeconfig" oc login "$CLUSTER_API" -u "$user" -p "$PASSWORD" --request-timeout=30s
  echo "[$user] logged in as: $(KUBECONFIG="$kubeconfig" oc whoami)"

  echo "[$user] oc delete -f ../llm-app/k8s-manifest.yaml"
  KUBECONFIG="$kubeconfig" oc delete -f ../llm-app/k8s-manifest.yaml

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
echo "Applications are installed and curl test was completed."