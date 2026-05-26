---
title: OpenTelemetry Collector Service
linkTitle: 6.5 OTLP HTTP
weight: 5
---

## OTLP HTTP Exporter

In the Exporters section of the workshop, we configured the `otlphttp` exporter to send metrics to Splunk Observability Cloud. We now need to enable this under the metrics pipeline.

Update the `exporters` section to include `otlphttp/splunk` under the `metrics` pipeline:

```yaml {hl_lines="13"}
service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [debug, otlphttp/splunk]
```

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Observing the collector internals{{% /badge %}}" %}}

The collector captures internal signals about its behavior this also includes additional signals from running components.
The reason for this is that components that make decisions about the flow of data need a way to surface that information
as metrics or traces.

## Why monitor the collector?

This is somewhat of a chicken and egg problem of, "Who is watching the watcher?", but it is important that we can surface this information. Another interesting part of the collector's history is that it existed before the Go metrics' SDK was considered stable so the collector exposes a Prometheus endpoint to provide this functionality for the time being.

## Considerations

Monitoring the internal usage of each running collector in your organization can contribute a significant amount of new Metric Time Series (MTS). The Splunk distribution has curated these metrics for you and would be able to help forecast the expected increases.

## The Ninja Zone

To expose the internal observability of the collector, some additional settings can be adjusted:

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
# To limit exposure to denial of service attacks, change the host in endpoints below from 0.0.0.0 to a specific network interface.
# See https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md#safeguards-against-denial-of-service-attacks

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
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  opencensus:
    endpoint: 0.0.0.0:55678

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
        endpoint: 0.0.0.0:14250
      thrift_binary:
        endpoint: 0.0.0.0:6832
      thrift_compact:
        endpoint: 0.0.0.0:6831
      thrift_http:
        endpoint: 0.0.0.0:14268

  zipkin:
    endpoint: 0.0.0.0:9411

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
      - key: participant.name
        action: insert
        value: "INSERT_YOUR_NAME_HERE"

exporters:
  debug:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-Token: ${env:ACCESS_TOKEN}

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [hostmetrics, otlp, opencensus, prometheus/internal]
      processors: [batch, resourcedetection/system, resourcedetection/ec2, attributes/conf]
      exporters: [debug, otlphttp/splunk]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{% /tabs %}}

{{% /expand %}}

---

{{% notice style="tip" %}}
It is recommended that you validate your configuration file before restarting the collector. You can do this by pasting the contents of your `config.yaml` file into **[otelbin.io](https://www.otelbin.io/)**.

{{% expand title="{{% badge color=green title=**Screenshot** %}}OTelBin{{% /badge %}}" %}}
![otelbin-validator](../../images/otelbin.png)
{{% /expand %}}

{{% /notice %}}

Now that we have a working configuration, let's start the collector and then check to see what [zPages](../2-extensions/#zpages) is reporting.

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

Open up zPages in your browser: [**http://localhost:55679/debug/pipelinez**](http://localhost:55679/debug/pipelinez) (change `localhost` to reflect your own environment).
![pipelinez-full-config](../../images/pipelinez-full-config.png)
