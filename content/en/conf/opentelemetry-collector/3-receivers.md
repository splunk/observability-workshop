---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

Welcome to the receiver portion of the workshop! This is the starting point of the data pipeline of the OpenTelemetry Collector. Let's dive in.

A receiver, which can be push or pull based, is how data gets into the Collector. Receivers may support one or more data sources. Generally, a receiver accepts data in a specified format, translates it into the internal format and passes it to processors and exporters defined in the applicable pipelines.

{{< mermaid >}}
%%{
  init:{
    "theme":"base",
    "themeVariables": {
      "primaryColor": "#ffffff",
      "clusterBkg": "#eff2fb",
      "defaultLinkColor": "#333333"
    }
  }
}%%

flowchart LR;
    style M fill:#e20082,stroke:#333,stroke-width:4px,color:#fff
    subgraph Collector
    A[OTLP] --> M(Receivers)
    B[JAEGER] --> M(Receivers)
    C[Prometheus] --> M(Receivers)
    end
    subgraph Processors
    M(Receivers) --> H(Filters, Attributes, etc)
    E(Extensions)
    end
    subgraph Exporters
    H(Filters, Attributes, etc) --> S(OTLP)
    H(Filters, Attributes, etc) --> T(JAEGER)
    H(Filters, Attributes, etc) --> U(Prometheus)
    end
{{< /mermaid >}}

### Host Metrics Receiver

[**The Host Metrics Receiver**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/hostmetricsreceiver/README.md) generates metrics about the host system scraped from various sources. This is intended to be used when the collector is deployed as an agent which is what we will be doing in this workshop.

Let's update the `/etc/otelcontribcol/config.yaml` file and configure the **hostmetrics** receiver. Insert the following YAML under the **receivers** section, taking care to indent by two spaces e.g.

``` bash
sudo vi /etc/otelcontribcol/config.yaml
```

{{< tabs >}}
{{% tab title="Host Metrics Receiver Configuration" %}}

```yaml {hl_lines=["2-22"]}
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
{{% tab title="Host Metrics Receiver Configuration Complete" %}}

```yaml {hl_lines=["10-30"]}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

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
  otlp:
    protocols:
      grpc:
      http:

  opencensus:

  # Collect own metrics
  prometheus:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

  jaeger:
    protocols:
      grpc:
      thrift_binary:
      thrift_compact:
      thrift_http:

  zipkin:

processors:
  batch:

exporters:
  logging:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}

You will also notice another receiver called **prometheus**. [Prometheus](https://prometheus.io/docs/introduction/overview/) is an open-source toolkit used by the OpenTelemetry Collector. This receiver is used to scrape metrics from the OpenTelemetry Collector itself. These metrics can then be used to monitor the health of the collector.

Let's modify the **prometheus** receiver to clearly show that it is for collecting metrics from the collector itself. By changing the name of the receiver from **prometheus** to **prometheus/internal**, it is now much clearer as to what that receiever is doing. Update the configuration file to look like this:

{{< tabs >}}
{{% tab title="Prometheus Receiver Configuration" %}}

```yaml {hl_lines=[1]}
prometheus/internal:
  config:
    scrape_configs:
    - job_name: 'otel-collector'
      scrape_interval: 10s
      static_configs:
      - targets: ['0.0.0.0:8888']
```

{{% /tab %}}
{{% tab title="Prometheus Receiver Configuration Complete" %}}

```yaml {hl_lines=[39]}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

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
  otlp:
    protocols:
      grpc:
      http:

  opencensus:

  # Collect own metrics
  prometheus/internal:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

  jaeger:
    protocols:
      grpc:
      thrift_binary:
      thrift_compact:
      thrift_http:

  zipkin:

processors:
  batch:

exporters:
  logging:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]

  extensions: [health_check, pprof, zpages]
```
  
{{% /tab %}}
{{< /tabs >}}

## Example Dashboard - Prometheus metrics

The following screenshot shows an example dashboard of the metrics the Prometheus internal receiver collects from the OpenTelemetry Collector. Here, we can see accepted and sent spans, metrics and log records.

{{% notice style="note" %}}
The following screenshot is an out of the box (OOTB) dashboard from Splunk Observability Cloud that allows your to easily monitor your Splunk OpenTelemetry Collector install base.
{{% /notice %}}

![otel-charts](../images/otel-charts.png)

## Other Receivers

You will notice in the default configuration there are other receivers (**otlp**, **opencensus**, **jaeger** and **zipkin**). These are used to receive telemetry data from other sources. We will not be using these receivers in this workshop and can be left as they are.

## Configuration Check-in

Now that we have reviewed how data gets into the OpenTelemetry Collector, we can now learn how the Collector processes the data.
