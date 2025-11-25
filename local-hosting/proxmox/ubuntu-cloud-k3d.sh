#!/usr/bin/env bash
export TERM=xterm-256color

apt update -qq
apt install jq curl -y -qq

function header_info() {
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

YW=$(echo "\033[33m")
BL=$(echo "\033[36m")
HA=$(echo "\033[1;34m")
RD=$(echo "\033[01;31m")
BGN=$(echo "\033[4;92m")
GN=$(echo "\033[1;92m")
DGN=$(echo "\033[32m")
CL=$(echo "\033[m")

if whiptail --backtitle "Splunk" --title "Observability Workshop VM" --yesno "This will create a Observability Workshop VM. Proceed?" 10 58; then
  :
else
  header_info && echo -e "${RD}User exited script${CL}\n" && exit
fi

if SWIPE_ID=$(whiptail --backtitle "Splunk" --title "SWiPE ID" --inputbox "Enter your SWiPE ID:" 10 58 3>&1 1>&2 2>&3); then
  #SWIPE_ID=$REPLY
  if [[ -n "$SWIPE_ID" ]]; then
    echo -e "SWiPE ID: ${YW}${SWIPE_ID}${CL}"
  else
    header_info && echo -e "${RD}Invalid SWiPE ID. Exiting script.${CL}\n" && exit
  fi
else
  header_info && echo -e "${RD}User exited script${CL}\n" && exit
fi

if ENV_NAME=$(whiptail --backtitle "Splunk" --title "Environment Name" --inputbox "Enter environment name (default: workshop):" 10 58 3>&1 1>&2 2>&3); then
  if [[ -z "$ENV_NAME" ]]; then
    ENV_NAME="workshop"
  fi
  echo -e "Environment: ${YW}${ENV_NAME}${CL}"
else
  header_info && echo -e "${RD}User exited script${CL}\n" && exit
fi

if whiptail --backtitle "Splunk" --title "Demo-in-a-Box Version" --yesno "Use staging version of demo-in-a-box?\n\nYes = Staging\nNo = Production" 12 58; then
  DIAB_VERSION="staging"
  echo -e "Demo-in-a-Box Version: ${YW}Staging${CL}"
else
  DIAB_VERSION="production"
  echo -e "Demo-in-a-Box Version: ${YW}Production${CL}"
fi

# Call the API and store the response
JSON_RESPONSE=$(curl -s https://swipe.splunk.show/api?id=${SWIPE_ID})

# Check if Workshop ID not found
if [[ "$JSON_RESPONSE" == '{"message":"Workshop ID not found"}' ]]; then
  header_info && echo -e "${RD}Workshop ID not found. Exiting script.${CL}\n" && exit
fi

# Parse the JSON response and extract values
REALM=$(echo ${JSON_RESPONSE} | jq -r '.REALM')
RUM_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.RUM')
INGEST_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.INGEST')
API_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.API')
HEC_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.HEC_TOKEN')
HEC_URL=$(echo ${JSON_RESPONSE} | jq -r '.HEC_URL')

NEXTID=$(pvesh get /cluster/nextid)

UNIQUE_HOST_ID=$(echo $RANDOM | md5sum | head -c 4)
RANDOM_ADDITION=$((4000 + RANDOM % 1001))
VMID=$((NEXTID))
STORAGE=local-lvm
HOSTNAME=$VMID-$ENV_NAME-$UNIQUE_HOST_ID
USER=splunk
PASSWORD=Splunk123!
LATEST_K9S_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | jq -r '.tag_name')
LATEST_TERRAFORM_VERSION=$(curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest | jq -r '.tag_name | ltrimstr("v")')

echo -e "Hostname: ${YW}${HOSTNAME}${CL}\n"
#set -x

cat << EOF | tee /var/lib/vz/snippets/k3d.yaml >/dev/null
#cloud-config
package_update: true
package_upgrade: false
package_reboot_if_required: false

hostname: $HOSTNAME
manage_etc_hosts: true
fqdn: $HOSTNAME
user: $USER
password: $PASSWORD
chpasswd:
  expire: False
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
ssh_pwauth: True

packages:
  - bash
  - ansible
  - ca-certificates
  - curl
  - gnupg
  - jq
  - maven
  - net-tools
  - openjdk-17-jdk
  - python3-venv
  - python3-pip
  - unzip
  - zsh
  - git
  - wget
  - qemu-guest-agent
write_files:
  - path: /etc/sysctl.conf
    append: true
    content: |
      # Increase inotify limits
      fs.inotify.max_user_watches=524288
      fs.inotify.max_user_instances=8192

  - path: /etc/environment
    append: true
    content: |
      # Splunk environment variables
      export TERM=xterm-256color
      export RUM_TOKEN="$RUM_TOKEN"
      export ACCESS_TOKEN="$INGEST_TOKEN"
      export API_TOKEN="$API_TOKEN"
      export HEC_TOKEN="$HEC_TOKEN"
      export HEC_URL="$HEC_URL"
      export REALM="$REALM"

      INSTANCE="$HOSTNAME"
      CLUSTER_NAME="$HOSTNAME-cluster"

      export INSTANCE CLUSTER_NAME

      export KUBECONFIG=/home/splunk/.kube/config
      alias kc='kubectl'
      alias dc='docker-compose'

  - path: /tmp/workshop-secrets.yaml
    permissions: '0755'
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
        deployment: "deployment.environment=$HOSTNAME-workshop"
        realm: $REALM
        access_token: $INGEST_TOKEN
        api_token: $API_TOKEN
        rum_token: $RUM_TOKEN
        hec_token: $HEC_TOKEN
        hec_url: $HEC_URL
        url: http://$HOSTNAME

runcmd:
  - systemctl start qemu-guest-agent
  - systemctl enable qemu-guest-agent

  # Install Docker from official repository
  - export DEBIAN_FRONTEND=noninteractive
  - install -m 0755 -d /etc/apt/keyrings
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  - chmod a+r /etc/apt/keyrings/docker.gpg
  - |
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  - apt-get update -qq
  - apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  - usermod -aG docker splunk

  #- chsh -s $(which zsh) splunk
  #- echo "source /etc/skel/.profile" >> /home/splunk/.zshrc

  # Install Helm
  - curl -s https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

  # Install K9s (Kubernetes UI) - Version: ${LATEST_K9S_VERSION}
  - curl -S -OL https://github.com/derailed/k9s/releases/download/${LATEST_K9S_VERSION}/k9s_Linux_amd64.tar.gz
  - tar xfz k9s_Linux_amd64.tar.gz -C /usr/local/bin/ k9s

  # Download Workshop
  - curl -s -OL https://github.com/splunk/observability-workshop/archive/main.zip
  - unzip -qq main.zip -d /home/splunk/
  - mkdir /home/splunk/workshop
  - mv /home/splunk/observability-workshop-main/workshop/* /home/splunk/workshop
  - mv /home/splunk/workshop/ansible/diab-v3.yml /home/splunk
  - rm -rf /home/splunk/observability-workshop-main
  - rm -rf /home/splunk/workshop/aws /home/splunk/workshop/cloud-init /home/splunk/workshop/ansible

  # Copy staging version of demo-in-a-box if selected and available
  - |
    if [ "$DIAB_VERSION" = "staging" ] && [ -f /home/splunk/workshop/k3s/demo-in-a-box-staging.zip ]; then
      cp /home/splunk/workshop/k3s/demo-in-a-box-staging.zip /home/splunk/workshop/k3s/demo-in-a-box.zip
    fi
  - mv /home/splunk/workshop/k3s/demo-in-a-box.zip /home/splunk

  # Download Splunk Observability Content Contrib Repo
  - curl -s -L https://github.com/splunk/observability-content-contrib/archive/main.zip -o content-contrib.zip
  - unzip -qq content-contrib.zip -d /home/splunk/
  - mv /home/splunk/observability-content-contrib-main /home/splunk/observability-content-contrib

  # Install Terraform (latest) - Version: ${LATEST_TERRAFORM_VERSION}
  - curl -S -OL https://releases.hashicorp.com/terraform/${LATEST_TERRAFORM_VERSION}/terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip
  - unzip -qq terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin

  # Install kubectl
  - curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  - install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   
  # Install k3d
  - curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

  # Create 3 node k3d cluster
  - k3d cluster create ${HOSTNAME}-cluster --agents 2 --agents-memory 6G --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@server:0" --k3s-arg "--kubelet-arg=eviction-hard=memory.available<1Gi@agent:*" --image rancher/k3s:v1.33.4-k3s1 --port "80:80@loadbalancer" --port "81:80@loadbalancer" --port "82:82@loadbalancer" --port "9999:9999@loadbalancer" -v /home/splunk:/home/splunk -v /var/log/syslog:/var/log/syslog -v /var/log/auth.log:/var/log/auth.log

  # Create k3d kube config and set correct permissions on splunk user home directory
  - mkdir /home/splunk/.kube && k3d kubeconfig get ${HOSTNAME}-cluster > /home/splunk/.kube/config
  - chmod 400 /home/splunk/.kube/config
  - chown -R splunk:splunk /home/splunk

  # Deploy private registry
  - /usr/local/bin/kubectl apply -f /home/splunk/workshop/k3s/registry/registry.yaml

  # Chaos Mesh
  - curl -sSL https://mirrors.chaos-mesh.org/v2.8.0/install.sh | bash -s -- --k3s

  # Deploy Splunk secrets
  - /usr/local/bin/kubectl apply -f /tmp/workshop-secrets.yaml

  # Increase inotify limits for k3s
  - sysctl -w fs.inotify.max_user_watches=524288
  - sysctl -w fs.inotify.max_user_instances=8192

EOF

#qm destroy $VMID >/dev/null
rm -f noble-server-cloudimg-amd64.img >/dev/null
wget -q https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
qemu-img resize noble-server-cloudimg-amd64.img 40G >/dev/null
qm create $VMID --name $HOSTNAME --ostype l26 \
    --memory 16384 --balloon 0 \
    --agent 1 \
    --bios ovmf --machine q35 --efidisk0 $STORAGE:0,pre-enrolled-keys=0 \
    --cpu host --socket 1 --cores 4 \
    --net0 virtio,bridge=vmbr0 >/dev/null
qm importdisk $VMID noble-server-cloudimg-amd64.img $STORAGE >/dev/null
qm set $VMID --scsihw virtio-scsi-pci --virtio0 $STORAGE:vm-$VMID-disk-1,discard=on >/dev/null
qm set $VMID --boot order=virtio0 >/dev/null
qm set $VMID --ide2 $STORAGE:cloudinit >/dev/null

qm set $VMID --cicustom "user=local:snippets/k3d.yaml" >/dev/null
qm set $VMID --tags o11y-workshop,noble,k3d >/dev/null
#qm set $VMID --ciuser ubuntu
#qm set $VMID --cipassword Splunk123!
#qm set $VMID --ciupdate 0
qm set $VMID --ipconfig0 ip=dhcp >/dev/null
qm cloudinit update $VMID >/dev/null
#qm template $VMID
qm start $VMID >/dev/null