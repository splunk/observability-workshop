---
title: OTel Collector
linkTitle: 2.2 OTel Collector
weight: 2
time: 15 minutes
description: Deploy the OTel Collector.
---

Next we will deploy the open telemetry collector

## Installation Steps

### Step 1: Deploy the Open Telemetry Collector

If your application is already instrumented and traces are visible in Splunk APM, you can skip to Step 2. Otherwise, the fastest learning path in Kubernetes is to use the Splunk OpenTelemetry Collector with the Operator enabled for zero-code instrumentation.

{{< tabs >}}
{{% tab title="Script" %}}

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update

helm install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --set splunkObservability.realm=$REALM \
  --set splunkObservability.accessToken=$ACCESS_TOKEN \
  --set clusterName=$CLUSTER_NAME \
  --set environment="thousandeyes-$INSTANCE" \
  --set operator.enabled=true \
  --set operatorcrds.install=true \
  --set agent.service.enabled=true
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Using ACCESS_TOKEN=XXX
Using REALM=us1
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN=XXX
Using REALM=us1
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
Using ACCESS_TOKEN=XXX
Using REALM=us1
NAME: splunk-otel-collector
LAST DEPLOYED: Tue May 12 22:53:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.

[INFO] Auto-instrumentation is enabled (operator.enabled=true).
  Instrumentation CR: deployed as a regular Helm resource.

  If the Instrumentation CR was not created, see Troubleshooting:
  https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/auto-instrumentation-install.md#troubleshooting-the-operator
```

{{% /tab %}}
{{< /tabs >}}

Your cluster name is:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
export | grep CLUSTER_NAME
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
CLUSTER_NAME=shw-xxxx-cluster
```

{{% /tab %}}
{{< /tabs >}}

Check if your Cluster is in **Splunk Observability Cloud**:

* Go to **Infrastructure > Kubernetes Entities**
* You should see your cluster in the list
  * It may take several minutes for it to show up

{{% notice title="Success" style="success" icon="check" %}}
If you found your cluster you are sending data in correctly.
{{% /notice %}}
