---
title: Installing the OpenTelemetry Collector
linkTitle: 20. OpenTelemetry Collector
weight: 20
---

## 1. Introduction

The Splunk OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, CPU, memory, etc)
* Application Performance Monitoring (APM) traces
* Profiling data
* Host and Application logs

To get Observability signals into the **Splunk Observability Cloud** we need to add an OpenTelemetry Collector to our Kubernetes cluster.

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}
If you have completed a Splunk Observability workshop using this EC2 instance, please ensure you have deleted the collector running in Kubernetes before continuing with this workshop. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 2. Install the OpenTelemetry Collector using Helm

We are going to install the Splunk distribution of the OpenTelemetry Collector in Operator mode using the Splunk Kubernetes Helm Chart for the Opentelemetry collector. First, we need to add the Splunk Helm chart repository to Helm and update so it knows where to find it:

{{< tabs >}}
{{% tab title="Helm Repo Add" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Helm Repo Add Output" %}}

```text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

Splunk Observability Cloud offers wizards in the **Splunk Observability Suite** UI to walk you through the setup of the Collector on your infrastructure including Kubernetes, but in interest of time, we will use a setup created earlier. As we want the auto instrumentation to be available, we will install the OpenTelemetry Collector with the OpenTelemetry Collector Helm chart with some additional options:

* --set="operator.enabled=true" - this will install the Opentelemetry operator, that will be used to handle auto instrumentation
* --set="certmanager.enabled=true" - This will install the required certificate manager for the operator.
* --set="splunkObservability.profilingEnabled=true" - This enabled Code profiling via the operator

To install the collector run the following commands, do **NOT** edit this:

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
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

{{% /tab %}}
{{% tab title="Helm Install Output" %}}

``` text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
NAME: splunk-otel-collector
LAST DEPLOYED: Tue Jan  2 13:46:16 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-o11y-suite-eu0.stg.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.

[INFO] You've enabled the operator's auto-instrumentation feature (operator.enabled=true), currently considered ALPHA.
- Instrumentation library maturity varies (e.g., Java is more mature than Go). For library stability, visit: https://opentelemetry.io/docs/instrumentation/#status-and-releases
  - Some libraries may be enabled by default. For current status, see: https://github.com/open-telemetry/opentelemetry-operator#controlling-instrumentation-capabilities
  - Splunk provides best-effort support for native OpenTelemetry libraries, and full support for Splunk library distributions. For used libraries, refer to the values.yaml under "operator.instrumentation.spec".
```

{{% /tab %}}
{{< /tabs >}}

You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds.

Ensure the status is reported as **Running** before continuing.

{{< tabs >}}
{{% tab title="Kubectl Get Pods" %}}

``` bash
kubectl get pods|grep splunk-otel 
```

{{% /tab %}}
{{% tab title="Kubectl Get Pods Output" %}}

``` text
splunk-otel-collector-certmanager-cainjector-5c5dc4ff8f-95z49   1/1     Running   0          10m
splunk-otel-collector-certmanager-6d95596898-vjxss              1/1     Running   0          10m
splunk-otel-collector-certmanager-webhook-69f4ff754c-nghxz      1/1     Running   0          10m
splunk-otel-collector-k8s-cluster-receiver-6bd5567d95-5f8cj     1/1     Running   0          10m
splunk-otel-collector-agent-tspd2                               1/1     Running   0          10m
splunk-otel-collector-operator-69d476cb7-j7zwd                  2/2     Running   0          10m
```

{{% /tab %}}
{{< /tabs >}}

Ensure there are no errors by tailing the logs from the OpenTelemetry Collector pod. The output should look similar to the log output shown in the Output tab below.

Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit). Or use the installed `k9s` terminal UI for bonus points!

{{< tabs >}}
{{% tab title="Kubectl Logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{% tab title="Kubectl Logs Output" %}}

```text
2021-03-21T16:11:10.900Z        INFO    service/service.go:364  Starting receivers...
2021-03-21T16:11:10.900Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/watcher.go:195       Configured Kubernetes MetadataExporter  {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster", "exporter_name": "signalfx"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    healthcheck/handler.go:128      Health Check state change       {"component_kind": "extension", "component_type": "health_check", "component_name": "health_check", "status": "ready"}
2021-03-21T16:11:11.009Z        INFO    service/service.go:267  Everything is ready. Begin running and processing data.
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:59       Starting shared informers and wait for initial cache sync.      {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.281Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:75       Completed syncing shared informer caches.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Deleting a failed installation" style="info" %}}
If you make an error installing the OpenTelemetry Collector you can start over by deleting the installation using:

``` sh
helm delete splunk-otel-collector
```

{{% /notice %}}

## 3. Verify the installation by checking Metrics and Logs

Once the installation is completed, you can login into the  **Splunk Observability Cloud** with the URL provided by the Instructor.
First, Navigate to **Kubernetes Navigator** in the **Infrastructure**![infra](../images/infra-icon.png?classes=inline&height=25px) section to see the metrics from your cluster in the **K8s nodes** pane. Change the *Time* filter to the last 15 Minutes (-15m) to focus on the latest data.

Use the regular filter option at the top of the Navigator and select `k8s.cluster.name` **(1)** and type or select the cluster name of your workshop instance (you can get the unique part from your cluster name by using the `INSTANCE` from the output from the shell script you run earlier). (You can also select you cluster by clicking on on its image in the cluster pane.)

You should see metrics **(3)** & log events **(4)** related to your cluster. Also a `Mysql` pane **(5)** should appear,when you click on that pane, you can see the MySQL related metrics from you database.

![Navigator](../images/navigator.png)

Once you see data flowing for your host and mysql shows metrics as well, we are then ready to get started with the auto instrumentation component.
