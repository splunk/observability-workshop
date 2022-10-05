---
title: Install the OpenTelemetry Collector
weight: 2
---

## Install The Open Telemetry Collector

The OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, cpu, memory, etc)
* Application Performance Monitoring (APM) traces
* Profiling data
* Host and application logs

Splunk Observability Cloud offers wizards to walk you through the setup of the Collector on both your infrastrucutre and applications. By default, the wizard will only provide the commands to only install the collector.

If you have already completed the **Splunk IMT** workshop you can take advantage of the existing environment variables. Othwewise, create the `ACCESS_TOKEN` and `REALM` environment variables to use in the proceeding OpenTelemetry Collector install command. For instance, if your realm is `us1`, you would type `export REALM=us1` and for `eu0` type `export REALM=eu0` etc.

{{< tabpane >}}
{{< tab header="Export Variables" lang="bash" >}}
export ACCESS_TOKEN=<replace_with_O11y-Workshop-ACCESS_TOKEN>
export REALM=<replace_with_Splunk_Realm>
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="Delete any existing OpenTelemtry Collectors" color="warning" %}}
If you have completed the Splunk IMT workshop, please ensure you have deleted the collector running in Kubernetes before continuing. This can be done by running the following command: `helm delete splunk-otel-collector`.
{{% /alert %}}

We can then go ahead and install the Collector. There are two additional parameters passed to the install script, they are `--with-instrumentation` and `--deployment-environment`. The `--with-instrumentation` option the installer will install the agent from the Splunk distribution of OpenTelemetry Java, which is then loaded automatically when the Pet Clinic Java application starts up. No configuration required!

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --with-instrumentation --deployment-environment $(hostname)-petclinic --realm $REALM -- $ACCESS_TOKEN
```

This command will download and setup the OpenTelemetry Collector. Once the install is completed, you can navigate to the Infrastructure page to see the data from your host, **Infrastructure → My Data Center → Hosts**.

Click {{% labelbutton color="ui-button-grey" %}}**Add Filter**{{% /labelbutton %}} select `host.name` and type or select the hostname of your virtual machine. Once you see data flowing for your host, we are then ready to get started with the APM component.
