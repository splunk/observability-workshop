# OpenTelemetry Collector Gateway Configuration

This directory contains Kubernetes manifests for deploying the OpenTelemetry Collector in a **gateway deployment pattern**, where agents send telemetry data to a centralized gateway collector running on a **separate host** before it's forwarded to Splunk Observability Cloud.

## Architecture Overview

```text
┌─────────────────────────────────────┐      ┌──────────────────────────────┐
│     Kubernetes Cluster              │      │    Separate Host             │
│                                     │      │                              │
│  ┌─────────────────┐                │      │  ┌──────────────────┐        │      ┌──────────────────────┐
│  │  Applications   │                │      │  │  OTel Gateway    │        │      │ Splunk Observability │
│  │   & Services    │                │      │  │                  │        │      │       Cloud          │
│  └────────┬────────┘                │      │  │  Standalone      │────────┼─────>│                      │
│           │                         │      │  │  Collector       │        │      │  - Traces (OTLP)     │
│           v                         │      │  │                  │        │      │  - Metrics (SignalFx)│
│  ┌─────────────────┐                │      │  └──────────────────┘        │      │  - Logs (HEC)        │
│  │  OTel Agent     │────────────────┼─────>│                              │      └──────────────────────┘
│  │  (DaemonSet)    │   HTTP         │      │  192.168.5.158               │
│  └─────────────────┘   OTLP         │      │  :4318, :9943, :6060         │
│                                     │      │                              │
└─────────────────────────────────────┘      └──────────────────────────────┘
```

**Key Architecture Points:**

- **OTel Agents** run as DaemonSet in Kubernetes cluster
- **OTel Gateway** runs on a separate host outside the cluster (IP: 192.168.5.158)
- All telemetry flows from agents → gateway → Splunk Cloud
- Gateway acts as a centralized aggregation and processing layer

## Key Differences from Standard Deployment

### 1. Gateway Location

**Standard Configuration:**

- Agents send directly to Splunk public cloud endpoints
- No intermediate gateway

**Gateway Configuration:**

- Agents send to a **separate host** running the gateway collector
- Gateway IP: `192.168.5.158` (external to Kubernetes cluster)
- Gateway then forwards to Splunk public endpoints

### 2. Agent Exporter Configuration

**Standard Configuration (Direct to Splunk):**

```yaml
exporters:
  otlphttp:
    traces_endpoint: "https://ingest.[REALM].signalfx.com/v2/trace/otlp"
    metrics_endpoint: "https://ingest.[REALM].signalfx.com/v2/datapoint/otlp"
  signalfx:
    access_token: ${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}
    realm: ${SPLUNK_REALM}
    ingest_url: "https://ingest.[REALM].signalfx.com"
  splunk_hec/platform_logs:
    endpoint: "[URL]:[PORT]/services/collector/event"
    token: ${SPLUNK_HEC_TOKEN}
```

**Gateway Configuration (Agent to Separate Host):**

```yaml
exporters:
  otlphttp:
    traces_endpoint: "http://192.168.5.158:4318/v1/traces"     # External gateway
    metrics_endpoint: "http://192.168.5.158:4318/v1/metrics"   # External gateway
    logs_endpoint: "http://192.168.5.158:4318/v1/logs"         # External gateway
```

### 3. Environment Variables

**Standard Configuration:**

```yaml
# Points directly to Splunk public endpoints
splunk_trace_url: "https://ingest.[REALM].signalfx.com/v2/trace/otlp"
splunk_api_url: "https://api.[REALM].signalfx.com"
splunk_ingest_url: "https://ingest.[REALM].signalfx.com"
splunk_hec_url: "https://[URL]:[PORT]/services/collector/event"
```

**Gateway Configuration:**

```yaml
# Points to the external gateway host
splunk_otlp_trace_url: "http://192.168.5.158:4318/v1/traces"
splunk_otlp_metric_url: "http://192.168.5.158:4318/v1/metrics"
splunk_otlp_log_url: "http://192.168.5.158:4318/v1/logs"
splunk_api_url: "http://192.168.5.158:6060"
splunk_ingest_url: "http://192.168.5.158:9943"
```

### 4. Data Flow Changes

**Standard Configuration:**

```text
K8s Agents ──────────────────> Splunk Observability Cloud
            (HTTPS, Public)
```

**Gateway Configuration:**

```text
K8s Agents ────────> Gateway Host ────────> Splunk Observability Cloud
         (HTTP, LAN)  192.168.5.158  (HTTPS, Public)
```

- Agents send **all telemetry** (traces, metrics, logs) via OTLP HTTP to the external gateway
- Gateway performs centralized processing and exports to Splunk endpoints
- Single protocol (OTLP) between agents and gateway
- Gateway handles all authentication with Splunk Cloud

### 5. Gateway Receiver Configuration

The gateway (running on separate host) is configured to receive multiple protocols:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: "${SPLUNK_LISTEN_INTERFACE}:4317"    # Listens on gateway host
      http:
        endpoint: "${SPLUNK_LISTEN_INTERFACE}:4318"    # Listens on gateway host
  jaeger:
    protocols:
      grpc:
        endpoint: "${SPLUNK_LISTEN_INTERFACE}:14250"
      thrift_http:
        endpoint: "${SPLUNK_LISTEN_INTERFACE}:14268"
      # ... other Jaeger protocols
  signalfx:
    endpoint: "${SPLUNK_LISTEN_INTERFACE}:9943"
  zipkin:
    endpoint: "${SPLUNK_LISTEN_INTERFACE}:9411"
```

### 6. Gateway Resource Attributes

The gateway adds a specific resource attribute to identify itself:

```yaml
processors:
  resource/add_mode:
    attributes:
      - action: insert
        value: "gateway"
        key: otelcol.service.mode
```

## Benefits of External Gateway Deployment

1. **Reduced Egress Costs**: Single point of egress to Splunk Cloud instead of each Kubernetes node
2. **Network Isolation**: Keep Splunk credentials off Kubernetes cluster
3. **Centralized Processing**: Complex processing (sampling, filtering, enrichment) done at gateway
4. **Simplified Agent Configuration**: Agents use lightweight configuration, send to local network
5. **Better Resource Utilization**: Gateway can run on dedicated hardware, scaled independently
6. **Enhanced Security**: Splunk access tokens only stored on gateway host, not in cluster secrets
7. **Protocol Flexibility**: Gateway can receive multiple protocols and normalize to Splunk formats
8. **Cross-Cluster Aggregation**: Multiple Kubernetes clusters can send to the same gateway
9. **Reduced TLS Overhead**: Agent-to-gateway uses HTTP on trusted LAN, gateway handles HTTPS to cloud

## Deployment Components

### Gateway Collector (Separate Host - 192.168.5.158)

- **Config**: `gateway_config.yaml`
- **Location**: Runs on separate host outside Kubernetes
- **Purpose**: Receives telemetry from agents and forwards to Splunk Observability Cloud
- **Ports**:
  - 4317 (OTLP gRPC)
  - 4318 (OTLP HTTP) - **Primary port used by agents**
  - 9943 (SignalFx)
  - 6060 (HTTP Forwarder)

### Agent (Kubernetes DaemonSet)

- **File**: `daemonset.yaml`
- **ConfigMap**: `configmap-agent.yaml`
- **Purpose**: Runs on each Kubernetes node to collect telemetry
- **Exports to**: External gateway at 192.168.5.158

### Cluster Receiver (Kubernetes Deployment)

- **File**: `deployment-cluster-receiver.yaml`
- **ConfigMap**: `configmap-cluster-receiver.yaml`
- **Purpose**: Collects cluster-level metrics (single replica)

### Configuration & Secrets

- **File**: `configmap-and-secrets.yaml`
- **Contains**: External gateway endpoints and access tokens (for agents only)

## Configuration Steps

### 1. Deploy Gateway on Separate Host

On the gateway host (192.168.5.158), install the Splunk OpenTelemetry Collector:

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm eu0 -- <ACCESS_TOKEN> --mode gateway
```

### 2. Update Gateway Endpoints in ConfigMap

Edit `configmap-and-secrets.yaml` to point to your gateway host IP:

```yaml
data:
  splunk_otlp_trace_url: "http://192.168.5.158:4318/v1/traces"
  splunk_otlp_metric_url: "http://192.168.5.158:4318/v1/metrics"
  splunk_otlp_log_url: "http://192.168.5.158:4318/v1/logs"
  splunk_api_url: "http://192.168.5.158:6060"
  splunk_ingest_url: "http://192.168.5.158:9943"
  k8s_cluster_name: "your-cluster-name"
  deployment_environment: "your-environment"
```

**Important:** Update the IP address if your gateway is on a different host!

## Performance Considerations

### High Availability Options

- Deploy multiple gateway hosts with load balancer
- Use DNS round-robin for gateway endpoint
- Configure agent retry logic for failover

### Batching and Buffering

- Gateway batches data before forwarding (see `batch` processor in `gateway_config.yaml`)
- Adjust batch size based on network latency and throughput
- Memory limiter prevents OOM on gateway host
