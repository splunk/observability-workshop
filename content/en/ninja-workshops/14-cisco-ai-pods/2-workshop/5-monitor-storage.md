---
title: Monitor Storage
linkTitle: 5. Monitor Storage
weight: 5
time: 10 minutes
---

In this step, we'll configure the Prometheus receiver to monitor the storage. 

## What storage do Cisco AI PODs utilize? 

Cisco AI PODs have a number of different storage options, including Pure Storage, 
VAST, and NetApp. 

The workshop will focus on Pure Storage. 

## How do we capture Pure Storage metrics? 

Cisco AI PODs that utilize Pure Storage also use a technology called Portworx, 
which provides persistent storage for Kubernetes. 

Portworx includes a metrics endpoint that we can scrape using the Prometheus receiver. 

## Capture Storage Metrics with Prometheus

Let's modify the OpenTelemetry collector configuration to scrape Portworx metrics 
with the Prometheus receiver. 

To do so, let's add an additional Prometheus receiver creator section
to the `otel-collector-values.yaml` file:

``` yaml
      receiver_creator/storage:
        # Name of the extensions to watch for endpoints to start and stop.
        watch_observers: [ k8s_observer ]
        receivers:
          prometheus/portworx:
            config:
              config:
                scrape_configs:
                  - job_name: portworx-metrics
                    static_configs:
                      - targets:
                          - '`endpoint`:17001'
                          - '`endpoint`:17018'
            rule: type == "pod" && labels["app"] == "portworx-metrics-sim"
```

We'll need to ensure that Portworx metrics are added to the `filter/metrics_to_be_included` filter
processor configuration as well:

``` yaml
    processors:
      filter/metrics_to_be_included:
        metrics:
          # Include only metrics used in charts and detectors
          include:
            match_type: strict
            metric_names:
              - DCGM_FI_DEV_FB_FREE
              - ...
              - px_cluster_cpu_percent
              - px_cluster_disk_total_bytes
              - px_cluster_disk_utilized_bytes
              - px_cluster_status_nodes_offline
              - px_cluster_status_nodes_online
              - px_volume_read_latency_seconds
              - px_volume_reads_total
              - px_volume_readthroughput
              - px_volume_write_latency_seconds
              - px_volume_writes_total
              - px_volume_writethroughput
```

We'll need to add a new metrics pipeline for Portworx metrics as well:

``` yaml
        metrics/storage:
          exporters:
            - signalfx
          processors:
            - memory_limiter
            - filter/metrics_to_be_included
            - batch
            - resourcedetection
            - resource
          receivers:
            - receiver_creator/storage
```

Before applying the configuration changes to the collector, take a moment to compare the
contents of your modified `otel-collector-values.yaml` file with the
`otel-collector-values-with-portworx.yaml` file.
Update your file as needed to ensure the contents match.  Remember that indentation is important
for `yaml` files, and needs to be precise.

Now we can update the OpenTelemetry collector configuration by running the
following Helm command:

``` bash
helm upgrade splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector-values.yaml \
  -n $USER_NAME \
  splunk-otel-collector-chart/splunk-otel-collector
```

## Confirm Metrics are Sent to Splunk

Navigate to `Dashboards` in Splunk Observability Cloud, then search for the
`Cisco AI PODs Dashboard`, which is included in the `Built-in dashboard groups`.
Navigate to the `PURE STORAGE` tab and ensure the dashboard is filtered 
on your OpenShift cluster name. The charts should be populated as in the 
following example:

![Pure Storage Dashboard](../../images/PureStorage.png)

