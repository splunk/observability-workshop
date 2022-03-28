---
title: Install the OpenTelemetry Collector
weight: 2
---

## Install The Open Telemetry Collector

The OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, cpu, memory, etc)
* Application Performance Monitoring (APM) traces
* Host and application logs

Splunk Observability Cloud offers wizards to walk you through the setup of the Collector on both your infrastrucutre and applications. To get to the wizard, click in the top left corner icon (the hamburger menu), then click on **Data Setup**

You'll be taken to a short wizard where you will select some options. The default settings should work, no need to make changes. The wizard will output a few commands that need to be executed in the shell.

However, if you have already completed the **Splunk IMT** workshop you can take advantage of the existing environment variables. Othwewise, create the `ACCESS_TOKEN` and `REALM` environment variables to use in the proceeding OpenTelemetry Collector install command. For instance, if your realm is `us1`, you would type `export REALM=us1` and for `eu0` type `export REALM=eu0`.

{{< tabpane >}}
{{< tab header="Export Variables" lang="bash" >}}
export ACCESS_TOKEN=<replace_with_O11y-Workshop-ACCESS_token>
export REALM=<replace_with_splunk_realm>
{{< /tab >}}
{{< /tabpane >}}

We can then go ahead and install the Collector:

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN --mode agent
```

This command will download and setup the OpenTelemetry Collector. Once the install is completed, you can navigate to the Infrastructure page to see the data from your Host

`>> Infrastructure >> My Data Center >> Hosts`

Add Filter >> `host.name` >> (type or select the hostname of your virtual machine)

Once you see data flowing for your host, we are then ready to get started with the APM component
