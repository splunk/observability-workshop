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
TBD
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
TBD
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
TBD
```

{{% /tab %}}
{{< /tabs >}}

## Collector Configuration

Where do we find the configuration that is used by this collector? 

It's available in the `/etc/otel/collector` directory.  Since we installed the 
collector in `agent` mode, the collector configuration can be found in the 
`agent_config.yaml file`. 

