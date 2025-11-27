---
title: Cilium Installation
weight: 4
---

## Step 1: Configure Cilium Enterprise

Create a file named `cilium-enterprise-values.yaml`. Replace `<YOUR-EKS-API-SERVER-ENDPOINT>` with the endpoint from the previous step (without `https://` prefix):

```yaml
# Configure unique cluster name & ID
cluster:
  name: isovalent-demo
  id: 0

# Configure ENI specifics
eni:
  enabled: true
  updateEC2AdapterLimitViaAPI: true
  awsEnablePrefixDelegation: true

enableIPv4Masquerade: false
loadBalancer:
  serviceTopology: true

ipam:
  mode: eni

routingMode: native

# BPF / KubeProxyReplacement
kubeProxyReplacement: "true"
k8sServiceHost: <YOUR-EKS-API-SERVER-ENDPOINT>
k8sServicePort: 443

# Configure TLS configuration
tls:
  ca:
    certValidityDuration: 3650 # 10 years

# Enable Cilium Hubble for visibility
hubble:
  enabled: true
  metrics:
    enableOpenMetrics: true
    enabled:
      - dns:labelsContext=source_namespace,destination_namespace
      - drop:labelsContext=source_namespace,destination_namespace
      - tcp:labelsContext=source_namespace,destination_namespace
      - port-distribution:labelsContext=source_namespace,destination_namespace
      - icmp:labelsContext=source_namespace,destination_namespace
      - flow:sourceContext=workload-name|reserved-identity
      - "httpV2:exemplars=true;labelsContext=source_namespace,destination_namespace"
      - "policy:labelsContext=source_namespace,destination_namespace"
    serviceMonitor:
      enabled: true
  tls:
    enabled: true
    auto:
      enabled: true
      method: cronJob
      certValidityDuration: 1095 # 3 years
  relay:
    enabled: true
    tls:
      server:
        enabled: true
    prometheus:
      enabled: true
      serviceMonitor:
        enabled: true
  timescape:
    enabled: true

# Enable Cilium Operator metrics
operator:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Enable Cilium Agent metrics
prometheus:
  enabled: true
  serviceMonitor:
    enabled: true

# Configure Cilium Envoy
envoy:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Enable DNS Proxy HA support
extraConfig:
  external-dns-proxy: "true"

enterprise:
  featureGate:
    approved:
      - DNSProxyHA
      - HubbleTimescape
```

{{% notice title="Configuration Highlights" style="info" %}}
- **ENI Mode**: Pods get native VPC IP addresses
- **Kube-Proxy Replacement**: eBPF-based service load balancing
- **Hubble**: Network observability with L7 visibility
- **Timescape**: Historical network flow storage
{{% /notice %}}

## Step 2: Install Cilium Enterprise

Install Cilium using Helm:

```bash
helm install cilium isovalent/cilium --version 1.18.4 \
  --namespace kube-system -f cilium-enterprise-values.yaml
```

{{% notice title="Note" style="warning" %}}
The installation may initially show pending jobs. This is expected - proceed to create nodes.
{{% /notice %}}

## Step 3: Create Node Group

Create a file named `nodegroup.yaml`:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: isovalent-demo
  region: us-east-1
managedNodeGroups:
- name: standard
  instanceType: m5.xlarge
  desiredCapacity: 2
  privateNetworking: true
```

Create the node group (this takes 5-10 minutes):

```bash
eksctl create nodegroup -f nodegroup.yaml
```

## Step 4: Verify Cilium Installation

Once nodes are ready, verify all components:

```bash
# Check nodes
kubectl get nodes

# Check Cilium pods
kubectl get pods -n kube-system -l k8s-app=cilium

# Check all Cilium components
kubectl get pods -n kube-system | grep -E "(cilium|hubble)"
```

**Expected Output:**
- 2 nodes in `Ready` state
- Cilium pods running (1 per node)
- Hubble relay and timescape running
- Cilium operator running

## Step 5: Install Tetragon

Install Tetragon for runtime security:

```bash
helm install tetragon isovalent/tetragon --version 1.18.0 \
  --namespace tetragon --create-namespace
```

Verify installation:

```bash
kubectl get pods -n tetragon
```

**What you'll see:** Tetragon runs as a DaemonSet (one pod per node) plus an operator.

## Step 6: Install Cilium DNS Proxy HA

Create a file named `cilium-dns-proxy-ha-values.yaml`:

```yaml
enableCriticalPriorityClass: true
metrics:
  serviceMonitor:
    enabled: true
```

Install DNS Proxy HA:

```bash
helm upgrade -i cilium-dnsproxy isovalent/cilium-dnsproxy --version 1.16.7 \
  -n kube-system -f cilium-dns-proxy-ha-values.yaml
```

Verify:

```bash
kubectl rollout status -n kube-system ds/cilium-dnsproxy --watch
```

{{% notice title="Success" style="success" %}}
You now have a fully functional EKS cluster with Cilium CNI, Hubble observability, and Tetragon security!
{{% /notice %}}
