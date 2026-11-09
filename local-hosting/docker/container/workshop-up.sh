#!/bin/bash
# Bring up the same k3d workshop environment cloud-init builds on EC2.
# The container entrypoint starts the inner Docker engine, then runs this
# script as splunk. Workshop tokens are fetched at start from SWIPE_ID and
# written only to mode-600 files under /home/splunk. They are not part of the image.

set -euo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

INSTANCE="${INSTANCE:-workshop}"
CLUSTER_NAME="${CLUSTER_NAME:-${INSTANCE}-cluster}"
WORKSHOP_AGENTS="${WORKSHOP_AGENTS:-2}"
WORKSHOP_NODE_MEMORY="${WORKSHOP_NODE_MEMORY:-8G}"
K3S_IMAGE="${K3S_IMAGE:-rancher/k3s:v1.33.4-k3s1}"
HOME_DIR="/home/splunk"
export INSTANCE CLUSTER_NAME WORKSHOP_AGENTS WORKSHOP_NODE_MEMORY K3S_IMAGE
export KUBECONFIG="${KUBECONFIG:-${HOME_DIR}/.kube/config}"
export HOME="${HOME_DIR}"

if [ "$(id -un)" != "splunk" ]; then
    echo "Run workshop-up.sh as splunk." >&2
    exit 1
fi

if [[ ! "${INSTANCE}" =~ ^[a-z][a-z0-9-]{0,30}$ ]]; then
    echo "INSTANCE must be a short lowercase name." >&2
    exit 1
fi
if [[ ! "${CLUSTER_NAME}" =~ ^[a-z0-9][a-z0-9-]{0,40}$ ]]; then
    echo "CLUSTER_NAME must be a lowercase cluster name." >&2
    exit 1
fi
if [[ ! "${WORKSHOP_AGENTS}" =~ ^[0-9]+$ ]] || [ "${WORKSHOP_AGENTS}" -gt 10 ]; then
    echo "WORKSHOP_AGENTS must be a whole number from 0 to 10." >&2
    exit 1
fi
if [[ ! "${WORKSHOP_NODE_MEMORY}" =~ ^[1-9][0-9]{0,3}[MG]$ ]]; then
    echo "WORKSHOP_NODE_MEMORY must look like 8G or 512M." >&2
    exit 1
fi
if [[ ! "${K3S_IMAGE}" =~ ^[A-Za-z0-9][A-Za-z0-9._:/-]{0,180}$ ]]; then
    echo "K3S_IMAGE is not a usable image reference." >&2
    exit 1
fi

wait_for_docker() {
    local attempt
    echo "Waiting for Docker."
    for attempt in $(seq 1 60); do
        if docker info >/dev/null 2>&1; then
            return 0
        fi
        sleep 2
    done
    echo "Docker did not become ready." >&2
    return 1
}

raise_inotify_limits() {
    local setting
    for setting in fs.inotify.max_user_watches=524288 fs.inotify.max_user_instances=8192; do
        if ! sudo sysctl -w "${setting}" >/dev/null 2>&1; then
            echo "Could not set ${setting}. k3d may run out of inotify watches." >&2
        fi
    done
}

start_rsyslog() {
    sudo touch /var/log/syslog /var/log/auth.log
    # Ubuntu rsyslog drops to the syslog user and cannot open root-owned files.
    if getent passwd syslog >/dev/null && getent group adm >/dev/null; then
        sudo chown syslog:adm /var/log/syslog /var/log/auth.log
        sudo chmod 640 /var/log/syslog /var/log/auth.log
    else
        sudo chmod 644 /var/log/syslog /var/log/auth.log
    fi
    if pgrep -x rsyslogd >/dev/null 2>&1; then
        return 0
    fi
    sudo rm -f /run/rsyslogd.pid /var/run/rsyslogd.pid
    if ! sudo rsyslogd; then
        echo "rsyslog did not start. The cluster still mounts the log files." >&2
    fi
}

install_content() {
    local ready="${HOME_DIR}/.workshop-content-ready"
    local workshop_zip content_zip
    if [ -f "${ready}" ]; then
        echo "Workshop content is already present."
        return 0
    fi
    echo "Downloading workshop content."
    rm -rf \
        "${HOME_DIR}/observability-workshop-main" \
        "${HOME_DIR}/workshop" \
        "${HOME_DIR}/observability-content-contrib-main" \
        "${HOME_DIR}/observability-content-contrib"
    workshop_zip="$(mktemp)"
    curl -fsSL --retry 3 --retry-delay 2 -o "${workshop_zip}" \
        https://github.com/splunk/observability-workshop/archive/main.zip
    unzip -qq "${workshop_zip}" -d "${HOME_DIR}"
    rm -f "${workshop_zip}"
    mkdir -p "${HOME_DIR}/workshop"
    mv "${HOME_DIR}/observability-workshop-main/workshop/"* "${HOME_DIR}/workshop"
    mv "${HOME_DIR}/workshop/ansible/diab-"*.yml "${HOME_DIR}"
    rm -rf "${HOME_DIR}/observability-workshop-main"
    rm -rf "${HOME_DIR}/workshop/aws" "${HOME_DIR}/workshop/cloud-init" "${HOME_DIR}/workshop/ansible"
    mv "${HOME_DIR}/workshop/k3s/demo-in-a-box.zip" "${HOME_DIR}"
    content_zip="$(mktemp)"
    curl -fsSL --retry 3 --retry-delay 2 -o "${content_zip}" \
        https://github.com/splunk/observability-content-contrib/archive/main.zip
    unzip -qq "${content_zip}" -d "${HOME_DIR}"
    rm -f "${content_zip}"
    mv "${HOME_DIR}/observability-content-contrib-main" "${HOME_DIR}/observability-content-contrib"
    touch "${ready}"
}

create_cluster() {
    local -a args
    echo "Creating cluster ${CLUSTER_NAME}."
    args=(
        cluster create "${CLUSTER_NAME}"
        --image "${K3S_IMAGE}"
        --timeout 10m
        --servers 1
        --agents "${WORKSHOP_AGENTS}"
        --servers-memory "${WORKSHOP_NODE_MEMORY}"
        --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@server:0"
        --k3s-arg "--kubelet-arg=container-log-max-size=10Mi@server:*"
        --k3s-arg "--kubelet-arg=container-log-max-files=5@server:*"
        --port "81:80@loadbalancer"
        --port "82:82@loadbalancer"
        --port "9999:9999@loadbalancer"
        --port "443:443@loadbalancer"
    )
    if [ "${WORKSHOP_AGENTS}" -gt 0 ]; then
        args+=(
            --agents-memory "${WORKSHOP_NODE_MEMORY}"
            --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@agent:*"
            --k3s-arg "--kubelet-arg=container-log-max-size=10Mi@agent:*"
            --k3s-arg "--kubelet-arg=container-log-max-files=5@agent:*"
            -v "${HOME_DIR}:${HOME_DIR}@server:*;agent:*"
            -v "/var/log/syslog:/var/log/syslog@server:*;agent:*"
            -v "/var/log/auth.log:/var/log/auth.log@server:*;agent:*"
        )
    else
        args+=(
            -v "${HOME_DIR}:${HOME_DIR}@server:*"
            -v "/var/log/syslog:/var/log/syslog@server:*"
            -v "/var/log/auth.log:/var/log/auth.log@server:*"
        )
    fi
    if ! k3d "${args[@]}"; then
        echo "Cluster create failed. Removing a partial cluster so the next start can retry." >&2
        k3d cluster delete "${CLUSTER_NAME}" || true
        exit 1
    fi
}

ensure_cluster() {
    if k3d cluster get "${CLUSTER_NAME}" >/dev/null 2>&1; then
        echo "Starting cluster ${CLUSTER_NAME}."
        k3d cluster start "${CLUSTER_NAME}"
        return 0
    fi
    create_cluster
}

write_kubeconfig() {
    local tmp
    mkdir -p "${HOME_DIR}/.kube"
    chmod 700 "${HOME_DIR}/.kube"
    tmp="$(mktemp "${HOME_DIR}/.kube/config.XXXXXX")"
    k3d kubeconfig get "${CLUSTER_NAME}" > "${tmp}"
    # k3d records a host-facing address. kubectl runs in this container,
    # where the API port is published on localhost.
    sed -i \
        -e 's/host\.docker\.internal/127.0.0.1/g' \
        -e 's/0\.0\.0\.0/127.0.0.1/g' \
        "${tmp}"
    chmod 400 "${tmp}"
    # The installed config is mode 400, so the next start cannot open it
    # for writing. Replacing the directory entry avoids that.
    mv -f "${tmp}" "${KUBECONFIG}"
}

wait_for_nodes() {
    local attempt
    for attempt in $(seq 1 60); do
        if kubectl get nodes --no-headers 2>/dev/null | grep -q .; then
            kubectl wait --for=condition=Ready node --all --timeout=600s
            return 0
        fi
        sleep 5
    done
    echo "Timed out waiting for nodes." >&2
    return 1
}

kubectl_apply() {
    local manifest="$1"
    local attempt
    for attempt in $(seq 1 30); do
        if kubectl apply -f "${manifest}"; then
            return 0
        fi
        echo "Kubernetes is not ready to apply ${manifest}. Retrying." >&2
        sleep 5
    done
    echo "Could not apply ${manifest}." >&2
    return 1
}

apply_registry() {
    local manifest="${HOME_DIR}/workshop/k3s/registry/registry.yaml"
    if [ ! -f "${manifest}" ]; then
        echo "Missing registry manifest: ${manifest}" >&2
        exit 1
    fi
    kubectl_apply "${manifest}"
    kubectl wait --for=condition=Ready pod -n kube-system -l k8s-app=kube-registry --timeout=5m
}

install_chaos_mesh() {
    if kubectl get namespace chaos-mesh >/dev/null 2>&1; then
        echo "Chaos Mesh is already installed."
        return 0
    fi
    echo "Installing Chaos Mesh v2.8.0."
    curl -fsSL --retry 3 --retry-delay 2 https://mirrors.chaos-mesh.org/v2.8.0/install.sh \
        | bash -s -- --k3s
}

apply_swipe_secret() {
    local swipe_error
    if [ -z "${SWIPE_ID:-}" ]; then
        echo "SWIPE_ID is unset. workshop-secret was not applied."
        return 0
    fi
    echo "Fetching the SWiPE workshop and applying workshop-secret."
    # The API body stays in this capture. The case below prints a fixed message.
    if ! swipe_error="$(python3 - 2>&1 <<'PY'
import json, os, pathlib, re, shlex, urllib.parse, urllib.request

swipe_id = os.environ.get("SWIPE_ID", "")
instance = os.environ["INSTANCE"]
home = pathlib.Path("/home/splunk")

if swipe_id == "" or any(ch.isspace() for ch in swipe_id):
    raise SystemExit("invalid")

url = "https://swipe.splunk.show/api?id=" + urllib.parse.quote(swipe_id)
try:
    with urllib.request.urlopen(url, timeout=30) as response:
        body = response.read().decode()
except Exception:
    raise SystemExit("unreachable") from None
try:
    data = json.loads(body)
except json.JSONDecodeError:
    raise SystemExit("unexpected") from None
if not isinstance(data, dict):
    raise SystemExit("unexpected")
if data.get("message") == "Workshop ID not found":
    raise SystemExit("notfound")

payload = {}
for key, value in data.items():
    if (
        not isinstance(key, str)
        or not isinstance(value, str)
        or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) is None
        or "\n" in value
        or "\r" in value
    ):
        raise SystemExit("unexpected")
    payload[key] = value
if not payload:
    raise SystemExit("unexpected")

aliases = {
    "RUM_TOKEN": payload.get("RUM", ""),
    "ACCESS_TOKEN": payload.get("INGEST", ""),
    "INGEST_TOKEN": payload.get("INGEST", ""),
    "API_TOKEN": payload.get("API", ""),
}
exports = [f"export {key}={shlex.quote(payload[key])}" for key in sorted(payload)]
exports.extend(f"export {key}={shlex.quote(value)}" for key, value in aliases.items())
env_path = home / ".workshop-env"
env_path.write_text("\n".join(exports) + "\n")
env_path.chmod(0o600)

def yaml_string(value):
    return json.dumps(value)

lines = [
    "apiVersion: v1",
    "kind: Secret",
    "metadata:",
    "  name: workshop-secret",
    "  namespace: default",
    "type: Opaque",
    "stringData:",
    f"  app: {yaml_string(instance + '-store')}",
    f"  env: {yaml_string(instance + '-workshop')}",
    f"  instance: {yaml_string(instance + '-workshop')}",
    f"  deployment: {yaml_string('deployment.environment=' + instance + '-workshop')}",
    f"  realm: {yaml_string(payload.get('REALM', ''))}",
    f"  ingest_token: {yaml_string(payload.get('INGEST', ''))}",
    f"  api_token: {yaml_string(payload.get('API', ''))}",
    f"  rum_token: {yaml_string(payload.get('RUM', ''))}",
    f"  hec_token: {yaml_string(payload.get('HEC_TOKEN', ''))}",
    f"  hec_url: {yaml_string(payload.get('HEC_URL', ''))}",
]
for key in sorted(payload):
    lines.append(f"  {key}: {yaml_string(payload[key])}")
lines.append(f"  url: {yaml_string('http://localhost:81')}")
secret_path = home / "workshop-secrets.yaml"
secret_path.write_text("\n".join(lines) + "\n")
secret_path.chmod(0o600)
PY
    )"; then
        swipe_error="${swipe_error//$'\n'/}"
        case "${swipe_error}" in
            notfound) echo "SWiPE ID was not found." >&2 ;;
            unreachable) echo "Could not reach the SWiPE API." >&2 ;;
            invalid) echo "SWIPE_ID is invalid." >&2 ;;
            *) echo "Unexpected SWiPE API response." >&2 ;;
        esac
        exit 1
    fi
    kubectl_apply "${HOME_DIR}/workshop-secrets.yaml"
}

wait_for_docker
raise_inotify_limits
start_rsyslog
install_content
ensure_cluster
write_kubeconfig
wait_for_nodes
apply_registry
install_chaos_mesh
apply_swipe_secret

echo "Workshop cluster ${CLUSTER_NAME} is ready."
echo "Site: http://localhost:81"
