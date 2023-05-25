---
title: OpenTelemetry Collector Extensions
linkTitle: 2. Extensions
weight: 2
---

Now that we have the OpenTelemetry Collector is installed. Let's take a look at extensions for the OTEL Collector.

Extensions are available primarily for tasks that do not involve processing telemetry data. Examples of extensions include health monitoring, service discovery, and data forwarding. Extensions are optional.

Extensions are configured in the same `config.yaml` file that we reference in module 1 of this lab. Let's edit the `config.yaml` file and configure the extensions. Note that the `pprof` and `zpages` extensions are already configured in the default `config.yaml` file. For the purpose of this lab, we will only be updating the `health_check` extension.

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{< tabs >}}
{{% tab name="Extensions Configuration" %}}

```yaml {hl_lines=[3]}
extensions:
  health_check:
    endpoint: "0.0.0.0:13133"
```

{{% /tab %}}
{{% tab name="Extensions Configuration Complete" %}}

```yaml {hl_lines=[3]}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
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

Restart the collector:

``` bash
sudo systemctl restart otelcol-contrib
```

***

{{% expand title="{{% badge style=primary icon=user-ninja title=**Ninja** %}}Improve data durability with storage extension{{% /badge %}}" %}}

For this, we will need to validate our distrobution has the `file_storage` extension installed,
this can be down by running the command `otelcol-contrib components` and it should so something like:

```yaml
# ... truncated for clarity
extensions:
  - file_storage
```

This extension provides exporters the ability to queue data to disk in the event that exporter is unable
to send data to the configured endpoint.

In order to configure the extension, you will need to update to include the following information:

```yaml
extensions:
  file_storage:
    directory: /tmp/otel-data
    timeout: 10s
    compaction:
       directory: /tmp/otel-data
       on_start: true
       on_rebound: true
       rebound_needed_threshold_mib: 5
       rebound_trigger_threshold_mib: 3

# ... truncated for clarity

service:
  extension:
  # Additiona extensions here 
  - file_storage
```

## Why queue data to disk?

This allows the collector to queue data (and even restart) to ensure data is sent the upstream provider.

## Considerations for queuing data to disk?

There is a potential that this could impact data throughput performance due disk performance.

### References

1. [https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583](https://community.splunk.com/t5/Community-Blog/Data-Persistence-in-the-OpenTelemetry-Collector/ba-p/624583)
2. [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage)

{{% /expand %}}

***

## Health Check

This extension enables an HTTP url that can be probed to check the status of the OpenTelemetry Collector. This extension can be used as a liveness and/or readiness probe on Kubernetes. To learn more about the curl command, check out the [curl man page](https://curl.se/docs/manpage.html).

{{< tabs >}}
{{% tab name="Command" %}}

```bash
curl http://localhost:13133
```

{{% /tab %}}
{{% tab name="Status Output" %}}

``` text
{"status":"Server available","upSince":"2023-04-27T10:11:22.153295874+01:00","uptime":"16m24.684476004s"}
```

{{% /tab %}}
{{< /tabs >}}

## Performance Profiler

[Performance Profiler](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/extension/pprofextension/README.md) extension enables the golang net/http/pprof endpoint. This is typically used by developers to collect performance profiles and investigate issues with the service.

## zPages

[zPages](https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md) are an in-process alternative to external exporters. When included, they collect and aggregate tracing and metrics information in the background; this data is served on web pages when requested.

{{% notice style="tip" %}}
Install a text-based web browser (or use your local browser using the instance IP address)

``` bash
sudo apt update && sudo apt install lynx -y
```

{{% /notice %}}

**ServiceZ** gives an overview of the collector services and quick access to the pipelinez, extensionz, and featurez zPages. The page also provides build and runtime information.

Example URL: [http://localhost:55679/debug/servicez](http://localhost:55679/debug/servicez)

![ServiceZ](../images/servicez.png)

**PipelineZ** brings insight on the running pipelines running in the collector. You can find information on type, if data is mutated and the receivers, processors and exporters that are used for each pipeline.

Example URL: [http://localhost:55679/debug/pipelinez](http://localhost:55679/debug/pipelinez)

![PipelineZ](../images/pipelinez.png)

**ExtensionZ** shows the extensions that are active in the collector.

Example URL: [http://localhost:55679/debug/extensionz](http://localhost:55679/debug/extensionz)

![ExtensionZ](../images/extensionz.png)

Now that we have reviewed extensions, lets dive into the data pipeline portion of the workshop. The data pipeline in the OpenTelemetry Collector is made up of receivers, processors, and exporters. We will first start with receivers.
