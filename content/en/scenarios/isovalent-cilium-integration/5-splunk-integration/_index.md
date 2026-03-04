---
title: Splunk Integration
weight: 5
---

## Overview

The Splunk OpenTelemetry Collector uses Prometheus receivers to scrape metrics from all Isovalent components. Each component exposes metrics on different ports, and because Cilium and Hubble share the same pods (just different ports), we configure separate receivers for each one rather than relying on pod annotations.

| Component | Port | What it provides |
|-----------|------|------------------|
| Cilium Agent | 9962 | eBPF datapath, policy enforcement, IPAM, BPF map stats |
| Cilium Envoy | 9964 | L7 proxy metrics (HTTP, gRPC) |
| Cilium Operator | 9963 | Cluster-wide identity and endpoint management |
| Hubble | 9965 | Network flows, DNS, HTTP L7, TCP flags, policy verdicts |
| Tetragon | 2112 | Runtime security, socket stats, network flow events |

## Step 1: Create Configuration File

Create a file named `splunk-otel-collector-values.yaml`. Replace the credential placeholders with your actual values.

```yaml
terminationGracePeriodSeconds: 30
agent:
  config:
    extensions:
      # k8s_observer watches the Kubernetes API for pod and port changes.
      # This enables automatic service discovery without static endpoint lists.
      k8s_observer:
        auth_type: serviceAccount
        observe_pods: true

    receivers:
      kubeletstats:
        collection_interval: 30s
        insecure_skip_verify: true

      # Cilium Agent (port 9962) and Hubble (port 9965) both run in the
      # same DaemonSet pod, identified by label k8s-app=cilium.
      # We use two separate scrape jobs because they're on different ports.
      prometheus/isovalent_cilium:
        config:
          scrape_configs:
            - job_name: 'cilium_metrics_9962'
              scrape_interval: 30s
              metrics_path: /metrics
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_label_k8s_app]
                  action: keep
                  regex: cilium
                - source_labels: [__meta_kubernetes_pod_ip]
                  target_label: __address__
                  replacement: ${__meta_kubernetes_pod_ip}:9962
                - target_label: job
                  replacement: 'cilium_metrics_9962'
            - job_name: 'hubble_metrics_9965'
              scrape_interval: 30s
              metrics_path: /metrics
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_label_k8s_app]
                  action: keep
                  regex: cilium
                - source_labels: [__meta_kubernetes_pod_ip]
                  target_label: __address__
                  replacement: ${__meta_kubernetes_pod_ip}:9965
                - target_label: job
                  replacement: 'hubble_metrics_9965'

      # Cilium Envoy uses a different pod label (k8s-app=cilium-envoy)
      prometheus/isovalent_envoy:
        config:
          scrape_configs:
            - job_name: 'envoy_metrics_9964'
              scrape_interval: 30s
              metrics_path: /metrics
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_label_k8s_app]
                  action: keep
                  regex: cilium-envoy
                - source_labels: [__meta_kubernetes_pod_ip]
                  target_label: __address__
                  replacement: ${__meta_kubernetes_pod_ip}:9964
                - target_label: job
                  replacement: 'cilium_metrics_9964'

      # Cilium Operator is a Deployment (not DaemonSet), identified by io.cilium.app=operator
      prometheus/isovalent_operator:
        config:
          scrape_configs:
            - job_name: 'cilium_operator_metrics_9963'
              scrape_interval: 30s
              metrics_path: /metrics
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_label_io_cilium_app]
                  action: keep
                  regex: operator
                - target_label: job
                  replacement: 'cilium_metrics_9963'

      # Tetragon is identified by app.kubernetes.io/name=tetragon
      prometheus/isovalent_tetragon:
        config:
          scrape_configs:
            - job_name: 'tetragon_metrics_2112'
              scrape_interval: 30s
              metrics_path: /metrics
              kubernetes_sd_configs:
                - role: pod
              relabel_configs:
                - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_name]
                  action: keep
                  regex: tetragon
                - source_labels: [__meta_kubernetes_pod_ip]
                  target_label: __address__
                  replacement: ${__meta_kubernetes_pod_ip}:2112
                - target_label: job
                  replacement: 'tetragon_metrics_2112'

    processors:
      # Strict allowlist filter: only forward metrics we've explicitly named.
      # Without this, Cilium and Tetragon can generate thousands of metric series
      # and overwhelm Splunk Observability Cloud with cardinality.
      filter/includemetrics:
        metrics:
          include:
            match_type: strict
            metric_names:
            # --- Kubernetes base metrics ---
            - container.cpu.usage
            - container.memory.rss
            - k8s.container.restarts
            - k8s.pod.phase
            - node_namespace_pod_container
            - tcp.resets
            - tcp.syn_timeouts

            # --- Cilium Agent metrics ---
            # API rate limiting — detect if the agent is being throttled
            - cilium_api_limiter_processed_requests_total
            - cilium_api_limiter_processing_duration_seconds
            # BPF map utilization — alerts when eBPF maps are near capacity
            - cilium_bpf_map_ops_total
            # Controller health — tracks background reconciliation tasks
            - cilium_controllers_group_runs_total
            - cilium_controllers_runs_total
            # Endpoint state — how many pods are in each lifecycle state
            - cilium_endpoint_state
            # Agent error/warning counts — early warning for problems
            - cilium_errors_warnings_total
            # IP address allocation tracking
            - cilium_ip_addresses
            - cilium_ipam_capacity
            # Kubernetes event processing rate
            - cilium_kubernetes_events_total
            # L7 policy enforcement (HTTP, DNS, Kafka)
            - cilium_policy_l7_total
            # DNS proxy latency histogram — key metric for catching DNS saturation
            - cilium_proxy_upstream_reply_seconds_bucket

            # --- Hubble metrics ---
            # DNS query and response counts — primary indicator in the demo scenario
            - hubble_dns_queries_total
            - hubble_dns_responses_total
            # Packet drops by reason (policy_denied, invalid, TTL_exceeded, etc.)
            - hubble_drop_total
            # Total flows processed — overall network activity volume
            - hubble_flows_processed_total
            # HTTP request latency histogram and total count
            - hubble_http_request_duration_seconds_bucket
            - hubble_http_requests_total
            # ICMP traffic tracking
            - hubble_icmp_total
            # Policy verdict counts (forwarded vs. dropped by policy)
            - hubble_policy_verdicts_total
            # TCP flag tracking (SYN, FIN, RST) — connection lifecycle visibility
            - hubble_tcp_flags_total

            # --- Tetragon metrics ---
            # Total eBPF events processed
            - tetragon_events_total
            # DNS cache health
            - tetragon_dns_cache_evictions_total
            - tetragon_dns_cache_misses_total
            - tetragon_dns_total
            # HTTP response tracking with latency
            - tetragon_http_response_total
            - tetragon_http_stats_latency_bucket
            - tetragon_http_stats_latency_count
            - tetragon_http_stats_latency_sum
            # Layer3 errors
            - tetragon_layer3_event_errors_total
            # TCP socket statistics — per-connection RTT, retransmits, byte/segment counts
            # These power the latency and throughput views in Network Explorer
            - tetragon_socket_stats_retransmitsegs_total
            - tetragon_socket_stats_rxsegs_total
            - tetragon_socket_stats_srtt_count
            - tetragon_socket_stats_srtt_sum
            - tetragon_socket_stats_txbytes_total
            - tetragon_socket_stats_txsegs_total
            - tetragon_socket_stats_rxbytes_total
            # UDP statistics
            - tetragon_socket_stats_udp_retrieve_total
            - tetragon_socket_stats_udp_txbytes_total
            - tetragon_socket_stats_udp_txsegs_total
            - tetragon_socket_stats_udp_rxbytes_total
            # Network flow events (connect, close, send, receive)
            - tetragon_network_connect_total
            - tetragon_network_close_total
            - tetragon_network_send_total
            - tetragon_network_receive_total

      resourcedetection:
        detectors: [system]
        system:
          hostname_sources: [os]

    service:
      pipelines:
        metrics:
          receivers:
            - prometheus/isovalent_cilium
            - prometheus/isovalent_envoy
            - prometheus/isovalent_operator
            - prometheus/isovalent_tetragon
            - hostmetrics
            - kubeletstats
            - otlp
          processors:
            - filter/includemetrics
            - resourcedetection

autodetect:
  prometheus: true

clusterName: isovalent-demo

splunkObservability:
  accessToken: <YOUR-SPLUNK-ACCESS-TOKEN>
  realm: <YOUR-SPLUNK-REALM>           # e.g. us1, us2, eu0
  profilingEnabled: true

cloudProvider: aws
distribution: eks
environment: isovalent-demo

# Gateway mode runs a central collector deployment that receives from all agents.
# Agents send to the gateway, which handles batching and export to Splunk.
# This reduces the number of direct connections to Splunk's ingest endpoint.
gateway:
  enabled: true
  resources:
    requests:
      cpu: 250m
      memory: 512Mi
    limits:
      cpu: 1
      memory: 1Gi

# certmanager handles mTLS between the OTel Collector agent and gateway
certmanager:
  enabled: true
```

**Important:** Replace:
- `<YOUR-SPLUNK-ACCESS-TOKEN>` with your Splunk Observability Cloud access token
- `<YOUR-SPLUNK-REALM>` with your realm (e.g., us1, us2, eu0)

{{% notice title="Why we use a strict metric allowlist" style="info" %}}
Cilium can emit thousands of unique metric series when you factor in all the label combinations for workloads, namespaces, and protocol details. Without the `filter/includemetrics` allowlist, a busy cluster can easily generate 50,000+ active series and overwhelm Splunk's ingestion. The list above is curated to include exactly the metrics that power the Cilium and Hubble dashboards, plus the Tetragon socket stats needed for Network Explorer. If you add new dashboards later, you can add metrics to this list.
{{% /notice %}}

{{% notice title="What Tetragon socket stats enable" style="info" %}}
The `tetragon_socket_stats_*` metrics are what make per-connection latency and throughput analysis possible in Splunk's Network Explorer. `srtt_count`/`srtt_sum` give you average TCP round-trip time per workload. `retransmitsegs_total` surfaces packet loss and congestion. `txbytes`/`rxbytes` show bandwidth per connection. None of this is visible through APM or standard infrastructure metrics.
{{% /notice %}}

## Step 2: Install Splunk OpenTelemetry Collector

Install the collector:

```bash
helm upgrade --install splunk-otel-collector \
  splunk-otel-collector-chart/splunk-otel-collector \
  -n otel-splunk --create-namespace \
  -f splunk-otel-isovalent.yaml
```

Wait for rollout to complete:

```bash
kubectl rollout status daemonset/splunk-otel-collector-agent -n otel-splunk --timeout=60s
```

## Step 3: Verify Metrics Collection

Check that the collector is scraping metrics:

```bash
kubectl logs -n otel-splunk -l app=splunk-otel-collector --tail=100 | grep -i "cilium\|hubble\|tetragon"
```

You should see log entries indicating successful scraping of each component.

{{% notice title="Next Steps" style="success" %}}
Metrics are now flowing to Splunk Observability Cloud! Proceed to verification to check the dashboards.
{{% /notice %}}
