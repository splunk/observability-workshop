#!/usr/bin/env bash
set -Eeuo pipefail

if ! command -v jq >/dev/null 2>&1 || ! command -v curl >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq jq curl
fi

YW=$'\e[33m'
RD=$'\e[01;31m'
GN=$'\e[1;92m'
CL=$'\e[m'

header_info() {
  clear
  cat <<"EOF"

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝
EOF
}

fatal() {
  header_info
  echo -e "${RD}$1${CL}\n"
  exit 1
}

user_cancelled() {
  header_info
  echo -e "${RD}VM creation cancelled. No VM was created.${CL}\n"
  exit 0
}

format_elapsed() {
  local total_seconds=$1
  local hours=$((total_seconds / 3600))
  local minutes=$(((total_seconds % 3600) / 60))
  local seconds=$((total_seconds % 60))

  if (( hours > 0 )); then
    printf '%dh %02dm %02ds' "$hours" "$minutes" "$seconds"
  elif (( minutes > 0 )); then
    printf '%dm %02ds' "$minutes" "$seconds"
  else
    printf '%ds' "$seconds"
  fi
}

wait_for_guest_agent() {
  local vmid=$1
  local deadline=$2

  echo -e "${YW}Waiting for QEMU Guest Agent...${CL}"

  while (( $(date +%s) < deadline )); do
    if qm agent "$vmid" ping >/dev/null 2>&1; then
      echo -e "${GN}QEMU Guest Agent is ready.${CL}"
      return 0
    fi
    sleep 5
  done

  WORKSHOP_FAILURE_REASON="Timed out waiting for QEMU Guest Agent"
  return 1
}

get_guest_ipv4() {
  local vmid=$1
  local network_json

  network_json=$(qm agent "$vmid" network-get-interfaces 2>/dev/null) || return 1

  jq -r '
    (if type == "object" and has("return") then .return else . end)
    | [
        .[]
        | select((.name // "") != "lo")
        | select((.name // "") | test("^(docker|br-|veth|k3d)") | not)
        | .["ip-addresses"][]?
        | select(.["ip-address-type"] == "ipv4")
        | select(.["ip-address"] != "127.0.0.1")
        | .["ip-address"]
      ][0] // empty
  ' <<< "$network_json"
}

# Runs workshop-status in the guest and sets STATUS_OUTPUT/STATUS_STATE/
# STATUS_DETAIL. Fails when the agent is not up or returns no output yet.
get_workshop_status() {
  local response
  response=$(qm guest exec "$1" -- /usr/local/sbin/workshop-status 2>/dev/null) || return 1
  STATUS_OUTPUT=$(jq -er '."out-data" // empty' <<< "$response" 2>/dev/null) || return 1
  STATUS_STATE=$(sed -n '1p' <<< "$STATUS_OUTPUT")
  STATUS_DETAIL=$(sed -n '2p' <<< "$STATUS_OUTPUT")
}

LAST_STAGE=""
print_stage() {
  if [[ -n "$1" && "$1" != "$LAST_STAGE" ]]; then
    echo -e "Provisioning: ${YW}$1${CL}"
    LAST_STAGE="$1"
  fi
}

set_failure_from_status() {
  WORKSHOP_FAILURE_REASON=$(tail -n +2 <<< "$STATUS_OUTPUT")
  [[ -n "$WORKSHOP_FAILURE_REASON" ]] || WORKSHOP_FAILURE_REASON="Guest provisioning failed without details"
}

wait_for_workshop() {
  local vmid=$1
  local deadline=$2
  local cloud_response cloud_output cloud_state

  echo -e "${YW}Waiting for workshop provisioning...${CL}"

  while (( $(date +%s) < deadline )); do
    if [[ -z "$DISCOVERED_IP" ]]; then
      DISCOVERED_IP=$(get_guest_ipv4 "$vmid" || true)
      if [[ -n "$DISCOVERED_IP" ]]; then
        echo -e "IP address: ${YW}${DISCOVERED_IP}${CL}"
      fi
    fi

    if ! get_workshop_status "$vmid"; then
      sleep 10
      continue
    fi

    case "$STATUS_STATE" in
      READY)
        if cloud_response=$(qm guest exec "$vmid" -- /usr/bin/cloud-init status 2>/dev/null) \
          && cloud_output=$(jq -er '."out-data" // empty' <<< "$cloud_response" 2>/dev/null); then
          cloud_state=$(awk -F': ' '/^status:/ {print $2; exit}' <<< "$cloud_output")

          case "$cloud_state" in
            done)
              echo -e "${GN}Workshop provisioning completed.${CL}"
              return 0
              ;;
            error)
              WORKSHOP_FAILURE_REASON="cloud-init reported an error"
              return 1
              ;;
          esac
        fi
        print_stage "Waiting for cloud-init finalization"
        ;;
      FAILED)
        set_failure_from_status
        return 1
        ;;
      RUNNING)
        print_stage "$STATUS_DETAIL"
        ;;
      STARTING)
        print_stage "Starting provisioning"
        ;;
    esac

    sleep 10
  done

  WORKSHOP_FAILURE_REASON="Timed out waiting for workshop provisioning"
  return 1
}

wait_for_template_shutdown() {
  local vmid=$1
  local deadline=$2

  while (( $(date +%s) < deadline )); do
    if [[ $(qm status "$vmid" | awk '{print $2}') == "stopped" ]]; then
      return 0
    fi

    if get_workshop_status "$vmid"; then
      case "$STATUS_STATE" in
        FAILED)
          set_failure_from_status
          return 1
          ;;
        RUNNING)
          print_stage "$STATUS_DETAIL"
          ;;
      esac
    fi

    sleep 15
  done

  WORKSHOP_FAILURE_REASON="Timed out waiting for template provisioning and shutdown"
  return 1
}

show_workshop_failure() {
  local vmid=$1
  local elapsed=$2

  echo
  echo -e "${RD}Provisioning did not complete after ${elapsed}.${CL}"
  echo -e "${RD}${WORKSHOP_FAILURE_REASON}${CL}"
  echo
  echo "The VM has been preserved for troubleshooting."
  echo "Check provisioning status:"
  echo "  qm guest exec ${vmid} -- /usr/local/sbin/workshop-status"
  echo "View the provisioning log:"
  echo "  qm guest exec ${vmid} -- tail -n 200 /var/log/o11y-workshop-provision.log"
  echo "View cloud-init status:"
  echo "  qm guest exec ${vmid} -- cloud-init status --long"
  echo "View cloud-init output:"
  echo "  qm guest exec ${vmid} -- tail -n 200 /var/log/cloud-init-output.log"

  if [[ -n "${DISCOVERED_IP:-}" ]]; then
    echo "Connect for further troubleshooting:"
    echo "  ssh ${VM_USER}@${DISCOVERED_IP}"
  fi
}

show_workshop_success() {
  local vmid=$1
  local hostname=$2
  local ip=$3
  local elapsed=$4

  echo
  echo -e "${GN}Splunk Observability Workshop is ready.${CL}"
  echo "Provisioning time: ${elapsed}"
  echo "VM ID: ${vmid}"
  echo "Hostname: ${hostname}"

  if [[ -n "$ip" ]]; then
    echo "IP address: ${ip}"
    echo
    echo "Connect:"
    echo "  ssh ${VM_USER}@${ip}"
    echo "  Password: ${VM_PASSWORD}"
    echo
    echo "Workshop endpoints:"
    echo "  http://${ip}"
    echo "  http://${ip}:81"
    echo "  http://${ip}:82"
  else
    echo "IP address: Not reported by QEMU Guest Agent"
    echo "Retrieve it with:"
    echo "  qm agent ${vmid} network-get-interfaces"
  fi

  echo
  echo "Useful checks:"
  echo "  qm guest exec ${vmid} -- kubectl get nodes"
  echo "  qm guest exec ${vmid} -- systemctl status k3d-cluster.service"
}

TEMPLATE_MODE=false
USE_TEMPLATE_CLONE=false
TEMPLATE_SOURCE_VMID=""
TEMPLATE_SOURCE_NAME=""
NONINTERACTIVE=false
ASSUME_YES=false
CLI_MODE=""
CLI_SWIPE_ID=""
CLI_ENV_NAME=""
CLI_DIAB_VERSION=""
CLI_USE_TEMPLATE_CLONE=""
CLI_TEMPLATE_NAME=""
CLI_TEMPLATE_VMID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --non-interactive) NONINTERACTIVE=true; shift ;;
    --assume-yes) ASSUME_YES=true; shift ;;
    --mode) CLI_MODE="${2:-}"; shift 2 ;;
    --swipe-id) CLI_SWIPE_ID="${2:-}"; shift 2 ;;
    --env-name) CLI_ENV_NAME="${2:-}"; shift 2 ;;
    --diab-version) CLI_DIAB_VERSION="${2:-}"; shift 2 ;;
    --use-template-clone) CLI_USE_TEMPLATE_CLONE="${2:-}"; shift 2 ;;
    --template-name) CLI_TEMPLATE_NAME="${2:-}"; shift 2 ;;
    --template-vmid) CLI_TEMPLATE_VMID="${2:-}"; shift 2 ;;
    --help|-h)
      echo "Usage: $0 [--non-interactive] [--assume-yes] [--mode normal|template] [--swipe-id ID] [--env-name NAME] [--diab-version staging|production] [--use-template-clone yes|no] [--template-vmid VMID] [--template-name NAME]"
      exit 0
      ;;
    *)
      fatal "Unknown argument: $1"
      ;;
  esac
done

TEMPLATE_LIST=$(pvesh get /cluster/resources --type vm --output-format json | jq -r '.[] | select(((.template // 0) | tostring) == "1") | select((.tags // "") | test("(^|[;,])o11y-k3d-template([;,]|$)")) | "\(.vmid)|\(.name // "template")"')

if [[ "$NONINTERACTIVE" == "true" ]]; then
  CLI_MODE=${CLI_MODE,,}
  case "${CLI_MODE:-normal}" in
    template) TEMPLATE_MODE=true ;;
    normal) TEMPLATE_MODE=false ;;
    *) fatal "Invalid --mode: ${CLI_MODE}. Use normal or template." ;;
  esac
else
  MODE_SELECTION=$(whiptail \
    --backtitle "Splunk Observability Workshop" \
    --title "Choose Action" \
    --menu "What would you like to create?" \
    14 72 2 \
    "workshop" "Create a ready-to-use workshop VM" \
    "template" "Build a reusable Proxmox template (advanced)" \
    3>&1 1>&2 2>&3) || user_cancelled

  [[ "$MODE_SELECTION" == "template" ]] && TEMPLATE_MODE=true || TEMPLATE_MODE=false
fi

if [[ "$TEMPLATE_MODE" == "true" ]]; then
  echo -e "Mode: ${YW}Template build${CL}"
  if [[ "$NONINTERACTIVE" == "true" ]]; then
    TEMPLATE_NAME="${CLI_TEMPLATE_NAME:-o11y-k3d-template}"
  else
    TEMPLATE_NAME=$(whiptail --backtitle "Splunk Observability Workshop" --title "Template Name" --inputbox "Enter template base name (default: o11y-k3d-template):" 10 68 3>&1 1>&2 2>&3) || user_cancelled
  fi

  TEMPLATE_NAME=$(tr -cs 'a-z0-9-' '-' <<< "${TEMPLATE_NAME,,}")
  TEMPLATE_NAME="${TEMPLATE_NAME#-}"
  TEMPLATE_NAME="${TEMPLATE_NAME%-}"
  TEMPLATE_NAME="${TEMPLATE_NAME:-o11y-k3d-template}"
  ENV_NAME="$TEMPLATE_NAME"
  DIAB_VERSION="production"
  SWIPE_ID=""
  echo -e "Template Name: ${YW}${TEMPLATE_NAME}${CL}"
else
  echo -e "Mode: ${YW}Normal workshop VM${CL}"
  if [[ "$NONINTERACTIVE" == "true" ]]; then
    SWIPE_ID="$CLI_SWIPE_ID"
    ENV_NAME="${CLI_ENV_NAME:-workshop}"
    DIAB_VERSION=${CLI_DIAB_VERSION,,}
    DIAB_VERSION=${DIAB_VERSION:-production}
  else
    SWIPE_ID=$(whiptail --backtitle "Splunk Observability Workshop" --title "SWiPE ID" --inputbox "Enter your SWiPE ID:" 10 68 3>&1 1>&2 2>&3) || user_cancelled

    ENV_NAME=$(whiptail --backtitle "Splunk Observability Workshop" --title "Environment Name" --inputbox "Enter environment name (default: workshop):" 10 68 3>&1 1>&2 2>&3) || user_cancelled
    ENV_NAME="${ENV_NAME:-workshop}"

    DIAB_VERSION=$(whiptail \
      --backtitle "Splunk Observability Workshop" \
      --title "Demo-in-a-Box Version" \
      --menu "Choose the workshop content version:" \
      14 72 2 \
      "production" "Production (recommended)" \
      "staging" "Staging (testing and development)" \
      3>&1 1>&2 2>&3) || user_cancelled
  fi

  [[ -n "$SWIPE_ID" ]] || fatal "Invalid SWiPE ID. Exiting script."
  case "$DIAB_VERSION" in
    staging|production) ;;
    *) fatal "Invalid demo-in-a-box version: ${DIAB_VERSION}. Use staging or production." ;;
  esac
  echo -e "SWiPE ID: ${YW}${SWIPE_ID}${CL}"
  echo -e "Environment: ${YW}${ENV_NAME}${CL}"
  echo -e "Demo-in-a-Box Version: ${YW}${DIAB_VERSION^}${CL}"

  TEMPLATE_CLONE_SELECTED=false
  if [[ "$NONINTERACTIVE" == "true" ]]; then
    case "${CLI_USE_TEMPLATE_CLONE,,}" in
      yes|true|1) TEMPLATE_CLONE_SELECTED=true ;;
      no|false|0|"") TEMPLATE_CLONE_SELECTED=false ;;
      *) fatal "Invalid --use-template-clone value. Use yes or no." ;;
    esac
  elif [[ -n "$TEMPLATE_LIST" ]]; then
    TEMPLATE_PROVISIONING=$(whiptail \
      --backtitle "Splunk Observability Workshop" \
      --title "Provisioning Method" \
      --menu "A compatible workshop template is available. Choose how to create the VM:" \
      15 78 2 \
      "clone" "Clone an existing template (fastest)" \
      "full" "Build from the Ubuntu cloud image" \
      3>&1 1>&2 2>&3) || user_cancelled

    [[ "$TEMPLATE_PROVISIONING" == "clone" ]] && TEMPLATE_CLONE_SELECTED=true
  else
    echo -e "${YW}No compatible workshop templates found. A full build will be used.${CL}"
  fi

  if [[ "$TEMPLATE_CLONE_SELECTED" == "true" ]]; then
    if [[ -z "$TEMPLATE_LIST" ]]; then
      echo -e "${YW}No workshop templates found (tag: o11y-k3d-template). Falling back to full build.${CL}"
    else
      mapfile -t TEMPLATE_OPTIONS <<< "$TEMPLATE_LIST"
      if [[ -n "$CLI_TEMPLATE_VMID" ]]; then
        TEMPLATE_SOURCE_VMID="$CLI_TEMPLATE_VMID"
        TEMPLATE_SOURCE_NAME=$(awk -F'|' -v id="$TEMPLATE_SOURCE_VMID" '$1==id {print $2; exit}' <<< "$TEMPLATE_LIST")
        if [[ -z "$TEMPLATE_SOURCE_NAME" ]]; then
          echo -e "${YW}Template VMID ${TEMPLATE_SOURCE_VMID} not found in workshop templates. Falling back to full build.${CL}"
          TEMPLATE_SOURCE_VMID=""
        fi
      elif (( ${#TEMPLATE_OPTIONS[@]} == 1 )) || [[ "$NONINTERACTIVE" == "true" ]]; then
        TEMPLATE_SOURCE_VMID="${TEMPLATE_OPTIONS[0]%%|*}"
        TEMPLATE_SOURCE_NAME="${TEMPLATE_OPTIONS[0]#*|}"
      else
        MENU_ITEMS=()
        for template_option in "${TEMPLATE_OPTIONS[@]}"; do
          MENU_ITEMS+=("${template_option%%|*}" "${template_option#*|}")
        done
        TEMPLATE_SOURCE_VMID=$(whiptail --backtitle "Splunk Observability Workshop" --title "Select Template" --menu "Choose the template to clone:" 18 72 10 "${MENU_ITEMS[@]}" 3>&1 1>&2 2>&3) || user_cancelled
        TEMPLATE_SOURCE_NAME=$(awk -F'|' -v id="$TEMPLATE_SOURCE_VMID" '$1==id {print $2; exit}' <<< "$TEMPLATE_LIST")
      fi

      if [[ -n "$TEMPLATE_SOURCE_VMID" ]]; then
        USE_TEMPLATE_CLONE=true
        echo -e "Template Clone: ${YW}Yes${CL} (${TEMPLATE_SOURCE_VMID} - ${TEMPLATE_SOURCE_NAME})"
      else
        echo -e "${YW}Template not selected. Falling back to full build.${CL}"
      fi
    fi
  else
    echo -e "Template Clone: ${YW}No${CL}"
  fi
fi

if [[ "$TEMPLATE_MODE" == "true" ]]; then
  REALM=""
  RUM_TOKEN=""
  INGEST_TOKEN=""
  API_TOKEN=""
  HEC_TOKEN=""
  HEC_URL=""
else
  JSON_RESPONSE=$(curl -fsS "https://swipe.splunk.show/api?id=${SWIPE_ID}") \
    || fatal "Could not reach the SWiPE API. Exiting script."

  if [[ "$JSON_RESPONSE" == '{"message":"Workshop ID not found"}' ]]; then
    fatal "Workshop ID not found. Exiting script."
  fi

  REALM=$(jq -r '.REALM // empty' <<< "$JSON_RESPONSE")
  [[ -n "$REALM" ]] || fatal "Unexpected SWiPE API response (missing REALM). Exiting script."
  RUM_TOKEN=$(jq -r '.RUM // ""' <<< "$JSON_RESPONSE")
  INGEST_TOKEN=$(jq -r '.INGEST // ""' <<< "$JSON_RESPONSE")
  API_TOKEN=$(jq -r '.API // ""' <<< "$JSON_RESPONSE")
  HEC_TOKEN=$(jq -r '.HEC_TOKEN // ""' <<< "$JSON_RESPONSE")
  HEC_URL=$(jq -r '.HEC_URL // ""' <<< "$JSON_RESPONSE")
fi

VMID=$(pvesh get /cluster/nextid)
STORAGE=local-lvm
if [[ "$TEMPLATE_MODE" == "true" ]]; then
  HOSTNAME="${ENV_NAME}-${VMID}"
else
  HOSTNAME="${VMID}-${ENV_NAME}-$(openssl rand -hex 2)"
fi
VM_USER=splunk
VM_PASSWORD='Splunk123!'
SNIPPET_NAME="k3d-${VMID}.yaml"
SNIPPET_PATH="/var/lib/vz/snippets/${SNIPPET_NAME}"
K3D_VERSION=v5.9.0
CHAOS_MESH_VERSION=v2.8.0
CHAOS_MESH_INSTALLER_SHA256=07170c3ae6c6578640a6d58f953ff92312e1dbebffb4838642b5d979f2c1486a

# Tool versions are only needed for a full build; clone mode inherits the
# template's tools, so skip the GitHub API calls entirely.
LATEST_K9S_VERSION=""
LATEST_TERRAFORM_VERSION=""
if [[ "$USE_TEMPLATE_CLONE" != "true" ]]; then
  LATEST_K9S_VERSION=$(curl -fsS https://api.github.com/repos/derailed/k9s/releases/latest | jq -er '.tag_name') \
    || fatal "Could not resolve the latest k9s release from the GitHub API."
  LATEST_TERRAFORM_VERSION=$(curl -fsS https://api.github.com/repos/hashicorp/terraform/releases/latest | jq -er '.tag_name | ltrimstr("v")') \
    || fatal "Could not resolve the latest Terraform release from the GitHub API."
fi

if [[ "$NONINTERACTIVE" != "true" && "$ASSUME_YES" != "true" ]]; then
  if [[ "$TEMPLATE_MODE" == "true" ]]; then
    CONFIRM_TITLE="Confirm Template Build"
    CONFIRM_TEXT="Review the template build:\n\nAction: Build reusable Proxmox template\nTemplate name: ${TEMPLATE_NAME}\nVM ID: ${VMID}\nCPU: 4 cores\nMemory: 24 GiB\nDisk: 60 GiB\nStorage: ${STORAGE}\nNetwork: vmbr0 with DHCP\n\nThe VM will power off and be converted to a template when provisioning succeeds."
  else
    if [[ "$USE_TEMPLATE_CLONE" == "true" ]]; then
      PROVISIONING_SUMMARY="Clone template ${TEMPLATE_SOURCE_VMID} (${TEMPLATE_SOURCE_NAME})"
      RESOURCE_SUMMARY="Inherited from the selected template"
    else
      PROVISIONING_SUMMARY="Full build from Ubuntu Noble cloud image"
      RESOURCE_SUMMARY="4 cores, 24 GiB RAM, 60 GiB disk"
    fi

    CONFIRM_TITLE="Confirm Workshop VM"
    CONFIRM_TEXT="Review the workshop VM:\n\nEnvironment: ${ENV_NAME}\nVM ID: ${VMID}\nSWiPE ID: ${SWIPE_ID}\nContent: ${DIAB_VERSION}\nProvisioning: ${PROVISIONING_SUMMARY}\nResources: ${RESOURCE_SUMMARY}\nStorage: ${STORAGE}\nNetwork: vmbr0 with DHCP\n\nCreate this workshop VM?"
  fi

  whiptail \
    --backtitle "Splunk Observability Workshop" \
    --title "$CONFIRM_TITLE" \
    --yes-button "Create" \
    --no-button "Cancel" \
    --yesno "$CONFIRM_TEXT" \
    22 82 || user_cancelled
fi

echo -e "Hostname: ${YW}${HOSTNAME}${CL}\n"

# The cloud-init snippet is rendered in two parts:
#   1. an interpolated heredoc for everything that carries host-side values
#      (identity, tokens, versions), including /etc/o11y-workshop.env, and
#   2. a quoted heredoc for the static guest scripts, which therefore need
#      no \$ escaping and read their inputs from /etc/o11y-workshop.env.
# Keep each VM's credential-bearing cloud-init data isolated from other
# deployments and readable only by root on the Proxmox host.
install -m 0600 /dev/null "$SNIPPET_PATH"

cat > "$SNIPPET_PATH" <<CLOUDCFG_DYNAMIC
#cloud-config
package_update: true
package_upgrade: false
package_reboot_if_required: false

hostname: $HOSTNAME
manage_etc_hosts: true
fqdn: $HOSTNAME
chpasswd:
  expire: false
  users:
    - name: $VM_USER
      password: "$VM_PASSWORD"
      type: text
users:
  - name: $VM_USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
ssh_pwauth: True

packages:
  - ansible
  - ca-certificates
  - cron
  - curl
  - git
  - gnupg
  - jq
  - maven
  - net-tools
  - openjdk-17-jdk
  - python3-pip
  - python3-venv
  - qemu-guest-agent
  - unzip
  - vim
  - wget
  - whiptail
  - zsh

write_files:
  - path: /etc/o11y-workshop.env
    permissions: '0644'
    content: |
      HOSTNAME=$HOSTNAME
      CLUSTER_NAME=$HOSTNAME-cluster
      VM_USER=$VM_USER
      TEMPLATE_MODE=$TEMPLATE_MODE
      USE_TEMPLATE_CLONE=$USE_TEMPLATE_CLONE
      DIAB_VERSION=$DIAB_VERSION
      K9S_VERSION=$LATEST_K9S_VERSION
      TERRAFORM_VERSION=$LATEST_TERRAFORM_VERSION
      K3D_VERSION=$K3D_VERSION
      CHAOS_MESH_VERSION=$CHAOS_MESH_VERSION
      CHAOS_MESH_INSTALLER_SHA256=$CHAOS_MESH_INSTALLER_SHA256

  # This file is appended, not replaced: a clone's block lands after the
  # template's block, and zsh logins read it via /etc/skel/.profile directly,
  # so the last-written values win. The TEMPLATE_MODE test below is folded to
  # a constant at render time, which keeps token exports out of template
  # builds while clones re-render it with live tokens.
  - path: /etc/skel/.profile
    append: true
    content: |
      if ! sudo /usr/bin/cloud-init status 2>/dev/null | grep -q '^status: done$'; then
        echo "Waiting for cloud-init status..."
        if /usr/bin/timeout 180 sudo /usr/bin/cloud-init status --wait; then
          echo "Your instance is ready!";
        else
          echo "Instance setup did not complete successfully after 3 minutes. Please try again.";
        fi
      fi

      if [ "${TEMPLATE_MODE}" != "true" ]; then
        # Splunk environment variables
        export RUM_TOKEN="$RUM_TOKEN"
        export ACCESS_TOKEN="$INGEST_TOKEN"
        export INGEST_TOKEN="$INGEST_TOKEN"
        export API_TOKEN="$API_TOKEN"
        export HEC_TOKEN="$HEC_TOKEN"
        export HEC_URL="$HEC_URL"
        export REALM="$REALM"
      fi

      INSTANCE="$HOSTNAME"
      CLUSTER_NAME="$HOSTNAME-cluster"

      export INSTANCE CLUSTER_NAME

      export KUBECONFIG=/home/splunk/.kube/config
      alias kc='kubectl'
      alias dc='docker-compose'

  - path: /home/splunk/workshop-secrets.yaml
    permissions: '0600'
    content: |
      apiVersion: v1
      kind: Secret
      metadata:
        name: workshop-secret
        namespace: default
      type: Opaque
      stringData:
        app: $HOSTNAME-store
        env: $HOSTNAME-workshop
        instance: $HOSTNAME-workshop
        deployment: "deployment.environment=$HOSTNAME-workshop"
        realm: $REALM
        ingest_token: $INGEST_TOKEN
        api_token: $API_TOKEN
        rum_token: $RUM_TOKEN
        hec_token: $HEC_TOKEN
        hec_url: $HEC_URL
        url: http://frontend-proxy:8080
CLOUDCFG_DYNAMIC

cat >> "$SNIPPET_PATH" <<'CLOUDCFG_STATIC'

  - path: /etc/modules-load.d/k3d.conf
    permissions: '0644'
    content: |
      overlay
      br_netfilter

  - path: /etc/sysctl.d/99-k3d.conf
    permissions: '0644'
    content: |
      # Kubernetes networking
      net.bridge.bridge-nf-call-iptables=1
      net.bridge.bridge-nf-call-ip6tables=1
      net.ipv4.ip_forward=1

      # Increase inotify limits
      fs.inotify.max_user_watches=524288
      fs.inotify.max_user_instances=8192

  # Manage the cluster as a unit so Docker cannot assign node addresses in a
  # different order when it restarts all k3d containers concurrently.
  - path: /etc/systemd/system/k3d-cluster.service
    permissions: '0644'
    content: |
      [Unit]
      Description=Managed k3d workshop cluster
      Requires=docker.service
      PartOf=docker.service
      After=docker.service network-online.target
      Wants=network-online.target

      [Service]
      Type=oneshot
      RemainAfterExit=yes
      EnvironmentFile=/etc/o11y-workshop.env
      ExecStartPre=-/usr/local/bin/k3d cluster stop ${CLUSTER_NAME}
      ExecStart=/usr/local/bin/k3d cluster start ${CLUSTER_NAME} --wait
      ExecStop=/usr/local/bin/k3d cluster stop ${CLUSTER_NAME}
      TimeoutStartSec=300
      TimeoutStopSec=120
      Restart=on-failure
      RestartSec=10

      [Install]
      WantedBy=multi-user.target

  - path: /usr/local/sbin/workshop-stage
    permissions: '0755'
    content: |
      #!/usr/bin/env bash
      set -Eeuo pipefail

      status_dir=/var/lib/o11y-workshop
      status_file="${status_dir}/status"
      ready_file="${status_dir}/ready"
      failed_file="${status_dir}/failed"
      action="${1:-}"

      install -d -m 0700 "${status_dir}"

      case "${action}" in
        reset)
          rm -f "${ready_file}" "${failed_file}"
          printf '%s\n' 'Starting provisioning' > "${status_file}.tmp"
          mv "${status_file}.tmp" "${status_file}"
          ;;
        stage)
          printf '%s\n' "${2:?stage name is required}" > "${status_file}.tmp"
          mv "${status_file}.tmp" "${status_file}"
          ;;
        fail)
          exit_code="${2:-1}"
          stage='Unknown provisioning stage'
          if [[ -s "${status_file}" ]]; then
            stage=$(<"${status_file}")
          fi
          {
            printf 'exit_code=%s\n' "${exit_code}"
            printf 'stage=%s\n' "${stage}"
            printf 'time=%s\n' "$(date --iso-8601=seconds)"
          } > "${failed_file}"
          rm -f "${ready_file}"
          ;;
        ready)
          date --iso-8601=seconds > "${ready_file}"
          rm -f "${failed_file}"
          ;;
        *)
          echo "Usage: $0 reset|stage NAME|fail EXIT_CODE|ready" >&2
          exit 2
          ;;
      esac

  - path: /usr/local/sbin/workshop-status
    permissions: '0755'
    content: |
      #!/usr/bin/env bash
      set -u

      status_dir=/var/lib/o11y-workshop
      cloud_init_output=$(/usr/bin/cloud-init status 2>/dev/null || true)
      cloud_init_state=${cloud_init_output#status: }

      if [[ -f "${status_dir}/failed" ]]; then
        echo 'FAILED'
        cat "${status_dir}/failed"
      elif [[ "${cloud_init_state}" == "error" ]]; then
        echo 'FAILED'
        echo 'cloud-init reported an error'
      elif [[ -f "${status_dir}/ready" && "${cloud_init_state}" == "done" ]]; then
        echo 'READY'
      elif [[ -f "${status_dir}/ready" ]]; then
        echo 'RUNNING'
        echo 'Waiting for cloud-init finalization'
      elif [[ -f "${status_dir}/status" ]]; then
        echo 'RUNNING'
        cat "${status_dir}/status"
      else
        echo 'STARTING'
      fi

  - path: /usr/local/lib/o11y-workshop/lib.sh
    permissions: '0644'
    content: |
      # Shared helpers for the o11y workshop provisioning scripts.
      retry() {
        local attempt
        for attempt in 1 2 3 4 5; do
          if "$@"; then
            return 0
          fi
          echo "Command failed (attempt $attempt of 5): $*" >&2
          (( attempt < 5 )) && sleep $((attempt * 10))
        done
        echo "Giving up after 5 attempts: $*" >&2
        return 1
      }

      # Retried curl: external endpoints (Cloudflare, GitHub) intermittently
      # return 5xx, which must not sink a 30+ minute provisioning run.
      fetch() {
        retry curl -fsSL "$@"
      }

      wait_for_jobs() {
        local failed=0 pid
        for pid in "$@"; do
          wait "$pid" || failed=1
        done
        return "$failed"
      }

  - path: /usr/local/lib/o11y-workshop/install.sh
    permissions: '0755'
    content: |
      #!/usr/bin/env bash
      set -Eeuo pipefail
      . /etc/o11y-workshop.env
      . /usr/local/lib/o11y-workshop/lib.sh

      # Workshop content is downloaded when a workshop VM is created — never
      # baked into a template — so every instance picks up the latest GitHub
      # release instead of whatever was current when the template was built.
      download_workshop_content() {
        /usr/local/sbin/workshop-stage stage 'Downloading workshop content'
        fetch -o /tmp/workshop.zip https://github.com/splunk/observability-workshop/archive/main.zip
        unzip -qq /tmp/workshop.zip -d /home/splunk/
        rm -f /tmp/workshop.zip
        mkdir -p /home/splunk/workshop
        mv /home/splunk/observability-workshop-main/workshop/* /home/splunk/workshop
        mv /home/splunk/workshop/ansible/diab-*.yml /home/splunk
        rm -rf /home/splunk/observability-workshop-main
        rm -rf /home/splunk/workshop/aws /home/splunk/workshop/cloud-init /home/splunk/workshop/ansible

        # Use the staging build of demo-in-a-box when selected and available
        if [ "$DIAB_VERSION" = "staging" ] && [ -f /home/splunk/workshop/k3s/demo-in-a-box-staging.zip ]; then
          cp /home/splunk/workshop/k3s/demo-in-a-box-staging.zip /home/splunk/workshop/k3s/demo-in-a-box.zip
        fi
        mv /home/splunk/workshop/k3s/demo-in-a-box.zip /home/splunk

        # Splunk Observability Content Contrib repo
        fetch -o /tmp/content-contrib.zip https://github.com/splunk/observability-content-contrib/archive/main.zip
        unzip -qq /tmp/content-contrib.zip -d /home/splunk/
        rm -f /tmp/content-contrib.zip
        mv /home/splunk/observability-content-contrib-main /home/splunk/observability-content-contrib
      }

      /usr/local/sbin/workshop-stage reset
      exec >>/var/log/o11y-workshop-provision.log 2>&1
      trap '/usr/local/sbin/workshop-stage fail "$?"' ERR

      # Clones inherit the template's tools; only the workshop content is
      # fetched fresh.
      if [ "$USE_TEMPLATE_CLONE" = "true" ]; then
        /usr/local/sbin/workshop-stage stage 'Using the reusable workshop template'
        download_workshop_content
        exit 0
      fi

      /usr/local/sbin/workshop-stage stage 'Configuring the shell environment'
      chsh -s "$(command -v zsh)" "$VM_USER"
      # Install Starship prompt (the installer downloads the binary itself,
      # so retry the run as well as the fetch)
      fetch -o /tmp/starship-install.sh https://starship.rs/install.sh
      retry sh /tmp/starship-install.sh -y
      rm -f /tmp/starship-install.sh
      mkdir -p /home/splunk/.config
      starship preset pastel-powerline -o /home/splunk/.config/starship.toml
      cat > /home/splunk/.zshrc <<'ZSHRC'
      if ! infocmp "$TERM" >/dev/null 2>&1; then
        echo "Terminal $TERM not found, using fallback..."
        export TERM=xterm-256color
      fi
      autoload -U +X compinit && compinit
      source /etc/skel/.profile
      source <(kubectl completion zsh)
      source <(helm completion zsh)
      source <(docker completion zsh)
      eval "$(starship init zsh)"
      ZSHRC

      # Install Docker from official repository
      /usr/local/sbin/workshop-stage stage 'Installing Docker'
      export DEBIAN_FRONTEND=noninteractive
      install -m 0755 -d /etc/apt/keyrings
      fetch -o /tmp/docker-apt.gpg https://download.docker.com/linux/ubuntu/gpg
      gpg --dearmor -o /etc/apt/keyrings/docker.gpg < /tmp/docker-apt.gpg
      rm -f /tmp/docker-apt.gpg
      chmod a+r /etc/apt/keyrings/docker.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
      apt-get update -qq
      apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
      usermod -aG docker "$VM_USER"

      # Load and persist the kernel networking prerequisites before creating k3d.
      modprobe overlay
      modprobe br_netfilter
      sysctl --system

      /usr/local/sbin/workshop-stage stage 'Installing Kubernetes tools'
      # Helm (installer downloads the release tarball itself)
      fetch -o /tmp/get-helm-3 https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
      retry bash /tmp/get-helm-3
      rm -f /tmp/get-helm-3

      # K9s
      fetch -o /tmp/k9s.tar.gz "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_amd64.tar.gz"
      tar xfz /tmp/k9s.tar.gz -C /usr/local/bin/ k9s
      rm -f /tmp/k9s.tar.gz

      # Terraform
      fetch -o /tmp/terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
      unzip -qq /tmp/terraform.zip -d /usr/local/bin
      rm -f /tmp/terraform.zip

      # kubectl
      fetch -o /tmp/kubectl "https://dl.k8s.io/release/v1.34.0/bin/linux/amd64/kubectl"
      install -o root -g root -m 0755 /tmp/kubectl /usr/local/bin/kubectl
      rm -f /tmp/kubectl

      # k3d (installer downloads the release binary itself)
      fetch -o /tmp/k3d-install.sh https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh
      export TAG="$K3D_VERSION"
      retry bash /tmp/k3d-install.sh
      unset TAG
      rm -f /tmp/k3d-install.sh

      # Template builds stop here: content is fetched by the instance, not
      # the template.
      if [ "$TEMPLATE_MODE" != "true" ]; then
        download_workshop_content
      fi

  # Template builds cache the k3s and workshop service images so each clone
  # can create a unique cluster without downloading them again.
  - path: /usr/local/lib/o11y-workshop/deploy.sh
    permissions: '0755'
    content: |
      #!/usr/bin/env bash
      set -Eeuo pipefail
      . /etc/o11y-workshop.env
      . /usr/local/lib/o11y-workshop/lib.sh

      if [ -f /var/lib/o11y-workshop/failed ]; then
        exit 1
      fi

      exec >>/var/log/o11y-workshop-provision.log 2>&1
      trap '/usr/local/sbin/workshop-stage fail "$?"' ERR

      /usr/local/sbin/workshop-stage stage 'Starting Docker'
      systemctl enable --now docker
      timeout 120 bash -c 'until docker info >/dev/null 2>&1; do sleep 2; done' \
        || { echo "Docker daemon did not become ready in time"; exit 1; }

      if [ "$TEMPLATE_MODE" = "true" ]; then
        /usr/local/sbin/workshop-stage stage 'Caching Kubernetes images for the template'
        install -d -m 0755 /opt/o11y-workshop-cache/chaos-mesh
        fetch -o /opt/o11y-workshop-cache/chaos-mesh/install.sh \
          "https://raw.githubusercontent.com/chaos-mesh/chaos-mesh/${CHAOS_MESH_VERSION}/install.sh"
        echo "${CHAOS_MESH_INSTALLER_SHA256}  /opt/o11y-workshop-cache/chaos-mesh/install.sh" | sha256sum -c -
        chmod 0755 /opt/o11y-workshop-cache/chaos-mesh/install.sh

        CACHED_WORKSHOP_IMAGES=(
          docker.io/library/registry:2
          "ghcr.io/chaos-mesh/chaos-mesh:${CHAOS_MESH_VERSION}"
          "ghcr.io/chaos-mesh/chaos-daemon:${CHAOS_MESH_VERSION}"
          "ghcr.io/chaos-mesh/chaos-dashboard:${CHAOS_MESH_VERSION}"
          ghcr.io/chaos-mesh/chaos-coredns:v0.2.6
        )

        retry docker pull rancher/k3s:v1.33.4-k3s1
        retry docker pull "ghcr.io/k3d-io/k3d-proxy:${K3D_VERSION#v}"

        CACHE_CLUSTER=o11y-template-image-cache
        k3d cluster delete "$CACHE_CLUSTER" >/dev/null 2>&1 || true
        k3d cluster create "$CACHE_CLUSTER" \
          --servers 1 \
          --agents 0 \
          --no-lb \
          --image rancher/k3s:v1.33.4-k3s1 \
          --timeout 10m \
          -v "/opt/o11y-workshop-cache:/opt/o11y-workshop-cache@server:0"

        CACHE_NODE="k3d-${CACHE_CLUSTER}-server-0"
        PIDS=()
        for image in "${CACHED_WORKSHOP_IMAGES[@]}"; do
          retry docker exec "$CACHE_NODE" ctr --namespace k8s.io images pull --platform linux/amd64 "$image" &
          PIDS+=("$!")
        done
        wait_for_jobs "${PIDS[@]}"

        docker exec "$CACHE_NODE" ctr --namespace k8s.io images export \
          --platform linux/amd64 \
          /opt/o11y-workshop-cache/workshop-images.tar \
          "${CACHED_WORKSHOP_IMAGES[@]}"

        k3d cluster delete "$CACHE_CLUSTER"
      else
        command -v k3d >/dev/null 2>&1 || { echo "k3d is not installed on this template"; exit 1; }

        /usr/local/sbin/workshop-stage stage 'Creating the k3d cluster'
        k3d cluster create "$CLUSTER_NAME" \
          --agents 2 \
          --servers-memory 8G \
          --agents-memory 7G \
          --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@server:0" \
          --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@agent:*" \
          --image rancher/k3s:v1.33.4-k3s1 \
          --timeout 10m \
          --port "80:80@loadbalancer" \
          --port "81:80@loadbalancer" \
          --port "82:82@loadbalancer" \
          --port "9999:9999@loadbalancer" \
          --port "443:443@loadbalancer" \
          -v "/home/splunk:/home/splunk@server:*;agent:*" \
          -v "/opt/o11y-workshop-cache:/opt/o11y-workshop-cache@server:*;agent:*" \
          -v "/var/log/syslog:/var/log/syslog@server:*;agent:*" \
          -v "/var/log/auth.log:/var/log/auth.log@server:*;agent:*"

        if [ -s /opt/o11y-workshop-cache/workshop-images.tar ]; then
          /usr/local/sbin/workshop-stage stage 'Importing cached workshop images'
          PIDS=()
          for node in server-0 agent-0 agent-1; do
            docker exec "k3d-${CLUSTER_NAME}-${node}" ctr --namespace k8s.io images import \
              /opt/o11y-workshop-cache/workshop-images.tar &
            PIDS+=("$!")
          done
          wait_for_jobs "${PIDS[@]}"
        fi

        # Let systemd manage cluster shutdown/startup as one ordered operation.
        # Docker restart policies remain enabled for recovery from crashes.
        systemctl daemon-reload
        systemctl enable k3d-cluster.service

        # Create k3d kube config and set correct permissions.
        mkdir -p /home/splunk/.kube
        k3d kubeconfig get "$CLUSTER_NAME" > /home/splunk/.kube/config
        chmod 400 /home/splunk/.kube/config

        /usr/local/sbin/workshop-stage stage 'Deploying workshop services'
        kubectl apply -f /home/splunk/workshop/k3s/registry/registry.yaml
        CHAOS_MESH_INSTALLER=/opt/o11y-workshop-cache/chaos-mesh/install.sh
        if [ ! -f "$CHAOS_MESH_INSTALLER" ]; then
          CHAOS_MESH_INSTALLER=/tmp/chaos-mesh-install.sh
          fetch -o "$CHAOS_MESH_INSTALLER" \
            "https://raw.githubusercontent.com/chaos-mesh/chaos-mesh/${CHAOS_MESH_VERSION}/install.sh"
        fi
        echo "${CHAOS_MESH_INSTALLER_SHA256}  ${CHAOS_MESH_INSTALLER}" | sha256sum -c -
        bash "$CHAOS_MESH_INSTALLER" --k3s --version "$CHAOS_MESH_VERSION"

        # Point the RUM load generators at the VM's external address so they
        # exercise the same ingress path as a real user. The DHCP address is
        # unknown when the snippet is rendered on the Proxmox host, so it is
        # resolved here at deploy time; on failure the secret keeps the
        # in-cluster frontend-proxy fallback.
        PRIMARY_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for (i=1; i<NF; i++) if ($i == "src") {print $(i+1); exit}}')
        if [ -n "$PRIMARY_IP" ]; then
          sed -i "s|^\( *url:\).*|\1 http://${PRIMARY_IP}|" /home/splunk/workshop-secrets.yaml
        fi
        kubectl apply -f /home/splunk/workshop-secrets.yaml

        /usr/local/sbin/workshop-stage stage 'Checking Kubernetes readiness'
        kubectl wait --for=condition=Ready node --all --timeout=5m
        kubectl wait --for=condition=Ready pod -n kube-system -l k8s-app=kube-registry --timeout=5m
        kubectl rollout status deployment/chaos-controller-manager -n chaos-mesh --timeout=5m
        kubectl rollout status deployment/chaos-dashboard -n chaos-mesh --timeout=5m
        kubectl rollout status daemonset/chaos-daemon -n chaos-mesh --timeout=5m
      fi

      /usr/local/sbin/workshop-stage stage 'Finalizing the workshop VM'
      chown -R splunk:splunk /home/splunk

  - path: /usr/local/lib/o11y-workshop/finalize.sh
    permissions: '0755'
    content: |
      #!/usr/bin/env bash
      set -Eeuo pipefail
      . /etc/o11y-workshop.env

      if [ -f /var/lib/o11y-workshop/failed ]; then
        exit 1
      fi

      trap '/usr/local/sbin/workshop-stage fail "$?"' ERR

      if [ "$TEMPLATE_MODE" = "true" ]; then
        rm -f /var/lib/o11y-workshop/ready /var/lib/o11y-workshop/failed /var/lib/o11y-workshop/status
        cloud-init clean --logs
        truncate -s 0 /etc/machine-id
        rm -f /var/lib/dbus/machine-id
        ln -s /etc/machine-id /var/lib/dbus/machine-id
        sync
        shutdown -h now
      else
        /usr/local/sbin/workshop-stage ready
      fi

runcmd:
  - systemctl enable --now qemu-guest-agent
  - /usr/local/lib/o11y-workshop/install.sh
  - /usr/local/lib/o11y-workshop/deploy.sh
  - /usr/local/lib/o11y-workshop/finalize.sh
CLOUDCFG_STATIC

IMAGE_URL="https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
IMAGE_CACHE="/var/lib/vz/template/iso/noble-server-cloudimg-amd64.img"

WORK_DIR=""

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM HUP

  # Only remove this deployment's temporary copy.
  if [[ -n "$WORK_DIR" ]]; then
    rm -rf -- "$WORK_DIR"
  fi

  exit "$exit_code"
}

trap cleanup EXIT INT TERM HUP

if [[ "$USE_TEMPLATE_CLONE" == "true" ]]; then
  echo -e "${YW}Cloning template VM ${TEMPLATE_SOURCE_VMID} (${TEMPLATE_SOURCE_NAME})...${CL}"
  qm clone "$TEMPLATE_SOURCE_VMID" "$VMID" --name "$HOSTNAME" >/dev/null
else
  WORK_DIR=$(mktemp -d)
  VM_IMAGE="${WORK_DIR}/noble-server-cloudimg-amd64.img"

  if [[ ! -f "$IMAGE_CACHE" ]]; then
    echo "Downloading Ubuntu Noble base image..."
    curl -fsSL -o "${IMAGE_CACHE}.download" "$IMAGE_URL"
    mv "${IMAGE_CACHE}.download" "$IMAGE_CACHE"
  else
    echo "Using cached Ubuntu Noble base image."
  fi

  # Create a private, disposable copy.
  cp --reflink=auto "$IMAGE_CACHE" "$VM_IMAGE"

  qemu-img resize "$VM_IMAGE" 60G >/dev/null
  qm create "$VMID" --name "$HOSTNAME" --ostype l26 \
      --memory 24576 --balloon 24576 \
      --agent 1 \
      --bios ovmf --machine q35 --efidisk0 "$STORAGE:0,pre-enrolled-keys=0" \
      --cpu host --sockets 1 --cores 4 \
      --net0 virtio,bridge=vmbr0 >/dev/null
  qm importdisk "$VMID" "$VM_IMAGE" "$STORAGE" >/dev/null
  qm set "$VMID" \
      --scsihw virtio-scsi-pci \
      --virtio0 "$STORAGE:vm-$VMID-disk-1,discard=on" \
      --ide2 "$STORAGE:cloudinit" >/dev/null
fi

if [[ "$TEMPLATE_MODE" == "true" ]]; then
  VM_TAGS="o11y-workshop,noble,k3d,o11y-k3d-template"
  VM_NOTES=$(cat <<EOF
# Splunk Observability Workshop Template

| Property | Value |
| --- | --- |
| Build mode | **Template build** |
| VM ID/Environment | **$VMID - $ENV_NAME** |
| Hostname | **$HOSTNAME** |
| Operating system | Ubuntu Noble |

## Template flow

This VM installs workshop prerequisites via cloud-init, then powers off.
The script waits for shutdown and converts it into a Proxmox template.

EOF
)
else
  VM_TAGS="o11y-workshop,noble,k3d"
  VM_NOTES=$(cat <<EOF
# Splunk Observability Workshop

| Property | Value |
| --- | --- |
| VM ID/Environment | **$VMID - $ENV_NAME** |
| Hostname | **$HOSTNAME** |
| Operating system | Ubuntu Noble |
| Cluster | **${HOSTNAME}-cluster** |
| Provisioning path | **$( [[ "$USE_TEMPLATE_CLONE" == "true" ]] && echo "Template clone (${TEMPLATE_SOURCE_VMID})" || echo "Full build" )** |

## Access

The VM uses DHCP. Obtain its address from the Proxmox Summary page after the
QEMU guest agent becomes available, then connect with:

\`\`\`bash
ssh $VM_USER@<IP_ADDRESS>
Password: $VM_PASSWORD
\`\`\`

EOF
)
fi

qm set "$VMID" \
  --boot order=virtio0 \
  --cicustom "user=local:snippets/${SNIPPET_NAME}" \
  --tags "$VM_TAGS" \
  --ipconfig0 ip=dhcp \
  --description "$VM_NOTES" >/dev/null
qm cloudinit update "$VMID" >/dev/null

PROVISION_STARTED_AT=$(date +%s)
DISCOVERED_IP=""
WORKSHOP_FAILURE_REASON=""
qm start "$VMID" >/dev/null

if [[ "$TEMPLATE_MODE" == "true" ]]; then
  echo -e "${YW}Template mode: waiting for cloud-init to complete and power off...${CL}"

  if ! wait_for_template_shutdown "$VMID" "$((PROVISION_STARTED_AT + 90 * 60))"; then
    show_workshop_failure "$VMID" "$(format_elapsed $(($(date +%s) - PROVISION_STARTED_AT)))"
    exit 1
  fi

  qm template "$VMID" >/dev/null
  PROVISION_ELAPSED=$(format_elapsed $(($(date +%s) - PROVISION_STARTED_AT)))
  echo -e "${GN}Template ready: VMID ${VMID} (${HOSTNAME})${CL}"
  echo "Template provisioning time: ${PROVISION_ELAPSED}"
else
  PROVISION_DEADLINE=$((PROVISION_STARTED_AT + 60 * 60))

  if ! wait_for_guest_agent "$VMID" "$PROVISION_DEADLINE" || ! wait_for_workshop "$VMID" "$PROVISION_DEADLINE"; then
    show_workshop_failure "$VMID" "$(format_elapsed $(($(date +%s) - PROVISION_STARTED_AT)))"
    exit 1
  fi

  PROVISION_ELAPSED=$(format_elapsed $(($(date +%s) - PROVISION_STARTED_AT)))
  show_workshop_success "$VMID" "$HOSTNAME" "$DISCOVERED_IP" "$PROVISION_ELAPSED"
fi
