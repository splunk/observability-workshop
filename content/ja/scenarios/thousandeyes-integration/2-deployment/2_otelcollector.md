---
title: OTel Collector
linkTitle: 2.2 OTel Collector
weight: 2
time: 15 minutes
description: OTel Collector をデプロイします。
---

次に OpenTelemetry Collector をデプロイします。

## インストール手順

### Step 1: OpenTelemetry Collector のデプロイ

アプリケーションがすでに計装されており、Splunk APM でトレースが確認できる場合は、Step 2 までスキップできます。そうでない場合、Kubernetes 上で最も早く学習を進めるには、Operator を有効化したゼロコード計装で Splunk OpenTelemetry Collector を使用するのが最善です。

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

クラスター名は次のとおりです:

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

クラスターが **Splunk Observability Cloud** に表示されているか確認します:

* **Infrastructure > Kubernetes Entities** に移動します
* 一覧にクラスターが表示されているはずです
  * 表示されるまで数分かかる場合があります

{{% notice title="Success" style="success" icon="check" %}}
クラスターが見つかれば、データは正しく送信されています。
{{% /notice %}}
