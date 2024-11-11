---

title: Deploy the Splunk OpenTelemetry Collector
linkTitle: 1. Deploy OpenTelemetry Collector
weight: 2
---

To get Observability signals (**metrics, traces** and **logs**) into **Splunk Observability Cloud** the Splunk OpenTelemetry Collector needs to be deployed into the Kubernetes cluster.

For this workshop, we will be using the Splunk OpenTelemetry Collector Helm Chart. First we need to add the Helm chart repository to Helm and update to ensure the latest version:

{{< tabs >}}
{{% tab title="Install Helm Chart" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Output" %}}

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

**Splunk Observability Cloud** offers wizards in the UI to walk you through the setup of the OpenTelemetry Collector on  Kubernetes, but in the interest of time, we will use the Helm install command below. Additional parameters are set to enable the operator and automatic discovery and configuration.

* `--set="operator.enabled=true"` - this will install the Opentelemetry operator that will be used to handle automatic discovery and configuration.
* `--set="certmanager.enabled=true"` - this will install the required certificate manager for the operator.
* `--set="splunkObservability.profilingEnabled=true"` - this enables Code Profiling via the operator.

To install the collector run the following command, do **NOT** edit this:

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
helm install splunk-otel-collector --version 0.111.0 \
--set="operator.enabled=true", \
--set="certmanager.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.profilingEnabled=true" \
--set="agent.service.enabled=true"  \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml

{{% /tab %}}
{{% tab title="Output" %}}

``` plaintext
LAST DEPLOYED: Fri Apr 19 09:39:54 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.

[INFO] You've enabled the operator's auto-instrumentation feature (operator.enabled=true)! The operator can automatically instrument Kubernetes hosted applications.
  - Status: Instrumentation language maturity varies. See `operator.instrumentation.spec` and documentation for utilized instrumentation details.
  - Splunk Support: We offer full support for Splunk distributions and best-effort support for native OpenTelemetry distributions of auto-instrumentation libraries.
```

{{% /tab %}}
{{< /tabs >}}

Ensure the Pods are reported as **Running** before continuing (this typically takes around 30 seconds).

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods | grep splunk-otel 
```

{{% /tab %}}
{{% tab title="Output" %}}

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

Ensure there are no errors reported by the Splunk OpenTelemetry Collector (press `ctrl + c` to exit) or use the installed **awesome** `k9s` terminal UI for bonus points!

{{< tabs >}}
{{% tab title="kubectl logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{% tab title="Output" %}}

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

>[!INFO] Deleting a failed installation
>If you make an error installing the OpenTelemetry Collector you can start over by deleting the
>installation with the following command:
>
>``` bash
>helm delete splunk-otel-collector
>```
