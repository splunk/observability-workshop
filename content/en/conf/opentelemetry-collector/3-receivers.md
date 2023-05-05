---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

A receiver, which can be push or pull based, is how data gets into the Collector. Receivers may support one or more data sources. Generally, a receiver accepts data in a specified format, translates it into the internal format and passes it to processors and exporters defined in the applicable pipelines.

### Host Metrics Receiver

[The Host Metrics Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/hostmetricsreceiver/README.md) generates metrics about the host system scraped from various sources. This is intended to be used when the collector is deployed as an agent which is what we will be doing in this workshop.

Let's edit our `/etc/otelcontribcol/config.yaml` file and configure the hostmetrics receiver. Insert the following YAML under the `receivers` section, taking care to indent by two spaces e.g.

```yaml
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

You will also notice another receiver called `prometheus`. [Prometheus](https://prometheus.io/docs/introduction/overview/) is an open-source toolkit used by the OpenTelemetry Collector. This receiver is used to scrape metrics from the OpenTelemetry Collector itself. These metrics can then be used to monitor the health of the collector.

Let's modify the `prometheus` receiver to clearly show that it is for collecting metrics from the collector itself. Change the `config.yaml` file to look like this:

```yaml
  prometheus/internal:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']
```

![otel-charts](../images/otel-charts.png)
