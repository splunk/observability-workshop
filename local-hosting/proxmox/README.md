# Proxmox Workshop Instance Setup

## Overview

The `ubuntu-cloud.sh` script automates the creation of a Splunk Observability Workshop VM on Proxmox VE. It creates a complete Ubuntu 22.04 cloud-init based VM with all necessary tools and configurations pre-installed.

## Prerequisites

- Proxmox VE cluster with administrative access
- Internet connectivity for downloading cloud images and packages
- Available VM ID range and storage space
- Valid SWiPE ID for workshop access

## K3s Quick Start

Run the script directly on your Proxmox host:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3s.sh)"
```

Or download and run locally:

```bash
wget https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3s.sh
chmod +x ubuntu-cloud-k3s.sh
./ubuntu-cloud-k3s.sh
```

## K3d Quick Start

Run the script directly on your Proxmox host:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh)"
```

Or download and run locally:

```bash
wget https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh
chmod +x ubuntu-cloud-k3d.sh
./ubuntu-cloud-k3d.sh
```

## What the Script Does

### 1. Initial Setup

- Updates package repositories and installs required tools (`jq`, `curl`)
- Displays interactive prompts for user confirmation and SWiPE ID, environment name, DNS server and DNS domain input

### 2. Authentication & Configuration

- Validates SWiPE ID against the Splunk workshop API
- Retrieves workshop tokens and configuration (REALM, RUM_TOKEN, INGEST_TOKEN, etc.)
- Generates unique VM ID and hostname based on user input

### 3. VM Creation

- Downloads Ubuntu 24.04 Noble cloud image
- Resizes disk to 20GB
- Creates Proxmox VM with:
  - **Memory**: 16GB RAM
  - **CPU**: 4 cores (host CPU type)
  - **Storage**: Uses `local-lvm` storage
  - **Network**: Bridged to `vmbr0` with DHCP
  - **Boot**: UEFI with cloud-init support

### 4. Software Installation

The cloud-init configuration automatically installs:

- **Container Tools**: Docker, Docker Compose
- **Kubernetes**: K3s/K3d, kubectl, Helm, K9s
- **Development**: OpenJDK 17, Maven, Python3, Git
- **Infrastructure**: Terraform, Ansible
- **Monitoring**: Chaos Mesh

### 5. Workshop Content

- Downloads Splunk Observability Workshop materials
- Sets up Kubernetes secrets with workshop tokens
- Configures private container registry
- Prepares demo applications and content

## Environment Variables

The script configures these environment variables in the VM:

- `RUM_TOKEN`: Real User Monitoring token
- `ACCESS_TOKEN`: Data ingest token  
- `API_TOKEN`: Splunk API token
- `HEC_TOKEN`: HTTP Event Collector token
- `HEC_URL`: HEC endpoint URL
- `REALM`: Splunk realm
- `INSTANCE`: Unique hostname
- `CLUSTER_NAME`: Kubernetes cluster name

## Accessing the VM

1. Wait for VM creation and boot to complete (5-10 minutes)
2. Find the VM's IP address in Proxmox console or DHCP logs
3. SSH to the VM:

   ```bash
   ssh splunk@<vm-ip>
   # Password: Splunk123!
   ```

## Troubleshooting

- **Invalid SWiPE ID**: Verify your workshop registration and ID
- **VM creation fails**: Check Proxmox storage space and permissions
- **Network issues**: Ensure `vmbr0` bridge is properly configured
- **Slow deployment**: Allow extra time for cloud-init to complete all installations

## Tags

Created VMs are tagged with: `o11y-workshop`, `noble`, `k3s` or `k3d` for easy identification in Proxmox.
