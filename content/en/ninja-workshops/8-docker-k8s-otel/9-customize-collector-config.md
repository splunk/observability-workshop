---
title: Customize the OpenTelemetry Collector Configuration
linkTitle: 9. Customize the OpenTelemetry Collector Configuration
weight: 9
time: 20 minutes
---

We deployed the Splunk Distribution of the OpenTelemetry Collector in our K8s cluster 
using the default configuration. In this section, we'll walk through several examples 
showing how to customize the collector config. 

## Get the Collector Configuration

Before we customize the collector config, how do we determine what the current configuration 
looks like?  

In a Kubernetes environment, the collector configuration is stored using a Config Map. 

We can see which config maps exist in our cluster with the following command: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get cm -l app=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                 DATA   AGE
splunk-otel-collector-otel-k8s-cluster-receiver   1      3h37m
splunk-otel-collector-otel-agent                  1      3h37m
```

{{% /tab %}}
{{< /tabs >}}

We can then view the config map of the collector agent as follows: 

``` bash
kubectl describe cm my-splunk-otel-collector-otel-agent
```

## How to Update the Collector Configuration in K8s 

In our earlier example running the collector on a Linux instance, 
the collector configuration was available in the `/etc/otel/collector/agent_config.yaml` file.  If we 
needed to make changes to the collector config in that case, we'd simply edit this file, 
save the changes, and then restart the collector. 

In K8s, things work a bit differently.  Instead of modifying the `agent_config.yaml` directly, we'll 
instead customize the collector configuration by making changes to the `values.yaml` file used to deploy 
the helm chart.  

The values.yaml file in [GitHub](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml) 
describes the customization options that are available to us. 

Let's look at an example. 

## Add Infrastructure Events Monitoring 

For our first example, let's enable infrastructure events monitoring for our K8s cluster. 

This is done by add the following line to the `values.yaml` file: 

``` yaml
splunkObservability:
  realm: us1
  accessToken: ***
  infrastructureMonitoringEventsEnabled: true
clusterName: $INSTANCE-cluster
environment: otel-$INSTANCE
```

Once the file is saved, we can apply the changes with: 

``` bash
helm upgrade splunk-otel-collector -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

We can then view the config map and ensure the changes were applied:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm my-splunk-otel-collector-otel-k8s-cluster-receiver
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
TODO:  sample output
```

{{% /tab %}}
{{< /tabs >}}

