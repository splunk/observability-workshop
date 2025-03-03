---
title: OpenTelemetry Collector Exporters
linkTitle: 5.1 OTLP HTTP
weight: 1
---

## OTLP HTTP Exporter

To send metrics over HTTP to Splunk Observability Cloud, we will need to configure the **otlphttp** exporter.

Let's edit our `/etc/otelcol-contrib/config.yaml` file and configure the **otlphttp** exporter. Insert the following YAML under the **exporters** section, taking care to indent by two spaces e.g.

We will also change the verbosity of the logging exporter to prevent the disk from filling up. The default of `detailed` is very noisy.

```yaml {hl_lines="3-4"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
```

Next, we need to define the `metrics_endpoint` and configure the target URL.

{{% notice style="note" %}}
If you are an attendee at a Splunk-hosted workshop, the instance you are using has already been configured with a Realm environment variable. We will reference that environment variable in our configuration file. Otherwise, you will need to create a new environment variable and set the Realm e.g.

``` bash
export REALM="us1"
```

{{% /notice %}}

The URL to use is `https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp`. (Splunk has Realms in key geographical locations around the world for data residency).

The **otlphttp** exporter can also be configured to send traces and logs by defining a target URL for `traces_endpoint` and `logs_endpoint` respectively. Configuring these is outside the scope of this workshop.

```yaml {hl_lines="5"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
```

By default, `gzip` compression is enabled for all endpoints. This can be disabled by setting `compression: none` in the exporter configuration. We will leave compression enabled for this workshop and accept the default as this is the most efficient way to send data.

To send metrics to Splunk Observability Cloud, we need to use an Access Token. This can be done by creating a new token in the Splunk Observability Cloud UI. For more information on how to create a token, see [Create a token](https://docs.splunk.com/Observability/admin/authentication-tokens/org-tokens.html). The token needs to be of type **INGEST**.

{{% notice style="note" %}}
If you are an attendee at a Splunk-hosted workshop, the instance you are using has already been configured with an Access Token (which has been set as an environment variable). We will reference that environment variable in our configuration file. Otherwise, you will need to create a new token and set it as an environment variable e.g.

``` bash
export ACCESS_TOKEN=<replace-with-your-token>
```

{{% /notice %}}

The token is defined in the configuration file by inserting `X-SF-TOKEN: ${env:ACCESS_TOKEN}` under a `headers:` section:

```yaml {hl_lines="6-8"}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.${env:REALM}.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: ${env:ACCESS_TOKEN}
```

## Configuration Check-in

Now that we've covered exporters, let's check our configuration changes:

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="83-87"}
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
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [debug]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}
{{% /expand %}}

---

Of course, you can easily configure the `metrics_endpoint` to point to any other solution that supports the **OTLP** protocol.

Next, we need to enable the receivers, processors and exporters we have just configured in the service section of the `config.yaml`.
