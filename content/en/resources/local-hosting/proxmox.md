---
title: Proxmox
weight: 3
description: Create a local Splunk Observability Workshop VM on Proxmox VE.
---

## Proxmox Workshop Instance Setup

### Overview

The `ubuntu-cloud-k3d.sh` script creates an Ubuntu 24.04 VM containing a three-node K3s cluster running in Docker through k3d. It installs the workshop tools and content, configures credentials obtained with a SWiPE ID, and waits until Kubernetes is ready before reporting success.

The script supports:

- Creating a workshop VM from the Ubuntu cloud image
- Creating a workshop VM by cloning a compatible Proxmox template
- Building a reusable workshop template
- Interactive and non-interactive execution

### Prerequisites

Run the script from a root shell on a Proxmox VE host. The host requires:

- Internet access to Ubuntu, GitHub, Docker, Kubernetes, Helm, HashiCorp, Chaos Mesh, and the Splunk workshop API
- At least 24 GiB of available memory and 4 CPU cores for each running workshop VM
- At least 60 GiB of available VM storage
- A `vmbr0` bridge with DHCP connectivity
- An available VM ID
- A valid SWiPE ID when creating a workshop VM
- Snippet support enabled on the Proxmox `local` storage

To enable snippets:

1. In the Proxmox web interface, go to **Datacenter → Storage → local**.
2. Select **Edit**.
3. Add **Snippets** under **Content**.
4. Select **OK**.

The script stores its generated cloud-init file under `/var/lib/vz/snippets` and attaches it as `local:snippets/...`.

### Quick Start

Run the current k3d script directly on the Proxmox host:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh)"
```

The older k3s script remains available for legacy environments, but is not recommended for new workshop VMs:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3s.sh)"
```

### Interactive Flow

The script displays the following choices:

1. **Choose Action**
   - **Create a ready-to-use workshop VM** is the default.
   - **Build a reusable Proxmox template** is intended for advanced users.
2. **SWiPE ID** when creating a workshop VM.
3. **Environment Name**, with `workshop` as the default.
4. **Demo-in-a-Box Version**
   - **Production** is the default and recommended option.
   - **Staging** is intended for testing and development.
5. **Provisioning Method**, shown only when a compatible template exists.
   - Clone an existing template for the fastest creation.
   - Perform a full build from the Ubuntu cloud image.
6. **Final Confirmation**, showing the VM ID, resources, storage, network, content version, and provisioning method.

Pressing **Esc** or selecting **Cancel** stops the script without creating a VM. Cancelling template selection does not silently start a full build.

### VM Specifications

A full build creates the following VM:

| Property | Value |
| --- | --- |
| Operating system | Ubuntu 24.04 LTS (Noble) |
| CPU | 4 cores using the host CPU type |
| Memory | 24 GiB |
| Disk | 60 GiB |
| Firmware | UEFI using OVMF and q35 |
| Network | VirtIO on `vmbr0`, configured with DHCP |
| Default storage | `local-lvm` |
| User | `splunk` |
| Password | `Splunk123!` |
| SSH | Password authentication enabled |

A cloned VM inherits its CPU, memory, disks, and network hardware from the selected template. The script supplies new cloud-init configuration and requests a new DHCP address.

### Storage Behavior

The script currently hardcodes `local-lvm` for new VM disks:

```bash
STORAGE=local-lvm
```

There is no command-line storage option. The full-build path also expects the imported disk naming used by `local-lvm`, so changing only the `STORAGE` variable is not guaranteed to work with directory, NFS, Ceph, or ZFS storage.

To develop and test support for another storage backend, download the script before running it:

```bash
curl -fsSLo ubuntu-cloud-k3d.sh https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh
chmod +x ubuntu-cloud-k3d.sh
```

Update `STORAGE` and the associated `qm importdisk` and `qm set --virtio0` handling for the target backend, then run the local copy:

```bash
./ubuntu-cloud-k3d.sh
```

The cloud-init snippet continues to use `local` storage, so `local` must still support **Snippets** even if VM-disk support for another backend is added.

#### LVM thin-pool over-provisioning warning

When using `local-lvm`, Proxmox may display a warning similar to:

```text
WARNING: Sum of all thin volume sizes exceeds the size of thin pool pve/data
and the amount of free space in volume group.
```

LVM thin provisioning allows the virtual sizes of all disks to exceed the physical thin-pool capacity. The warning does not necessarily mean the pool is currently full, but it means the pool cannot hold every virtual disk if all disks grow to their configured sizes.

Check physical usage and advertised virtual capacity with:

```bash
pvesm status
vgs --units g -o vg_name,vg_size,vg_free
lvs -a --units g -o lv_name,vg_name,lv_size,data_percent,metadata_percent,pool_lv,origin
```

To remove the warning, use one or more of the following approaches:

- Move workshop VM disks to storage with sufficient capacity.
- Delete unused VMs, containers, templates, snapshots, or disks after confirming they are no longer required.
- Add physical storage to the volume group and extend the thin pool.
- Add and test support in the script for a suitable NFS, Ceph, ZFS, or directory-backed storage target.

Do not hide the warning by redirecting standard error. A full LVM thin pool can cause VM I/O failures and data loss.

### What the Script Installs

Cloud-init installs and configures:

- Docker Engine, Docker Compose, and containerd
- k3d with a three-node K3s cluster: one server and two agents
- kubectl, Helm, and K9s
- OpenJDK 17, Maven, Python, Git, Ansible, and Terraform
- Chaos Mesh
- A private Kubernetes container registry exposed on port `9999`
- Splunk Observability Workshop content
- Splunk Observability Content Contrib
- A Zsh and Starship shell environment

The VM exposes ports `80`, `81`, `82`, `443`, and `9999` through the k3d load balancer.

The script pins k3d to `v5.9.0`, K3s to `v1.33.4-k3s1`, kubectl to `v1.34.0`, and Chaos Mesh to `v2.8.0`. K9s and Terraform are resolved from their latest GitHub releases when a full image or template is built. The Chaos Mesh installer is checksum-verified before it runs.

### Provisioning Progress and Completion

After starting the VM, the script waits for the QEMU Guest Agent and displays progress reported by the guest, including:

- Configuring the shell environment
- Installing Docker
- Installing Kubernetes tools
- Downloading workshop content
- Caching Kubernetes images for a template, when building a template
- Using the reusable workshop template, when creating a clone
- Starting Docker
- Creating the k3d cluster
- Importing cached workshop images, when creating a VM from a template
- Deploying workshop services
- Checking Kubernetes readiness
- Finalizing the workshop VM
- Waiting for cloud-init finalization

For a workshop VM, success is reported only after:

- All three Kubernetes nodes report `Ready`.
- The workshop registry pod reports `Ready`.
- The Chaos Mesh controller and dashboard deployments complete their rollouts.
- The Chaos Mesh daemon set completes its rollout.
- Cloud-init reports `status: done`.

The final output includes:

- Actual provisioning time
- VM ID and hostname
- DHCP address reported by QEMU Guest Agent
- Exact SSH command
- Workshop endpoint URLs
- Useful health-check commands

Keep the terminal attached until the script reports success or failure. Workshop provisioning has a one-hour host-side timeout. Template provisioning has a 90-minute timeout while waiting for installation and shutdown.

### Accessing the VM

Use the address printed by the script:

```bash
ssh splunk@<vm-ip>
```

The default password is:

```text
Splunk123!
```

The main workshop endpoints are:

```text
http://<vm-ip>
http://<vm-ip>:81
http://<vm-ip>:82
```

### Useful Commands

Inside the VM:

```bash
# Check Kubernetes nodes
kubectl get nodes

# Inspect all workloads
kubectl get pods --all-namespaces

# Open the Kubernetes terminal interface
k9s

# View workshop materials
ls ~/workshop/

# Check the managed k3d service
systemctl status k3d-cluster.service
```

From the Proxmox host:

```bash
# Check guest-reported workshop status
qm guest exec <vmid> -- /usr/local/sbin/workshop-status

# View the workshop provisioning log
qm guest exec <vmid> -- tail -n 200 /var/log/o11y-workshop-provision.log

# Check cloud-init status
qm guest exec <vmid> -- cloud-init status --long

# View cloud-init output
qm guest exec <vmid> -- tail -n 200 /var/log/cloud-init-output.log

# Retrieve guest network interfaces
qm agent <vmid> network-get-interfaces
```

When provisioning fails, the script preserves the VM and prints these commands automatically.

### Reusable Templates

Select **Build a reusable Proxmox template** from the first menu to create a base image. Template builds:

- Do not request or embed SWiPE credentials.
- Install the reusable workshop prerequisites and content.
- Download and checksum-verify the pinned Chaos Mesh installer.
- Cache the K3s and k3d load-balancer images with retry handling.
- Create a temporary one-server k3d cache cluster.
- Pull the registry and Chaos Mesh images into that temporary cluster in parallel.
- Export the cached service images to `/opt/o11y-workshop-cache/workshop-images.tar`.
- Delete the temporary cache cluster, so the template contains no reusable Kubernetes cluster state.
- Clear provisioning markers, cloud-init state, and machine identity before shutdown.
- Power off after provisioning.
- Convert the stopped VM to a Proxmox template.
- Add the `o11y-k3d-template` tag.

While a template is being built, the host displays guest-reported stages and stops early if the guest reports a provisioning failure. A failed VM is preserved for troubleshooting instead of being converted into a template.

During later workshop creation, templates carrying the `o11y-k3d-template` tag are offered as fast clone sources. The clone receives current SWiPE credentials and a unique hostname, creates a new three-node k3d cluster during its first boot, and imports the cached service images into all three nodes before deploying the workshop services.

### Non-interactive Usage

Pass script arguments through `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh | \
  bash -s -- \
    --non-interactive \
    --mode normal \
    --swipe-id <swipe-id> \
    --env-name workshop \
    --diab-version production \
    --use-template-clone no
```

To clone a specific compatible template, add:

```text
--use-template-clone yes --template-vmid <template-vmid>
```

To create a reusable template:

```bash
curl -fsSL https://raw.githubusercontent.com/splunk/observability-workshop/refs/heads/main/local-hosting/proxmox/ubuntu-cloud-k3d.sh | \
  bash -s -- \
    --non-interactive \
    --mode template \
    --template-name o11y-k3d-template
```

#### Command-line options

| Option | Values and behavior |
| --- | --- |
| `--non-interactive` | Disables all whiptail prompts and uses command-line values or defaults. |
| `--assume-yes` | Skips only the final confirmation in interactive mode. Other interactive questions are still shown. |
| `--mode` | `normal` or `template`; defaults to `normal` in non-interactive mode. |
| `--swipe-id` | Required for a non-interactive normal workshop VM. |
| `--env-name` | Workshop environment name; defaults to `workshop`. |
| `--diab-version` | `production` or `staging`; defaults to `production`. |
| `--use-template-clone` | `yes` or `no`; defaults to `no` in non-interactive mode. |
| `--template-vmid` | Selects a tagged compatible template when template cloning is enabled. |
| `--template-name` | Name used in template mode; defaults to `o11y-k3d-template`. |
| `--help`, `-h` | Prints the supported command-line syntax and exits. |

If non-interactive cloning is enabled without `--template-vmid`, the script uses the first compatible tagged template returned by Proxmox. If the requested template cannot be found, the script reports the issue and falls back to a full build.

### Environment Variables

Workshop VMs configure:

- `RUM_TOKEN`: Real User Monitoring token
- `ACCESS_TOKEN`: Data ingest token retained for backward compatibility
- `INGEST_TOKEN`: Data ingest token
- `API_TOKEN`: Splunk API token
- `HEC_TOKEN`: HTTP Event Collector token
- `HEC_URL`: HTTP Event Collector endpoint
- `REALM`: Splunk realm
- `INSTANCE`: Unique VM hostname
- `CLUSTER_NAME`: k3d cluster name
- `KUBECONFIG`: `/home/splunk/.kube/config`

### Troubleshooting

- **Invalid SWiPE ID**: Confirm the ID is active and retry.
- **QEMU Guest Agent timeout**: Open the VM console and inspect `/var/log/cloud-init-output.log`.
- **Waiting for cloud-init finalization**: The workshop steps have finished, but the script is waiting for cloud-init itself to report `done`. Check `cloud-init status --long` if this persists.
- **Cloud-init reported an error**: Run `qm guest exec <vmid> -- cloud-init status --long` and inspect `/var/log/cloud-init-output.log` and `/var/log/o11y-workshop-provision.log`.
- **Workshop provisioning failure**: Run the host-side status and log commands shown above.
- **Template provisioning failure**: The VM is intentionally preserved. Use the status and provisioning-log commands printed by the script before retrying or deleting it.
- **No DHCP address**: Verify that `vmbr0` reaches a network with DHCP and inspect `qm agent <vmid> network-get-interfaces`.
- **VM creation failure**: Check the selected storage, snippet support, free capacity, VM ID availability, and Proxmox task log.
- **Template not offered**: Confirm that it is a Proxmox template and carries the `o11y-k3d-template` tag.
- **Image download failure**: Template image pulls retry up to five times with increasing delays. Confirm Docker Hub and GitHub Container Registry connectivity if all attempts fail.
- **Chaos Mesh installation failure**: Confirm access to GitHub and GHCR. The script rejects the installer if its SHA-256 checksum does not match the pinned value.
- **LVM thin-pool warning**: Move disks, reclaim unused virtual capacity, expand the pool, or select a larger storage target as described above.

### Tags

Workshop VMs use the tags `o11y-workshop`, `noble`, and `k3d`.

Reusable templates also use the `o11y-k3d-template` tag.
