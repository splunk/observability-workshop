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

Splunk Observability Cloud offers a wizard to walk you through the setup of the Collector on both your infrastructure and applications.

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}
If you have completed the Splunk IM workshop, please ensure you have deleted the collector running in Kubernetes before continuing. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 2. Confirm environment variables

To ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following command:

``` bash
env
```

In the output check the following environment variables are present and have values set:

```text
ACCESS_TOKEN
REALM
RUM_TOKEN
```

For this workshop, **all** of the above are required. If any are missing, please contact your instructor.

## 3. Install the OpenTelemetry Collector

We can then go ahead and install the Collector. Some additional parameters are passed to the install script, they are:

* `--with-instrumentation` - This will install the agent from the Splunk distribution of OpenTelemetry Java, which is then loaded automatically when the PetClinic Java application starts up. No configuration is required!
* `--deployment-environment` - Sets the resource attribute `deployment.environment` to the value passed. This is used to filter views in the UI.
* `--enable-profiler` - Enables the profiler for the Java application. This will generate CPU profiles for the application.
* `--enable-profiler-memory` - Enables the profiler for the Java application. This will generate memory profiles for the application.
* `--enable-metrics` - Enables the exporting of Micrometer metrics

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN --mode agent --without-fluentd --with-instrumentation --deployment-environment $INSTANCE-petclinic --enable-profiler --enable-profiler-memory --enable-metrics
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
Once the installation is completed, you can navigate to the **Hosts with agent installed** dashboard to see the data from your host, **Dashboards → Hosts with agent installed**.

Use the dashboard filter and select `host.name` and type or select the hostname of your virtual machine. Once you see data flowing for your host, we are then ready to get started with the APM component.
