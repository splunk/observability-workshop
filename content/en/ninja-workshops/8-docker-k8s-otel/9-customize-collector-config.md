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

> Why are there two config maps? 

We can then view the config map of the collector agent as follows:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Name:         splunk-otel-collector-otel-agent
Namespace:    default
Labels:       app=splunk-otel-collector
              app.kubernetes.io/instance=splunk-otel-collector
              app.kubernetes.io/managed-by=Helm
              app.kubernetes.io/name=splunk-otel-collector
              app.kubernetes.io/version=0.113.0
              chart=splunk-otel-collector-0.113.0
              helm.sh/chart=splunk-otel-collector-0.113.0
              heritage=Helm
              release=splunk-otel-collector
Annotations:  meta.helm.sh/release-name: splunk-otel-collector
              meta.helm.sh/release-namespace: default

Data
====
relay:
----
exporters:
  otlphttp:
    headers:
      X-SF-Token: ${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}
    metrics_endpoint: https://ingest.us1.signalfx.com/v2/datapoint/otlp
    traces_endpoint: https://ingest.us1.signalfx.com/v2/trace/otlp
    (followed by the rest of the collector config in yaml format) 
```

{{% /tab %}}
{{< /tabs >}}


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

> Hint: steps to open and save in vi are in previous steps. 

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
...
```

Once the file is saved, we can apply the changes with: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:17:03 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

We can then view the config map and ensure the changes were applied:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-k8s-cluster-receiver
```

{{% /tab %}}
{{% tab title="Example Output" %}}

Ensure `smartagent/kubernetes-events` is included in the agent config now: 

``` bash
  smartagent/kubernetes-events:
    alwaysClusterReporter: true
    type: kubernetes-events
    whitelistedEvents:
    - involvedObjectKind: Pod
      reason: Created
    - involvedObjectKind: Pod
      reason: Unhealthy
    - involvedObjectKind: Pod
      reason: Failed
    - involvedObjectKind: Job
      reason: FailedCreate
```

{{% /tab %}}
{{< /tabs >}}

> Note that we specified the cluster receiver config map since that's
> where these particular changes get applied. 

## Add the Debug Exporter 

Suppose we want to see the traces and logs that are sent to the collector, so we can 
inspect them before sending them to Splunk.  We can use the debug exporter for this purpose, which 
can be helpful for troubleshooting OpenTelemetry-related issues. 

Let's add the debug exporter to the bottom of the values.yaml file as follows: 

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - debug
        logs:
          exporters:
            - debug
```

Once the file is saved, we can apply the changes with:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:32:03 2024
NAMESPACE: default
STATUS: deployed
REVISION: 3
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

Exercise the application a few times using curl, then tail the agent collector logs with the
following command: 

``` bash
kubectl logs -l component=otel-collector-agent -f
```

You should see traces written to the agent collector logs such as the following: 

````
2024-12-20T01:43:52.929Z	info	Traces	{"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 2}
2024-12-20T01:43:52.929Z	info	ResourceSpans #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(78b452a43bbaa3354a3cb474010efd6ae2367165a1356f4b4000be031b10c5aa)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.pod.ip: Str(10.42.0.15)
     -> k8s.pod.labels.app: Str(helloworld)
     -> k8s.pod.name: Str(helloworld-84865965d9-nkqsx)
     -> k8s.namespace.name: Str(default)
     -> k8s.pod.uid: Str(38d39bc6-1309-4022-a569-8acceef50942)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
````

And log entries such as: 

````
2024-12-20T01:43:53.215Z	info	Logs	{"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 2}
2024-12-20T01:43:53.215Z	info	ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(78b452a43bbaa3354a3cb474010efd6ae2367165a1356f4b4000be031b10c5aa)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
````

If you return to Splunk Observability Cloud though, you'll notice that traces and logs are 
no longer being sent there by the application. 

Why do you think that is?  We'll explore it in the next section. 