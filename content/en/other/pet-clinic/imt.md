---
title: Installing the OpenTelemetry Collector
linkTitle: 1. OpenTelemetry Collector
weight: 1
---

## 1. Introduction

The OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, cpu, memory, etc)
* Application Performance Monitoring (APM) traces
* Profiling data
* Host and application logs

Splunk Observability Cloud offers wizards to walk you through the setup of the Collector on both your infrastructure and applications. By default, the wizard will only provide the commands to only install the collector.

## 2. Configure environment variables

If you have already completed the **Splunk IM** workshop you can take advantage of the existing environment variables. Otherwise, create the `ACCESS_TOKEN` and `REALM` environment variables to use in the proceeding OpenTelemetry Collector install command.

For instance, if your realm is `us1`, you would type `export REALM=us1` and for `eu0` type `export REALM=eu0` etc.

{{< tabs >}}
{{% tab title="Export ACCESS TOKEN" %}}

``` bash
export ACCESS_TOKEN="<replace_with_O11y-Workshop-ACCESS_TOKEN>"
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab title="Export REALM" %}}

``` bash
export REALM="<replace_with_REALM>"
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}
If you have completed the Splunk IM workshop, please ensure you have deleted the collector running in Kubernetes before continuing. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 3. Install the OpenTelemetry Collector

We can then go ahead and install the Collector. There are two additional parameters passed to the install script, they are `--with-instrumentation` and `--deployment-environment`. The `--with-instrumentation` option the installer will install the agent from the Splunk distribution of OpenTelemetry Java, which is then loaded automatically when the PetClinic Java application starts up. No configuration required!

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --with-instrumentation --deployment-environment $(hostname)-petclinic --realm $REALM -- $ACCESS_TOKEN
```

{{% notice style="info" title="AWS/EC2 instances" %}}
If you are attempting this workshop on an AWS/EC2 instance you will have to patch the collector to expose the hostname of the instance:

``` bash
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yaml
```

Once the `agent_config.yaml` has been patched, you will need to restart the collector:

``` bash
sudo systemctl restart splunk-otel-collector
```

{{% /notice %}}

Once the install is completed, you can navigate to the **Hosts with agent installed** dashboard to see the data from your host, **Dashboards → Hosts with agent installed**.

Use the dashboard filter and select `host.name` and type or select the hostname of your virtual machine. Once you see data flowing for your host, we are then ready to get started with the APM component.
