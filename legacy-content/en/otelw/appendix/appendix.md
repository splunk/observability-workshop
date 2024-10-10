---
title:  Helpful Tips
weight: 1
---

## Ubuntu Virtual Machine  

[Multipass](http://multipass.run) deploys and runs Ubuntu virtual machines easily on Mac and Windows.  

Make sure multipass is the CURRENT version:

```bash
brew upgrade multipass
```

Workshop examples have been tested on this configuration:

```bash
multipass launch -n primary -d 16G -m 6G
```

Make sure to always run `sudo apt-get -y update` before executing any step in the workshop.

## K8s Cluster Setup Hints

K3s is a lightweight Kubernetes deployment from Rancher: [https://k3s.io/](https://k3s.io/)

To K3s install on Linux:

```bash
curl -sfL https://get.k3s.io | sh -
```

Make a `.kube` directory in your home directory and create the `config` file e.g.:

```bash
mkdir /home/splunk/.kube && kubectl config view --raw > /home/splunk/.kube/config
```

Set the correct permissions and owndership on the newly created `config` file e.g.:

```bash
chmod 400 /home/splunk/.kube/config
chown -R ubuntu:ubuntu /home/splunk
```

The stock configuration of K3s and this workshop's K8s examples have been tested on the following configurations:  

* [K3s](http://k3s.io) cluster (default settings) on Ubuntu VM:
  1. Macbook Pro 32GB RAM, Windows 10 Laptop 12GB RAM: [Multipass](http://multipass.run) started with `multipass launch -n primary -d 8G -m 4G`  
  2. AWS EC2
  
The Kubernetes lab has also been tested on:

* Azure: Kubernetes 1.17.9 Azure Kubernetes Service
* EKS / GKE: Not tested yet but 99.9% chance will have no issues  
* Workshop will NOT work on: Macbook Pro Docker Desktop Kubernetes

To tear down a Multipass VM:

```bash
multipass delete primary --purge
```

## Using tmux

`tmux` is recommended to split your terminal into several panes so that you can run an application in each pane without having to containerize applications- and you can keep a separate pane open for checking status of spans, the host, etc.

**Important: each pane runs as its own bash shell so environment variables must be set in each pane. The workshop includes setup shell scripts to make it easy to do this.**

To install tmux:

```bash
sudo apt-get install tmux
```

Tmux works by using ++ctrl+b++ as a command key followed by:
`"` make a new horizontal pane
`%` make a new vertical pane
Arrow keys: move between panes.
