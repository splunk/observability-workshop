---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1. Installation
weight: 1
---

## 1. Downloading the OpenTelemetry Collector Contrib distribution

Obtain the `.deb` package for your platform from the [OpenTelemetry Collector Contrib releases page](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.75.0/otelcol-contrib_0.75.0_linux_amd64.deb
```

## 2. Installing the OpenTelemetry Collector Contrib distribution

Install the `.deb` package using `dpkg`:

{{< tabs >}}
{{% tab name="Install" %}}

``` bash
sudo dpkg -i otelcol-contrib_0.75.0_linux_amd64.deb
```

{{% /tab %}}
{{% tab name="dpkg Output" %}}

``` text
Selecting previously unselected package otelcol-contrib.
(Reading database ... 64218 files and directories currently installed.)
Preparing to unpack otelcol-contrib_0.75.0_linux_amd64.deb ...
Unpacking otelcol-contrib (0.75.0) ...
Setting up otelcol-contrib (0.75.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service.
```

{{% /tab %}}
{{< /tabs >}}

## 3. Confirm the Collector is running

{{< tabs >}}
{{% tab name="Command" %}}

``` bash
sudo systemctl status otelcol-contrib
```

{{% /tab %}}
{{% tab name="Status Output" %}}

``` text
● otelcol-contrib.service - OpenTelemetry Collector Contrib
     Loaded: loaded (/lib/systemd/system/otelcol-contrib.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2023-04-27 12:38:27 BST; 1h 51min ago
   Main PID: 3393 (otelcol-contrib)
      Tasks: 7 (limit: 1116)
     Memory: 49.1M
        CPU: 28.741s
     CGroup: /system.slice/otelcol-contrib.service
             └─3393 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

Apr 27 14:30:16 otel otelcol-contrib[3393]: Timestamp: 2023-04-27 13:30:15.958341145 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Value: 0.000000
Apr 27 14:30:16 otel otelcol-contrib[3393]: NumberDataPoints #7
Apr 27 14:30:16 otel otelcol-contrib[3393]: Data point attributes:
Apr 27 14:30:16 otel otelcol-contrib[3393]:      -> cpu: Str(cpu0)
Apr 27 14:30:16 otel otelcol-contrib[3393]:      -> state: Str(wait)
Apr 27 14:30:16 otel otelcol-contrib[3393]: StartTimestamp: 2023-04-27 09:01:16 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Timestamp: 2023-04-27 13:30:15.958341145 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Value: 9.700000
Apr 27 14:30:16 otel otelcol-contrib[3393]:         {"kind": "exporter", "data_type": "metrics", "name": "logging"}
```

{{% /tab %}}
{{< /tabs >}}

## 4. Default configuration

Let's look at the default configuration that is supplied:

{{< tabs >}}
{{% tab name="Command" %}}

```bash
cat /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab name="Configuration Output" %}}

```yaml
extensions:
  health_check:
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

We will now walk through each section of the configuration file and modify it to send host metrics to Splunk Observability Cloud.

Splunk does provide its own, fully supported, distribution of the OpenTelemetry Collector. This distribution is available to install from the [Splunk GitHub Repository](https://github.com/signalfx/splunk-otel-collector). This distribution includes a number of additional features and enhancements that are not available in the OpenTelemetry Collector Contrib distribution.

- The Splunk Distribution of the OpenTelemetry Collector is production tested; it is in use by a number of customers in their production environments
- Customers that use our distribution can receive direct help from official Splunk support within SLA's
- Customers can use or migrate to the Splunk Distribution of the OpenTelemetry Collector without worrying about future breaking changes to its core configuration experience for metrics and traces collection (OpenTelemetry logs collection configuration is in beta). There may be breaking changes to the Collector's own metrics.
