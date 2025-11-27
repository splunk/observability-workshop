---
title: EKS Setup
weight: 3
---

## Step 1: Add Helm Repositories

Add the required Helm repositories:

```bash
# Add Isovalent Helm repository
helm repo add isovalent https://helm.isovalent.com

# Add Splunk OpenTelemetry Collector Helm repository
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

# Update Helm repositories
helm repo update
```

## Step 2: Create EKS Cluster Configuration

Create a file named `cluster.yaml`:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: isovalent-demo
  region: us-east-1
  version: "1.30"
iam:
  withOIDC: true
addonsConfig:
  disableDefaultAddons: true
addons:
- name: coredns
```

**Key Configuration Details:**

- `disableDefaultAddons: true` - Disables AWS VPC CNI and kube-proxy (Cilium will replace both)
- `withOIDC: true` - Enables IAM roles for service accounts (required for Cilium to manage ENIs)
- `coredns` addon is retained as it's needed for DNS resolution

{{% notice title="Why Disable Default Addons?" style="info" %}}
Cilium provides its own CNI implementation using eBPF, which is more performant than the default AWS VPC CNI. By disabling the defaults, we avoid conflicts and let Cilium handle all networking.
{{% /notice %}}

## Step 3: Create the EKS Cluster

Create the cluster (this takes approximately 15-20 minutes):

```bash
eksctl create cluster -f cluster.yaml
```

Verify the cluster is created:

```bash
# Update kubeconfig
aws eks update-kubeconfig --name isovalent-demo --region us-east-1

# Check pods
kubectl get pods -n kube-system
```

**Expected Output:**
- CoreDNS pods will be in `Pending` state (this is normal - they're waiting for the CNI)
- No worker nodes yet

{{% notice title="Note" style="warning" %}}
Without a CNI plugin, pods cannot get IP addresses or network connectivity. CoreDNS will remain pending until Cilium is installed.
{{% /notice %}}

## Step 4: Get Kubernetes API Server Endpoint

You'll need this for the Cilium configuration:

```bash
aws eks describe-cluster --name isovalent-demo --region us-east-1 \
  --query 'cluster.endpoint' --output text
```

Save this endpoint - you'll use it in the Cilium installation step.

## Step 5: Install Prometheus CRDs

Cilium uses Prometheus ServiceMonitor CRDs for metrics:

```bash
kubectl apply -f https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.68.0/stripped-down-crds.yaml
```

{{% notice title="Next Steps" style="success" %}}
With the EKS cluster created, you're ready to install Cilium, Hubble, and Tetragon.
{{% /notice %}}
