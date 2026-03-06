---
title: Cilium Installation
weight: 4
---

## Step 1: Configure Cilium Enterprise

Create a file named `cilium-enterprise-values.yaml`. Replace `<YOUR-EKS-API-SERVER-ENDPOINT>` with the endpoint from the previous step (without the `https://` prefix).

```yaml
# Enable/disable debug logging
debug:
  enabled: false
  verbose: ~

# Configure unique cluster name & ID
cluster:
  name: isovalent-demo
  id: 0

# Configure ENI specifics
eni:
  enabled: true
  updateEC2AdapterLimitViaAPI: true   # Dynamically fetch ENI limits from EC2 API
  awsEnablePrefixDelegation: true     # Assign /28 CIDR blocks per ENI (16 IPs) instead of individual IPs

enableIPv4Masquerade: false           # Pods use their real VPC IPs — no SNAT needed in ENI mode
loadBalancer:
  serviceTopology: true               # Prefer backends in the same AZ to reduce cross-AZ traffic costs

ipam:
  mode: eni

routingMode: native                   # No overlay tunnels — traffic routes natively through VPC

# BPF / KubeProxyReplacement
# Cilium replaces kube-proxy entirely with eBPF programs in the kernel.
# This requires a direct path to the API server, hence k8sServiceHost.
kubeProxyReplacement: "true"
k8sServiceHost: <YOUR-EKS-API-SERVER-ENDPOINT>
k8sServicePort: 443

# TLS for internal Cilium communication
tls:
  ca:
    certValidityDuration: 3650        # 10 years for the CA cert

# Hubble: network observability built on top of Cilium's eBPF datapath
hubble:
  enabled: true
  metrics:
    enableOpenMetrics: true           # Use OpenMetrics format for better Prometheus compatibility
    enabled:
      # DNS: query/response tracking with namespace-level label context
      - dns:labelsContext=source_namespace,destination_namespace
      # Drop: packet drop reasons (policy deny, invalid, etc.) per namespace
      - drop:labelsContext=source_namespace,destination_namespace
      # TCP: connection state tracking (SYN, FIN, RST) per namespace
      - tcp:labelsContext=source_namespace,destination_namespace
      # Port distribution: which destination ports are being used
      - port-distribution:labelsContext=source_namespace,destination_namespace
      # ICMP: ping/traceroute visibility with workload identity context
      - icmp:labelsContext=source_namespace,destination_namespace;sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity
      # Flow: per-workload flow counters (forwarded, dropped, redirected)
      - flow:sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity
      # HTTP L7: request/response metrics with full workload context and exemplars for trace correlation
      - "httpV2:exemplars=true;labelsContext=source_ip,source_namespace,source_workload,destination_namespace,destination_workload,traffic_direction;sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity"
      # Policy: network policy verdict tracking (allowed/denied) per workload
      - "policy:sourceContext=app|workload-name|pod|reserved-identity;destinationContext=app|workload-name|pod|dns|reserved-identity;labelsContext=source_namespace,destination_namespace"
      # Flow export: enables Hubble to export flow records to Timescape for historical storage
      - flow_export
    serviceMonitor:
      enabled: true                   # Creates a Prometheus ServiceMonitor for auto-discovery
  tls:
    enabled: true
    auto:
      enabled: true
      method: cronJob                 # Automatically rotate Hubble TLS certs on a schedule
      certValidityDuration: 1095      # 3 years per cert rotation
  relay:
    enabled: true                     # Hubble Relay aggregates flows from all nodes cluster-wide
    tls:
      server:
        enabled: true
    prometheus:
      enabled: true
      serviceMonitor:
        enabled: true
  timescape:
    enabled: true                     # Stores historical flow data for time-travel debugging

# Cilium Operator: cluster-wide identity and endpoint management
operator:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Cilium Agent: per-node eBPF datapath metrics
prometheus:
  enabled: true
  serviceMonitor:
    enabled: true

# Cilium Envoy: L7 proxy metrics (HTTP, gRPC)
envoy:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Enable the Cilium agent to hand off DNS proxy responsibilities to the
# external DNS Proxy HA deployment, so policies keep working during upgrades
extraConfig:
  external-dns-proxy: "true"

# Enterprise feature gates — these must be explicitly approved
enterprise:
  featureGate:
    approved:
      - DNSProxyHA          # High-availability DNS proxy (installed separately)
      - HubbleTimescape     # Historical flow storage via Timescape
```

{{% notice title="Why label contexts matter" style="info" %}}
The `labelsContext` and `sourceContext`/`destinationContext` parameters on each Hubble metric control what dimensions the metric is broken down by. Setting `labelsContext=source_namespace,destination_namespace` means every metric will have those two labels attached, letting you filter by namespace in Splunk without cardinality explosion. The `workload-name|reserved-identity` fallback chain means Cilium will use the workload name if available, falling back to the security identity if not.
{{% /notice %}}

## Step 2: Install Cilium Enterprise

When a new node joins an EKS cluster, the kubelet on that node immediately starts looking for a CNI plugin to set up networking. It reads whatever CNI configuration is present in `/etc/cni/net.d/` and uses that to initialize the node. **If we create the node group first, the AWS VPC CNI is what gets there first** — and once a node has initialized with one CNI, switching to another requires draining and re-initializing the node.

By installing Cilium before any nodes exist, we ensure that Cilium's CNI configuration is already present in `kube-system` and ready to be picked up the moment a node starts. When the EC2 instances boot, Cilium's DaemonSet pod is scheduled immediately, its eBPF programs are loaded, and the node comes up `Ready` under Cilium's control from the very first second.

This is also why the cluster was created with `disableDefaultAddons: true` in Step 3 of the EKS setup — without that, the AWS VPC CNI would be installed automatically and would race against Cilium.

Install Cilium using Helm:

```bash
helm install cilium isovalent/cilium --version 1.18.4 \
  --namespace kube-system -f cilium-enterprise-values.yaml
```

{{% notice title="Pending jobs are expected" style="warning" %}}
After installation you'll see some jobs in a pending state — this is normal. Cilium's Helm chart includes a job that generates TLS certificates for Hubble, and that job needs a node to run on. It will complete automatically once nodes are available in the next step.
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

## Step 5: Install Tetragon with Enhanced Network Observability

Tetragon out of the box provides runtime security and process-level visibility. For the Splunk integration — especially the Network Explorer dashboards — you also want to enable its enhanced network observability mode, which tracks TCP/UDP socket statistics, RTT, connection events, and DNS at the kernel level.

Create a file named `tetragon-network-values.yaml`:

```yaml
# Tetragon configuration with Enhanced Network Observability enabled
# Required for Splunk Observability Cloud Network Explorer integration

tetragon:
  # Enable network events — this activates eBPF-based socket tracking
  enableEvents:
    network: true

  # Layer3 settings: track TCP, UDP, and ICMP with RTT and latency
  # These enable the socket stats metrics (srtt, retransmits, bytes, etc.)
  layer3:
    tcp:
      enabled: true
      rtt:
        enabled: true     # Round-trip time per TCP flow
    udp:
      enabled: true
    icmp:
      enabled: true
    latency:
      enabled: true       # Per-connection latency tracking

  # DNS tracking at the kernel level (complements Hubble DNS metrics)
  dns:
    enabled: true

  # Expose Tetragon metrics via Prometheus
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

  # Filter out noise from internal system namespaces — we only care about
  # application workloads, not the observability stack itself
  exportDenyList: |-
    {"health_check":true}
    {"namespace":["", "cilium", "tetragon", "kube-system", "otel-splunk"]}

  # Only include labels that are meaningful for the Network Explorer
  metricsLabelFilter: "namespace,workload,binary"

  resources:
    limits:
      cpu: 500m
      memory: 1Gi
    requests:
      cpu: 100m
      memory: 256Mi

# Enable the Tetragon Operator and TracingPolicy support.
# With tracingPolicy.enabled: true, the operator manages and deploys
# TracingPolicies (TCP connection tracking, HTTP visibility, etc.) automatically.
tetragonOperator:
  enabled: true
  tracingPolicy:
    enabled: true
```

Install Tetragon with these values:

```bash
helm install tetragon isovalent/tetragon --version 1.18.0 \
  --namespace tetragon --create-namespace \
  -f tetragon-network-values.yaml
```

Verify installation:

```bash
kubectl get pods -n tetragon
```

**What you'll see:** Tetragon runs as a DaemonSet (one pod per node) plus an operator.

{{% notice title="What Enhanced Network Observability adds" style="info" %}}
With `layer3.tcp.rtt.enabled: true`, Tetragon hooks into the kernel's TCP socket state and records per-connection metrics including round-trip time, retransmit counts, bytes sent/received, and segment counts. These feed the `tetragon_socket_stats_*` metrics that power latency and throughput views in Splunk's Network Explorer. Without this, you only get event counts — with it, you get connection quality data.

TracingPolicies (TCP connection tracking, HTTP visibility, etc.) are managed automatically by the Tetragon Operator when `tetragonOperator.tracingPolicy.enabled: true` is set in the Helm values above.
{{% /notice %}}

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
