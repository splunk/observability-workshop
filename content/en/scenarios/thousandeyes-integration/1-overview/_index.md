---
title: Overview
linkTitle: 1. Overview
weight: 1
---

## ThousandEyes Agent Types

### Enterprise Agents

Enterprise Agents are software-based monitoring agents that you deploy within your own infrastructure. They provide:

- **Inside-out visibility**: Monitor and test from your internal network to external services
- **Customizable placement**: Deploy where your users and applications are
- **Full test capabilities**: HTTP, network, DNS, voice, and other test types
- **Persistent monitoring**: Continuously running agents that execute scheduled tests

In this workshop, we're deploying an Enterprise Agent as a containerized workload inside a Kubernetes cluster.

### Endpoint Agents

Endpoint Agents are lightweight agents installed on end-user devices (laptops, desktops) that provide:

- **Real user perspective**: Monitor from actual user endpoints
- **Browser-based monitoring**: Capture real user experience metrics
- **Session data**: Detailed insights into application performance from the user's viewpoint

This workshop focuses on **Enterprise Agent** deployment only.

## Architecture

```mermaid
graph LR
    subgraph k8s["Kubernetes Cluster"]
        secret["Secret<br/>te-creds"]
        agent["ThousandEyes<br/>Enterprise Agent<br/>Pod"]
        
        subgraph apps["Application Pods"]
            api["API Gateway<br/>Pod"]
            payment["Payment Service<br/>Pod"]
            auth["Auth Service<br/>Pod"]
        end
        
        subgraph svcs["Services"]
            api_svc["api-gateway<br/>Service"]
            payment_svc["payment-svc<br/>Service"]
            auth_svc["auth-service<br/>Service"]
        end
        
        api_svc --> api
        payment_svc --> payment
        auth_svc --> auth
        
        secret -.-> agent
        agent -->|"HTTP Tests"| api_svc
        agent -->|"HTTP Tests"| payment_svc
        agent -->|"HTTP Tests"| auth_svc
    end
    
    external["External<br/>Services"]
    
    agent --> external
    
    subgraph te["ThousandEyes Platform"]
        te_cloud["ThousandEyes<br/>Cloud"]
        te_api["API<br/>v7/stream"]
        te_cloud <--> te_api
    end
    
    agent -->|"Test Results"| te_cloud
    
    subgraph splunk["Splunk Observability Cloud"]
        otel["OpenTelemetry<br/>Collector"]
        metrics["Metrics"]
        dashboards["Dashboards"]
        apm["APM/RUM"]
        alerts["Alerts"]
        
        otel --> metrics
        otel --> dashboards
        metrics --> apm
        dashboards --> alerts
    end
    
    te_cloud -->|"OTel/HTTP"| otel
    
    user["DevOps/SRE<br/>Team"]
    user -.-> te_cloud
    user -.-> dashboards
    user -.-> agent
    
    style k8s fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style apps fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style svcs fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style agent fill:#ffeb3b,stroke:#f57c00,stroke-width:2px
    style secret fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style api fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style payment fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style auth fill:#e1bee7,stroke:#7b1fa2,stroke-width:1px
    style api_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style payment_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style auth_svc fill:#ce93d8,stroke:#7b1fa2,stroke-width:1px
    style external fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style te fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style te_cloud fill:#ffecb3,stroke:#f57f17,stroke-width:2px
    style te_api fill:#ffe082,stroke:#f57f17,stroke-width:2px
    style splunk fill:#ff6e40,stroke:#d84315,stroke-width:2px
    style otel fill:#ff8a65,stroke:#d84315,stroke-width:2px
    style metrics fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style dashboards fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style apm fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style alerts fill:#ffccbc,stroke:#d84315,stroke-width:1px
    style user fill:#b2dfdb,stroke:#00695c,stroke-width:2px
```

## Architecture Components

### 1. Kubernetes Cluster

- **Secret (te-creds)**: Stores the base64-encoded `TEAGENT_ACCOUNT_TOKEN` for authentication
- **ThousandEyes Enterprise Agent Pod**:
  - Container image: `thousandeyes/enterprise-agent:latest`
  - Hostname: `te-agent-aleccham` (customizable)
  - Security capabilities: `NET_ADMIN`, `SYS_ADMIN` (required for network testing)
  - Memory allocation: 2GB request, 3.5GB limit
  - Network mode: IPv4 only (configured via `TEAGENT_INET: "4"` environment variable)
  - Image pull policy: `Always` (ensures latest image is pulled)
  - Init command: `/sbin/my_init` (required for proper agent initialization)
- **Internal Services**: Kubernetes workloads including REST APIs, microservices, databases, and gRPC services

### 2. Test Targets

- **Internal Services**: Monitor services within the Kubernetes cluster
- **External Services**: Test external dependencies such as:
  - Payment gateways (Stripe, PayPal)
  - Third-party APIs
  - SaaS applications
  - CDN endpoints
  - Public websites

### 3. ThousandEyes Platform

- **ThousandEyes Cloud**: Central platform for:
  - Agent registration and management
  - Test configuration and scheduling
  - Metrics collection and aggregation
  - Built-in alerting engine
- **ThousandEyes API**: RESTful API (v7/stream endpoint) for programmatic access

### 4. Test Types & Metrics

The Enterprise Agent performs:

- **HTTP/HTTPS tests**: Web page availability, response times, status codes
- **DNS tests**: Resolution time, record validation
- **Network layer tests**: Latency, packet loss, path visualization
- **Voice/RTP tests**: Quality metrics for voice traffic

Metrics collected include:

- HTTP server availability (%)
- Throughput (bytes/s)
- Request duration (seconds)
- Page load completion (%)
- Error codes and failure reasons

### 5. Splunk Observability Cloud Integration

- **OpenTelemetry Collector**: 
  - Endpoint: `https://ingest.{realm}.signalfx.com/v2/datapoint/otlp`
  - Protocol: HTTP or gRPC
  - Format: Protobuf
  - Authentication: `X-SF-Token` header
  - Signal type: Metrics (OpenTelemetry v2)
- **Observability Features**:
  - **Metrics**: Real-time visualization of ThousandEyes data
  - **Dashboards**: Pre-built ThousandEyes dashboard with unified views
  - **APM/RUM Integration**: Correlate synthetic tests with application traces and real user monitoring
  - **Alerting**: Centralized alert management with correlation rules

### 6. Data Flow

1. Agent authenticates using token from Kubernetes Secret
2. Agent runs scheduled tests against internal and external targets
3. Test results sent to ThousandEyes Cloud
4. ThousandEyes streams metrics to Splunk via OpenTelemetry protocol
5. Splunk ingests, processes, and visualizes data in dashboards
6. DevOps/SRE teams monitor dashboards and respond to alerts

## Testing Capabilities

With this deployment, you can:

- ✅ **Test internal services**: Monitor Kubernetes services, APIs, and microservices from within the cluster
- ✅ **Test external dependencies**: Validate connectivity to payment gateways, third-party APIs, and SaaS platforms
- ✅ **Measure performance**: Capture latency, availability, and performance metrics from your cluster's perspective
- ✅ **Troubleshoot issues**: Identify whether problems originate from your infrastructure or external dependencies

{{% notice title="Note" style="info" %}}
This is **not an officially supported** ThousandEyes agent deployment configuration. However, it has been tested and works very well in production-like environments.
{{% /notice %}}
