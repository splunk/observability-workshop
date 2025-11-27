# Configuration Examples

This directory contains the configuration files used during the deployment of Isovalent Enterprise Platform with Splunk Observability Cloud integration.

## Files Overview

### EKS Cluster Configuration
- **cluster.yaml** - Initial EKS cluster configuration
- **nodegroup.yaml** - Node group configuration

### Cilium Enterprise Configuration
- **cilium-enterprise-values.yaml** - Main Cilium Enterprise Helm values
- **cilium-dns-proxy-ha-values.yaml** - DNS Proxy HA Helm values

### Splunk OpenTelemetry Configuration
- **splunk-otel-isovalent.yaml** - Splunk OpenTelemetry Collector Helm values with Isovalent metrics receivers and metric filtering

### Splunk Observability Cloud Dashboards
- **Cilium by Isovalent.json** - Pre-built dashboard for Cilium metrics (agent status, ENI allocation, BPF map pressure)
- **Hubble by Isovalent.json** - Pre-built dashboard for Hubble metrics (network flows, DNS queries, dropped packets)

## Required Placeholders

Before using these configuration files, you **must** replace the following placeholders with your actual values:

### 1. EKS API Server Endpoint
**File:** `cilium-enterprise-values.yaml`  
**Placeholder:** `<YOUR-EKS-API-SERVER-ENDPOINT>`  
**Location:** Line 28 (`k8sServiceHost`)

**How to get it:**
```bash
kubectl cluster-info | grep 'Kubernetes control plane' | awk '{print $NF}' | sed 's|https://||'
```

**Example value:**
```
79F5FA6349FF9D1DC9052A3140032E7A.gr7.us-east-1.eks.amazonaws.com
```

### 2. Splunk Access Token
**File:** `splunk-otel-isovalent.yaml`  
**Placeholder:** `<YOUR-SPLUNK-ACCESS-TOKEN>`  
**Field:** `splunkObservability.accessToken`

**How to get it:**
1. Log into Splunk Observability Cloud
2. Navigate to **Settings** > **Access Tokens**
3. Create a new token with **INGEST** permissions or use an existing one

**Security note:** Keep this token secure. Do not commit it to version control.

### 3. Splunk Realm
**File:** `splunk-otel-isovalent.yaml`  
**Placeholder:** `<YOUR-SPLUNK-REALM>`  
**Field:** `splunkObservability.realm`

**How to find it:**
1. Log into Splunk Observability Cloud
2. Navigate to **Settings** > **Account**
3. Your realm is displayed (e.g., `us0`, `us1`, `eu0`, `ap0`)

**Common realms:**
- `us0` - US East (N. Virginia)
- `us1` - US East (Ohio)
- `eu0` - Europe (Frankfurt)
- `ap0` - Asia Pacific (Tokyo)

## Usage

After replacing the placeholders, use these files with the commands documented in the main [README.md](../README.md):

```bash
# Create EKS cluster
eksctl create cluster -f examples/cluster.yaml

# Add node group
eksctl create nodegroup -f examples/nodegroup.yaml

# Install Cilium Enterprise
helm upgrade --install cilium isovalent/cilium \
  --version 1.18.4 \
  --namespace kube-system \
  -f examples/cilium-enterprise-values.yaml

# Install DNS Proxy HA
helm upgrade --install cilium-dns-proxy-ha isovalent/cilium-dns-proxy-ha \
  --version 1.18.0 \
  --namespace kube-system \
  -f examples/cilium-dns-proxy-ha-values.yaml

# Install Splunk OpenTelemetry Collector
helm upgrade --install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace otel-splunk \
  --create-namespace \
  -f examples/splunk-otel-isovalent.yaml
```

## Metric Filtering

The `splunk-otel-isovalent.yaml` file includes a `filter/includemetrics` processor that limits which metrics are sent to Splunk Observability Cloud. This processor uses **strict include semantics**: only metrics explicitly listed in `metric_names` are forwarded; all other metrics are dropped. This is essential to:

- **Prevent metric explosion**: Cilium, Hubble, and Tetragon can generate hundreds of metrics
- **Control costs**: Splunk charges based on metrics volume (MTS - Metric Time Series)
- **Focus on key indicators**: Only send metrics that provide actionable insights

**Default filtered metrics include:**
- Container and pod resource metrics (CPU, memory, restarts)
- Cilium networking metrics (endpoints, BPF maps, policies, API limiter)
- Hubble observability metrics (flows, DNS, HTTP, drops)
- Tetragon security metrics (processes, HTTP, DNS, sockets)

**Customizing the filter:**
Edit the `metric_names` list under `processors.filter/includemetrics` to add or remove metrics based on your monitoring requirements. Use `kubectl exec` to view available metrics:

```bash
# View all Cilium metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9962/metrics | grep "^cilium_"

# View all Hubble metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9965/metrics | grep "^hubble_"

# View all Tetragon metrics
kubectl exec -n tetragon ds/tetragon -- curl -s localhost:2112/metrics | grep "^tetragon_"
```

## Customization

Feel free to modify these files to match your environment:

- Change cluster name and region in `cluster.yaml` and `nodegroup.yaml`
- Adjust instance types and capacity in `nodegroup.yaml`
- Modify Hubble metrics in `cilium-enterprise-values.yaml`
- Update cluster name in `splunk-otel-isovalent.yaml` to match your deployment
- Customize the metric filter list in `splunk-otel-isovalent.yaml` based on your monitoring needs

## Security Best Practices

1. **Never commit sensitive values** to version control
2. Use **environment variables** or **secret management tools** (e.g., AWS Secrets Manager, HashiCorp Vault) for credentials
3. Rotate access tokens regularly
4. Use **principle of least privilege** for IAM roles and service accounts
5. Enable **audit logging** in both EKS and Splunk Observability Cloud
