---
title: OTel Collector
linkTitle: 2.2 OTel Collector
weight: 2
time: 15 minutes
description: OTel Collector をデプロイします。
---

次に、OpenTelemetry Collector をデプロイします。

## インストール手順

### ステップ 1: OpenTelemetry Collector のデプロイ

アプリケーションが既にインストルメント済みで、トレースが Splunk APM に表示されている場合は、ステップ 2 に進んでください。そうでない場合、Kubernetes での最も速い学習パスは、Operator を有効にしたゼロコードインストルメンテーション付きの Splunk OpenTelemetry Collector を使用することです。

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

クラスター名は以下の通りです:

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

**Splunk Observability Cloud** でクラスターを確認します:

* **Infrastructure > Kubernetes Entities** に移動します
* リストにクラスターが表示されるはずです
  * 表示されるまでに数分かかる場合があります

{{% notice title="Success" style="success" icon="check" %}}
クラスターが見つかれば、データが正しく送信されています。
{{% /notice %}}
