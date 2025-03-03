---
title: OpenTelemetry Collector Processors
linkTitle: 4.3 Attributes
weight: 3
---

## Attributes Processor

The attributes processor modifies attributes of a span, log, or metric. This processor also supports the ability to filter and match input data to determine if they should be included or excluded for specified actions.

It takes a list of actions that are performed in the order specified in the config. The supported actions are:

- `insert`: Inserts a new attribute in input data where the key does not already exist.
- `update`: Updates an attribute in input data where the key does exist.
- `upsert`: Performs insert or update. Inserts a new attribute in input data where the key does not already exist and updates an attribute in input data where the key does exist.
- `delete`: Deletes an attribute from the input data.
- `hash`: Hashes (SHA1) an existing attribute value.
- `extract`: Extracts values using a regular expression rule from the input key to target keys specified in the rule. If a target key already exists, it will be overridden.

We are going to create an attributes processor to `insert` a new attribute to all our host metrics called `participant.name` with a value of your name e.g. `marge_simpson`.

{{% notice style="warning" %}}

Ensure you replace `INSERT_YOUR_NAME_HERE` with your name and also ensure you **do not** use spaces in your name.

{{% /notice %}}

Later on in the workshop, we will use this attribute to filter our metrics in Splunk Observability Cloud.

{{% tab title="Attributes Processor Configuration" %}}

``` yaml {hl_lines="9-13"}
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
```

{{%/ tab %}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Using connectors to gain internal insights{{% /badge %}}" %}}

One of the most recent additions to the collector was the notion of a [**connector**](https://opentelemetry.io/docs/collector/configuration/#connectors), which allows you to join the output of one pipeline to the input of another pipeline.

An example of how this is beneficial is that some services emit metrics based on the amount of datapoints being exported, the number of logs containing an error status,
or the amount of data being sent from one deployment environment. The count connector helps address this for you out of the box.

## Why a connector instead of a processor?

A processor is limited in what additional data it can produce considering it has to pass on the data it has processed making it hard to expose additional information. Connectors do not have to emit the data they receive which means they provide an opportunity to create the insights we are after.

For example, a connector could be made to count the number of logs, metrics, and traces that do not have the deployment environment attribute.

A very simple example with the output of being able to break down data usage by deployment environment.

## Considerations with connectors

A connector only accepts data exported from one pipeline and receiver by another pipeline, this means you may have to consider how you construct your collector config to take advantage of it.

## References

1. [**https://opentelemetry.io/docs/collector/configuration/#connectors**](https://opentelemetry.io/docs/collector/configuration/#connectors)
2. [**https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/countconnector)

{{% /expand %}}

---

## Configuration Check-in

That's processors covered, let's check our configuration changes.

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="69-79"}
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
    verbosity: detailed

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
