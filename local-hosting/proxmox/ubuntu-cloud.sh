#!/bin/bash

VMID=8100
STORAGE=local-lvm
HOSTNAME=workshop-1
USER=splunk
PASSWORD=Splunk123!
LATEST_K9S_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | jq -r '.tag_name')
LATEST_TERRAFORM_VERSION=$(curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest | jq -r '.tag_name | ltrimstr("v")')

set -x

cat << EOF | tee /var/lib/vz/snippets/ubuntu.yaml
#cloud-config
package_update: true
package_upgrade: true
package_reboot_if_required: true

hostname: $HOSTNAME
manage_etc_hosts: true
fqdn: $HOSTNAME
manage_etc_hosts: true
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
  - docker
  - docker-buildx
  - curl
  - docker-compose
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

runcmd:
  - systemctl start qemu-guest-agent
  - systemctl enable qemu-guest-agent

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
  - mv /home/splunk/workshop/k3s/demo-in-a-box.zip /home/splunk
  
  # Download Splunk Observability Content Contrib Repo
  - curl -s -L https://github.com/splunk/observability-content-contrib/archive/main.zip -o content-contrib.zip
  - unzip -qq content-contrib.zip -d /home/splunk/
  - mv /home/splunk/observability-content-contrib-main /home/splunk/observability-content-contrib
  
  # Install Terraform (latest) - Version: ${LATEST_TERRAFORM_VERSION}
  - curl -S -OL https://releases.hashicorp.com/terraform/${LATEST_TERRAFORM_VERSION}/terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip
  - unzip -qq terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
  
  # Install K3s
  - curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -
  
  # Create kube config and set correct permissions on splunk user home directory
  - mkdir /home/splunk/.kube && kubectl config view --raw > /home/splunk/.kube/config
  - chmod 400 /home/splunk/.kube/config
  - chown -R splunk:splunk /home/splunk
  
  # Deploy private registry
  - /usr/local/bin/kubectl apply -f /home/splunk/workshop/k3s/registry/registry.yaml
  
  # Chaos Mesh
  - curl -sSL https://mirrors.chaos-mesh.org/v2.7.1/install.sh | bash -s -- --k3s
EOF

qm destroy $VMID
rm -f jammy-server-cloudimg-amd64.img
wget -q https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img 
qemu-img resize jammy-server-cloudimg-amd64.img 8G
qm create $VMID --name "ubuntu-jammy-template" --ostype l26 \
    --memory 4096 --balloon 0 \
    --agent 1 \
    --bios ovmf --machine q35 --efidisk0 $STORAGE:0,pre-enrolled-keys=0 \
    --cpu host --socket 1 --cores 2 \
    --net0 virtio,bridge=vmbr0
qm importdisk $VMID jammy-server-cloudimg-amd64.img $STORAGE
qm set $VMID --scsihw virtio-scsi-pci --virtio0 $STORAGE:vm-$VMID-disk-1,discard=on
qm set $VMID --boot order=virtio0
qm set $VMID --ide2 $STORAGE:cloudinit

qm set $VMID --cicustom "user=local:snippets/ubuntu.yaml"
qm set $VMID --tags o11y-workshop,jammy,cloudinit
#qm set $VMID --ciuser ubuntu 
#qm set $VMID --cipassword Splunk123!
qm set $VMID --ciupdate 0
qm set $VMID --ipconfig0 ip=dhcp
qm cloudinit update $VMID
qm template $VMID
