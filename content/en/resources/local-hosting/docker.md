---
title: Docker
weight: 4
description: Create a local Splunk Observability Workshop container with Docker.
---

## Docker Workshop Instance Setup

### Overview

`workshop-container.sh` builds and starts an Ubuntu 24.04 container that runs a K3s cluster in Docker through k3d. The container installs the workshop tools and content, configures credentials obtained with a SWiPE ID, and waits until Kubernetes is ready before reporting success.

The script supports:

- Building the workshop image
- Creating the `workshop-k3d` container the first time it is run
- Starting that container again when it is stopped
- Following the container log until you stop watching it

There is no SSH server in this container. The shell is `docker exec`.

### Prerequisites

Run the script on a machine where the Docker engine is already running. The machine requires:

- Permission to start a privileged container
- Internet access to Ubuntu, Docker's apt repository, GitHub, the Kubernetes release site, Helm, HashiCorp, Chaos Mesh, and the Splunk workshop API
- Enough memory for the default cluster: one k3d server and two agents, each with an 8G memory cap
- Free local ports `81`, `82`, `9999`, and `443`
- A valid [SWiPE ID](https://swipe.splunk.show) when the workshop secret should be created

The container is privileged because k3d creates the cluster nodes as containers inside it. The script does not mount the host Docker socket. The Docker engine inside the container listens only on a local Unix socket.

### Quick Start

Clone the workshop repository and run the script from `local-hosting/docker`:

```bash
git clone https://github.com/splunk/observability-workshop
cd observability-workshop/local-hosting/docker
export SWIPE_ID='<swipe-id>'
./workshop-container.sh
```

`SWIPE_ID` is optional. When it is unset, the cluster still starts and `workshop-secret` is not applied.

The first run builds the image and creates the cluster. That takes several minutes. Keep the terminal attached until the log says:

```text
Workshop cluster workshop-cluster is ready.
```

Pressing `Ctrl+C` stops following the log. The container keeps running.

Running `./workshop-container.sh` again builds the image, then starts the existing `workshop-k3d` container if it is stopped. It does not replace a container that already exists. Deleting the container also drops the cluster: the node containers remain in the Docker volume, but the files they mount lived in the deleted container. The next run removes those leftover nodes and creates a new cluster. The volume still holds downloaded images, so that create does not download them again.

```bash
docker rm -f workshop-k3d
./workshop-container.sh
```

### Container specifications

| Property | Value |
| --- | --- |
| Image | `workshop-k3d` |
| Container name | `workshop-k3d` |
| Operating system | Ubuntu 24.04 LTS (Noble) |
| Hostname | `workshop` |
| Cluster | `workshop-cluster`: one k3d server and two agents |
| Node memory cap | `8G` on the server and on each agent |
| Published ports | `81`, `82`, `9999`, `443` |
| Cluster images | Docker volume `workshop-k3d-docker`, mounted at `/var/lib/docker` |
| User | `splunk` |
| Shell | `docker exec -it -u splunk workshop-k3d zsh` |

`WORKSHOP_AGENTS` and `WORKSHOP_NODE_MEMORY` override the cluster shape. `WORKSHOP_AGENTS` is a whole number from `0` to `10` and defaults to `2`. `WORKSHOP_NODE_MEMORY` looks like `8G` or `512M` and defaults to `8G`. Set them in the same shell that runs the script. A container that already exists keeps the cluster that was created for it. These variables apply when that cluster is created.

### What the container installs

The image installs:

- Docker Engine 29.9.3, Docker Compose, and containerd
- k3d v5.9.0 with K3s `rancher/k3s:v1.33.4-k3s1`
- kubectl v1.34.0, Helm v3.22.1, K9s v0.51.0, and Terraform v1.17.1
- Ansible, Python, Git, jq, and a Zsh and Starship shell
- Starship v1.27.0

On first start, the container also:

- Downloads the Splunk Observability Workshop content from the `main` branch into `/home/splunk/workshop`
- Downloads Splunk Observability Content Contrib into `/home/splunk/observability-content-contrib`
- Creates the k3d cluster and publishes container port `80` on host port `81`, plus ports `82`, `9999`, and `443`
- Applies the in-cluster registry from the workshop content
- Installs Chaos Mesh v2.8.0
- Applies `workshop-secret` when `SWIPE_ID` is set

The registry listens on port `9999`. Workshop files and `/var/log/syslog` and `/var/log/auth.log` are mounted into the k3d nodes.

### Startup progress and completion

The log reports these stages:

- Waiting for Docker
- Downloading workshop content, or reporting that the content is already present
- Creating the cluster, or starting the cluster that is already there
- Waiting until every node is `Ready`
- Waiting until the Kubernetes API can validate manifests
- Applying the workshop registry and waiting for its pod
- Installing Chaos Mesh, or reporting that it is already installed
- Fetching the SWiPE workshop and applying `workshop-secret`, when `SWIPE_ID` is set

Success is the line `Workshop cluster workshop-cluster is ready.` The script then prints `http://localhost:81` and the `docker exec` command.

### Accessing the container

```bash
docker exec -it -u splunk workshop-k3d zsh
```

The workshop site is:

```text
http://localhost:81
```

Ports `82`, `9999`, and `443` are published on the same host ports.

### Useful commands

Inside the container:

```bash
# Check Kubernetes nodes
kubectl get nodes

# Inspect all workloads
kubectl get pods --all-namespaces

# Open the Kubernetes terminal interface
k9s

# View workshop materials
ls ~/workshop/
```

From the machine running Docker:

```bash
# Follow the startup log
docker logs -f workshop-k3d

# Start a stopped container without rebuilding
docker start workshop-k3d

# Stop the container. Start it again with docker start or ./workshop-container.sh.
docker stop workshop-k3d
```

### Environment variables

Set these in the shell that runs `workshop-container.sh`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SWIPE_ID` | unset | Workshop ID used to fetch tokens. When unset, `workshop-secret` is skipped. |
| `WORKSHOP_AGENTS` | `2` | Number of k3d agents, from `0` to `10`. |
| `WORKSHOP_NODE_MEMORY` | `8G` | Memory cap for the server and for each agent. |

Inside the container, a SWiPE response is exported under the field names returned by the API. The login environment also sets `RUM_TOKEN` from `RUM`, `API_TOKEN` from `API`, and both `INGEST_TOKEN` and `ACCESS_TOKEN` from `INGEST`. Those values are written to `/home/splunk/.workshop-env` and to `workshop-secret`. They are not stored in the image.

The container also sets:

- `INSTANCE`: `workshop`
- `CLUSTER_NAME`: `workshop-cluster`
- `KUBECONFIG`: `/home/splunk/.kube/config`

The secret's `url` is `http://localhost:81`.

### Troubleshooting

- **Docker is not running**: Start Docker and run `./workshop-container.sh` again.
- **Port already in use**: Free port `81`, `82`, `9999`, or `443`, then remove the failed container with `docker rm -f workshop-k3d` and run the script again.
- **SWiPE ID was not found**: Confirm the ID and export `SWIPE_ID` again before starting a new container. An existing container keeps the environment it was created with.
- **Could not reach the SWiPE API**: Check access to `https://swipe.splunk.show` and run the script again.
- **Cluster create failed**: The script deletes a partial cluster so the next start can create it again. Read the log with `docker logs workshop-k3d`.
- **Could not apply a manifest**: The script waits until the API can validate manifests, then retries the apply. If the container exits before the ready line, start it again with `docker start workshop-k3d` or `./workshop-container.sh`.
- **Cluster fails to start after the container was deleted**: The old node containers are still in the Docker volume, and their `meminfo` mounts point at files that were deleted with the container. Run `./workshop-container.sh` again. It removes those nodes and creates a new cluster.
- **Existing container ignores a new image or a new `SWIPE_ID`**: `docker rm -f workshop-k3d` removes the container. The next run creates a new cluster. Run `./workshop-container.sh` after exporting `SWIPE_ID`.
- **Start over, including the cluster**: Stop and remove the container, then remove the volume.

```bash
docker rm -f workshop-k3d
docker volume rm workshop-k3d-docker
./workshop-container.sh
```
