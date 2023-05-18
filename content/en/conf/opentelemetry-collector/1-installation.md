---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1. Installation
weight: 1
---

## 1. Downloading the OpenTelemetry Collector Contrib distribution

The first step in installing the Open Telemetry Collector is downloading it. For our lab we will use the 'wget' command to download the '.deb' package from the OpenTelemetry Github repository. 

Obtain the `.deb` package for your platform from the [OpenTelemetry Collector Contrib releases page](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.75.0/otelcol-contrib_0.75.0_linux_amd64.deb
```

## 2. Installing the OpenTelemetry Collector Contrib distribution

Install the `.deb` package using `dpkg`. Not we are installing as root. Take a look at the Output tab in the box below to see what the exmple output of a successful install will look like:

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

The collector should now be running. We will verify this as root using systemctl command.

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
     Active: active (running) since Tue 2023-05-16 08:23:23 UTC; 25s ago
   Main PID: 1415 (otelcol-contrib)
      Tasks: 5 (limit: 1141)
     Memory: 22.2M
        CPU: 125ms
     CGroup: /system.slice/otelcol-contrib.service
             └─1415 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: NumberDataPoints #0
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Data point attributes:
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> exporter: Str(logging)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_instance_id: Str(df8a57f4-abdc-46b9-a847-acd62db1001f)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_name: Str(otelcol-contrib)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:      -> service_version: Str(0.75.0)
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: StartTimestamp: 2023-05-16 08:23:39.006 +0000 UTC
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Timestamp: 2023-05-16 08:23:39.006 +0000 UTC
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]: Value: 0.000000
May 16 08:23:39 ip-10-0-9-125 otelcol-contrib[1415]:         {"kind": "exporter", "data_type": "metrics", "name": "logging"}
```

{{% /tab %}}
{{< /tabs >}}

## 4. Default configuration

OpenTelemetry is configured through .yaml files. These files have default configurations that we can modify to meet our needs. Let's look at the default configuration that is supplied:

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

Congratulations! You have successfully downloaded and installed the OpenTelemtry Collector. You are well on your way to Ninja. But first lets chat through configuration files and different distrobutions of the OpenTelemetry Collector.

We will now walk through each section of the configuration file and modify it to send host metrics to Splunk Observability Cloud.

Splunk does provide its own, fully supported, distribution of the OpenTelemetry Collector. This distribution is available to install from the [Splunk GitHub Repository](https://github.com/signalfx/splunk-otel-collector). This distribution includes a number of additional features and enhancements that are not available in the OpenTelemetry Collector Contrib distribution.

- The Splunk Distribution of the OpenTelemetry Collector is production tested; it is in use by a number of customers in their production environments.
- Customers that use our distribution can receive direct help from official Splunk support within SLA's.
- Customers can use or migrate to the Splunk Distribution of the OpenTelemetry Collector without worrying about future breaking changes to its core configuration experience for metrics and traces collection (OpenTelemetry logs collection configuration is in beta). There may be breaking changes to the Collector's own metrics.
