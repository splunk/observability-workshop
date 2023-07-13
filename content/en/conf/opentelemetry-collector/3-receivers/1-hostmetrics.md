---
title: OpenTelemetry Collector Receivers
linkTitle: 1. Host Metrics
weight: 1
---

## Host Metrics Receiver

[**The Host Metrics Receiver**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/hostmetricsreceiver/README.md) generates metrics about the host system scraped from various sources. This is intended to be used when the collector is deployed as an agent which is what we will be doing in this workshop.

Let's update the `/etc/otel-contrib/config.yaml` file and configure the **hostmetrics** receiver. Insert the following YAML under the **receivers** section, taking care to indent by two spaces.

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{% tab title="Host Metrics Receiver Configuration" %}}

```yaml {hl_lines="2-22"}
receivers:
  hostmetrics:
    collection_interval: 10s
    scrapers:
      # CPU utilization metrics
      cpu:
      # Disk I/O metrics
      disk:
      # File System utilization metrics
      filesystem:
      # Memory utilization metrics
      memory:
      # Network interface I/O metrics & TCP connection metrics
      network:
      # CPU load metrics
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Process count metrics
      processes:
      # Per process CPU, Memory and Disk I/O metrics. Disabled by default.
      # process:
```

{{% /tab %}}
