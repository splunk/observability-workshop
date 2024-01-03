---
title: Installing the OpenTelemetry Collector
linkTitle: 2. OpenTelemetry Collector
weight: 2
---

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
helm install splunk-otel-collector \
--set="operator.enabled=true", \
--set="certmanager.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.logsEnabled=false" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

## 1. Introduction

The Splunk OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, CPU, memory, etc)
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
HEC_TOKEN
HEC_URL
```

For this workshop, **all** of the above are required. If any are missing, please contact your instructor.

## 3. Install the OpenTelemetry Collector

We can then go ahead and install the Collector. Some additional parameters are passed to the install script, they are:

* `--with-instrumentation` - This will install the agent from the Splunk distribution of OpenTelemetry Java, which is then loaded automatically when the PetClinic Java application starts up. No configuration is required!
* `--deployment-environment` - Sets the resource attribute `deployment.environment` to the value passed. This is used to filter views in the UI.
* `--enable-profiler` - Enables the profiler for the Java application. This will generate CPU profiles for the application.
* `--enable-profiler-memory` - Enables the profiler for the Java application. This will generate memory profiles for the application.
* `--enable-metrics` - Enables the exporting of Micrometer metrics
* `--hec-token` - Sets the HEC token for the collector to use
* `--hec-url` - Sets the HEC URL for the collector to use

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN --mode agent --without-fluentd --with-instrumentation --deployment-environment $INSTANCE-petclinic --enable-profiler --enable-profiler-memory --enable-metrics --hec-token $HEC_TOKEN --hec-url $HEC_URL
```

When prompted to restart services, select 'OK' and press enter.

Next, we will patch the collector to expose the hostname of the instance and not the AWS instance ID. This will make it easier to filter data in the UI. Run the following command to patch the collector:

``` bash
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yaml
```

Once the `agent_config.yaml` has been patched, you will need to restart the collector:

``` bash
sudo systemctl restart splunk-otel-collector
```

Once the installation is completed, you can navigate to the **Hosts with agent installed** dashboard to see the data from your host, **Dashboards → Hosts with agent installed**.

Use the dashboard filter and select `host.name` and type or select the hostname of your workshop instance (you can get this from the command prompt in your terminal session). Once you see data flowing for your host, we are then ready to get started with the APM component.
