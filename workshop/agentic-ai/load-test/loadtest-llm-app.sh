#!/usr/bin/env bash
set -euo pipefail
#set -x   # prints each command as it runs

usage() {
  cat <<'EOF'
Usage:
  ./loadtest-llm-app.sh --cluster-api URL --password PASS [options]

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
  local namespace="workshop-participant-${i}" # Adjust if your naming convention differs
  local password="$PASSWORD"
  local cluster_api="$CLUSTER_API"

  local kubeconfig
  kubeconfig="$(mktemp)"
  trap 'rm -f "$kubeconfig"' RETURN

  echo "[$user] login..."
  KUBECONFIG="$kubeconfig" oc login "$cluster_api" -u "$user" -p "$password" --request-timeout=30s

  echo "[$user] applying application manifest..."
  KUBECONFIG="$kubeconfig" oc apply -f ../llm-app/k8s-manifest.yaml

  echo "[$user] waiting for app readiness..."
  KUBECONFIG="$kubeconfig" oc rollout status deploy/llm-app --timeout=5m

  # wait for the llm-app to startup
  sleep 120

  echo "[$user] Running curl test inside the cluster..."

  # 1. Create the Pod using a Heredoc
  cat <<EOF | KUBECONFIG="$kubeconfig" oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: curl-test-pod
  namespace: ${namespace}
spec:
  containers:
  - name: curl-container
    image: curlimages/curl:latest
    command: ["/bin/sh", "-c"]
    args:
      - |
        set -e
        echo "DNS:"; nslookup llm-app || true
        echo "Waiting for service..."
        curl --fail --show-error --silent \
          --connect-timeout 2 \
          --retry 30 --retry-delay 2 --retry-all-errors \
          -X POST "http://llm-app:8080/askquestion" \
          -H "Accept: application/json" \
          -H "Content-Type: application/json" \
          -d '{"question":"How much memory does the NVIDIA H200 have?"}'
    resources:
      limits:
        cpu: "50m"
        memory: "100Mi"
      requests:
        cpu: "50m"
        memory: "100Mi"
  restartPolicy: Never
EOF

  # 2. Wait for the pod to actually start running
  KUBECONFIG="$kubeconfig" oc wait --for=condition=Ready pod/curl-test-pod --timeout=60s > /dev/null 2>&1

  # 3. Stream the logs (this shows the actual API response)
  echo "[$user] Response from LLM App:"
  KUBECONFIG="$kubeconfig" oc logs -f curl-test-pod

  # 4. Cleanup the test pod
  KUBECONFIG="$kubeconfig" oc delete pod curl-test-pod --wait=false > /dev/null 2>&1

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