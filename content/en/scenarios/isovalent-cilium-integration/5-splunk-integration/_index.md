---
title: Splunk Integration
weight: 5
---

## Overview

The Splunk OpenTelemetry Collector uses Prometheus receivers to scrape metrics from all Isovalent components. Each component exposes metrics on different ports:

| Component | Port | Metrics |
|-----------|------|---------|
| Cilium Agent | 9962 | CNI, networking, policy |
| Cilium Envoy | 9964 | L7 proxy metrics |
| Cilium Operator | 9963 | Cluster operations |
| Hubble | 9965 | Network flows, DNS, HTTP |
| Tetragon | 2112 | Runtime security events |

## Step 1: Create Configuration File

Create a file named `splunk-otel-isovalent.yaml` with your Splunk credentials:

```yaml
agent:
  config:
    receivers:
      prometheus/isovalent_cilium:
        config:
          scrape_configs:
          - job_name: 'cilium_metrics_9962'
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
          - job_name: 'hubble_metrics_9965'
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
      prometheus/isovalent_envoy:
        config:
          scrape_configs:
          - job_name: 'envoy_metrics_9964'
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
      prometheus/isovalent_operator:
        config:
          scrape_configs:
          - job_name: 'cilium_operator_metrics_9963'
            metrics_path: /metrics
            kubernetes_sd_configs:
            - role: pod
            relabel_configs:
            - source_labels: [__meta_kubernetes_pod_label_io_cilium_app]
              action: keep
              regex: operator
      prometheus/isovalent_tetragon:
        config:
          scrape_configs:
          - job_name: 'tetragon_metrics_2112'
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
    processors:
      filter/includemetrics:
        metrics:
          include:
            match_type: strict
            metric_names:
            # Cilium metrics
            - cilium_endpoint_state
            - cilium_bpf_map_ops_total
            - cilium_policy_l7_total
            # Hubble metrics
            - hubble_flows_processed_total
            - hubble_drop_total
            - hubble_dns_queries_total
            - hubble_http_requests_total
            # Tetragon metrics
            - tetragon_dns_total
            - tetragon_http_response_total
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
          processors:
          - filter/includemetrics
          - resourcedetection

clusterName: isovalent-demo
splunkObservability:
  accessToken: <YOUR-SPLUNK-ACCESS-TOKEN>
  realm: <YOUR-SPLUNK-REALM>

cloudProvider: aws
distribution: eks
```

**Important:** Replace:
- `<YOUR-SPLUNK-ACCESS-TOKEN>` with your Splunk Observability Cloud access token
- `<YOUR-SPLUNK-REALM>` with your realm (e.g., us1, us2, eu0)

{{% notice title="Metric Filtering" style="info" %}}
The configuration includes a metric filter to prevent overwhelming Splunk with high-volume metrics. Only the most valuable metrics for monitoring are included.
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
