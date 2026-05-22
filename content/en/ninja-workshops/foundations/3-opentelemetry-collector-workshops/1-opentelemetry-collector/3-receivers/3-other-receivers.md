---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Other Receivers
weight: 3
---

## Other Receivers

You will notice in the default configuration there are other receivers: **otlp**, **opencensus**, **jaeger** and **zipkin**. These are used to receive telemetry data from other sources. We will not be covering these receivers in this workshop and they can be left as they are.

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Create receivers dynamically{{% /badge %}}" %}}

To help observe short lived tasks like docker containers, kubernetes pods, or ssh sessions, we can use the [receiver creator](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator) with [observer extensions](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/observer) to create a new receiver as these services start up.

## What do we need?

In order to start using the receiver creator and its associated observer extensions, they will need to be part of your collector build manifest.

See [installation](../1-installation/) for the details.

## Things to consider?

Some short lived tasks may require additional configuration such as _username_, and _password_.
These values can be referenced via [environment variables](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables),
or use a scheme expand syntax such as `${file:./path/to/database/password}`.
Please adhere to your organisation's secret practices when taking this route.

## The Ninja Zone

There are only two things needed for this ninja zone:

1. Make sure you have added receiver creater and observer extensions to the builder manifest.
2. Create the config that can be used to match against discovered endpoints.

To create the templated configurations, you can do the following:

```yaml
receiver_creator:
  watch_observers: [host_observer]
  receivers:
    redis:
      rule: type == "port" && port == 6379
      config:
        password: ${env:HOST_REDIS_PASSWORD}
```

For more examples, refer to these [receiver creator's examples](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/receivercreator#examples).

{{% /expand %}}

---

## Configuration Check-in

We've now covered receivers, so let's now check our configuration changes.

---

{{% expand title="{{% badge icon=check color=green title=**Check-in** %}}Review your configuration{{% /badge %}}" %}}
{{< tabs >}}
{{% tab title="config.yaml" %}}

```yaml {lineNos="table" wrap="true" hl_lines="13-33 45"}
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

Now that we have reviewed how data gets into the OpenTelemetry Collector through receivers, let's now take a look at how the Collector processes the received data.

{{% notice style="warning" %}}
As the `/etc/otelcol-contrib/config.yaml` is not complete, please **do not** attempt to restart the collector at this point.
{{% /notice %}}
