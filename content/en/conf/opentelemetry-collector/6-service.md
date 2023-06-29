---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

The **Service** section is used to configure what components are enabled in the Collector based on the configuration found in the receivers, processors, exporters, and extensions sections.

{{% notice style="info" %}}
If a component is configured, but not defined within the **Service** section then it is **not** enabled.
{{% /notice %}}

The service section consists of three sub-sections:

- extensions
- pipelines
- telemetry

In the default configuration, the extension section has been configured to enable `health_check`, `pprof` and `zpages`, which we configured in the Extensions module earlier.

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

## Configure Metric Pipeline

### Hostmetrics Receiver

If you recall from the Receivers portion of the workshop, we defined the [Host Metrics Receiver](../3-receivers/#host-metrics-receiver) to generate metrics about the host system, which are scraped from various sources. To enable the receiver, we must include the `hostmetrics` receiver in the metrics pipeline.

In the `metrics` pipeline, add `hostmetrics` to the metrics `receivers` section.

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [logging]
```

### Prometheus Internal Receiver

Earlier in the workshop, we also renamed the `prometheus` receiver to reflect that is was collecting metrics internal to the collector, renaming it to `prometheus/internal`.

 We now need to enable the `prometheus/internal` receiver under the metrics pipeline. Update the `receivers` section to include `prometheus/internal` under the `metrics` pipeline:

```yaml {hl_lines="11"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch]
      exporters: [logging]
```

### Resource Detection Processor

We also added `resourcedetection/system` and `resourcedetection/ec2` processors so that the collector can capture the instance hostname and AWS/EC2 metadata. We now need to enable these two processors under the metrics pipeline.

Update the `processors` section to include `resourcedetection/system` and `resourcedetection/ec2` under the `metrics` pipeline:

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2]
      exporters: [logging]
```

### Attributes Processor

Also in the Processors section of this workshop, we added the `attributes/conf` processor so that the collector will inset a new attribute called `conf.attendee.name` to all the metrics. We now need to enable this under the metrics pipeline.

Update the `processors` section to include `attributes/conf` under the `metrics` pipeline:

```yaml {hl_lines="12"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [logging]
```

### OTLPHTTP Exporter

In the Exporters section of the workshop, we configured the `otlphttp` exporter to send metrics to Splunk Observability Cloud. We now need to enable this under the metrics pipeline.

Update the `exporters` section to include `otlphttp/splunk` under the `metrics` pipeline:

```yaml {hl_lines="13"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection]
      exporters: [logging, otlphttp/splunk]
```

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Observing the collector internals{{% /badge %}}" %}}

The collector captures internal signals about its behaviour this also include additional signals from running components.
The reason for this is that components that make decisions about the flow of data need a way to surface that information
as metrics or traces.

## Why monitor the collector?

This is somewhat of a chicken and egg problem of, "Who is watching the the watcher?", but it is important that we can surface this information. Another interesting part of the collector's history is that it existed before the Go metrics' SDK was considered stable so the collector exposes a prometheus endpoint to provide this functionality for the time being.

## Considerations

Monitoring the internal usage of each running collector in your organisation can contribute a significant amount of new Metric Time Series (MTS). The Splunk distribution has curated these metrics for you and would be able to to help forcast the expected increases.

## The Ninja Zone

To expose the internal observability of the collector, there are some additional settings that can be adjusted:

{{< tabs >}}
{{% tab title="telemetry schema" %}}

```yaml
service:
  telemetry:
    logs:
      level: <info|warn|error>
      development: <true|false>
      encoding: <console|json>
      disable_caller: <true|false>
      disable_stacktrace: <true|false>
      output_paths: [<stdout|stderr>, paths...]
      error_output_paths: [<stdout|stderr>, paths...]
      initial_fields:
        key: value
    metrics:
      level: <none|basic|normal|detailed>
      # Address binds the promethues endpoint to scrape
      address: <hostname:port>
```

{{% /tab %}}
{{% tab title="example-config.yml" %}}

```yaml
service:
  telemetry:
    logs: 
      level: info
      encoding: json
      disable_stacktrace: true
      initial_fields:
        instance.name: ${env:INSTANCE}
    metrics:
      address: localhost:8888 
```

{{% /tab %}}
{{< /tabs >}}

## References

1. [https://opentelemetry.io/docs/collector/configuration/#service](https://opentelemetry.io/docs/collector/configuration/#service)

{{% /expand %}}

---

## Final configuration

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your final configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

``` yaml {lineNos="table" wrap="true"}
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
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
  resourcedetection/ec2:
    detectors: [ec2]
  attributes/conf:
    actions:
      - key: conf.attendee.name
        action: insert
        value: "INSERT_YOUR_NAME_HERE"

exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.us1.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: ${env:ACCESS_TOKEN}

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [logging]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf] 
      exporters: [logging, otlphttp/splunk]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{% /tabs %}}

{{% /expand %}}

---

{{% notice style="tip" %}}
It is recommended that you validate your configuration file before restarting the collector. You can do this by using the built-in `validate` command:

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
otelcol-contrib validate --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab title="Example error output" %}}

``` text
Error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding:

* error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding:

* 'actions[0]' has invalid keys: actions
2023/06/29 09:41:28 collector server run finished with error: failed to get config: cannot unmarshal the configuration: 1 error(s) decoding:

* error decoding 'processors': error reading configuration for "attributes/conf": 1 error(s) decoding:

* 'actions[0]' has invalid keys: actions
```

{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

Now that we have a working configuration, let's start the collector and then check to see what [zPages](../2-extensions/#zpages) is reporting.

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

![pipelinez-full-config](../images/pipelinez-full-config.png)
