---
title: Deploy the OpenTelemetry Collector
linkTitle: 2. Deploy the OpenTelemetry Collector
weight: 2
time: 10 minutes
---

## Deploy the OpenTelemetry Collector

Let’s deploy the Splunk Distribution of the OpenTelemetry Collector on our Linux EC2 instance. 

We can do this by downloading the collector binary using `curl`, and then running it  
with specific arguments that tell the collector which realm to report data into, which access 
token to use, and which deployment environment to report into. 

> A deployment environment in Splunk Observability Cloud is a distinct deployment of your system 
> or application that allows you to set up configurations that don’t overlap with configurations 
> in other deployments of the same application.

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh; \
sudo sh /tmp/splunk-otel-collector.sh \
--realm $REALM \
--mode agent \
--without-instrumentation \
--deployment-environment otel-$INSTANCE \
-- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Splunk OpenTelemetry Collector Version: latest
Memory Size in MIB: 512
Realm: us1
Ingest Endpoint: https://ingest.us1.signalfx.com
API Endpoint: https://api.us1.signalfx.com
HEC Endpoint: https://ingest.us1.signalfx.com/v1/log
etc. 
```

{{% /tab %}}
{{< /tabs >}}

Refer to [Install the Collector for Linux with the installer script](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-linux/install-linux.html#otel-install-linux)
for further details on how to install the collector. 

## Confirm the Collector is Running

Let's confirm that the collector is running successfully on our instance. 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sudo systemctl status splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/splunk-otel-collector.service.d
             └─service-owner.conf
     Active: active (running) since Fri 2024-12-20 00:13:14 UTC; 45s ago
   Main PID: 14465 (otelcol)
      Tasks: 9 (limit: 19170)
     Memory: 117.4M
        CPU: 681ms
     CGroup: /system.slice/splunk-otel-collector.service
             └─14465 /usr/bin/otelcol

```

{{% /tab %}}
{{< /tabs >}}

## How do we view the collector logs? 

We can view the collector logs using `journalctl`: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sudo journalctl -u splunk-otel-collector 
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Dec 20 00:13:14 derek-1 systemd[1]: Started Splunk OpenTelemetry Collector.
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:483: Set config to /etc/otel/collector/agent_config.yaml
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:539: Set memory limit to 460 MiB
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:524: Set soft memory limit set to 460 MiB
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:373: Set garbage collection target percentage (GOGC) to 400
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:414: set "SPLUNK_LISTEN_INTERFACE" to "127.0.0.1"
etc. 
```

{{% /tab %}}
{{< /tabs >}}

## Collector Configuration

Where do we find the configuration that is used by this collector? 

It's available in the `/etc/otel/collector` directory.  Since we installed the 
collector in `agent` mode, the collector configuration can be found in the 
`agent_config.yaml` file. 

