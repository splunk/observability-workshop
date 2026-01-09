---
title: Apache OTel Receiver
linkTitle: 3. Apache OTel Receiver
weight: 3
---

## 1. PHP/Apache 用の OTel Receiver の確認

YAML ファイル `~/workshop/k3s/otel-apache.yaml` を確認し、以下のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/otel-apache.yaml
```

このファイルには、PHP/Apache デプロイメントを監視するための OpenTelemetry エージェントの設定が含まれています。

```yaml
agent:
  config:
    receivers:
      receiver_creator:
        receivers:
          apache:
            rule: type == "port" && pod.name matches "apache" && port == 80
            config:
              endpoint: http://php-apache-svc.apache.svc.cluster.local/server-status?auto
```

## 2. OpenTelemetry 設定における観測ルール

上記のファイルには、OTel `receiver_creator` を使用した Apache の観測ルールが含まれています。この Receiver は、観測されたエンドポイントが設定されたルールに一致するかどうかに基づいて、実行時に他の Receiver をインスタンス化できます。

設定されたルールは、検出された各エンドポイントに対して評価されます。ルールが true と評価された場合、そのルールの Receiver は、一致したエンドポイントに対して設定どおりに開始されます。

上記のファイルでは、OpenTelemetry エージェントに対して、名前が `apache` に一致し、ポート `80` が開いている Pod を探すように指示しています。見つかると、エージェントは設定された URL から Apache メトリクスを読み取る Apache Receiver を設定します。上記の YAML 内のサービス用の K8s DNS ベースの URL に注目してください。

Apache 設定を使用するには、以下のコマンドで既存の Splunk OpenTelemetry Collector Helm チャートをアップグレードして `otel-apache.yaml` ファイルを使用します:

{{< tabs >}}
{{% tab title="Helm Upgrade" %}}

``` bash
helm upgrade splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml \
-f ~/workshop/k3s/otel-apache.yaml
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="注意" style="info" %}}
デプロイメントの **REVISION** 番号が変更されました。これは変更を追跡するのに便利な方法です。

``` text
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Mon Nov  4 14:56:25 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-workshop.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.
```

{{% /notice %}}

## 3. Kubernetes ConfigMaps

ConfigMap は、アプリケーションに注入できるキーと値のペアで構成される Kubernetes のオブジェクトです。ConfigMap を使用すると、設定を Pod から分離できます。

ConfigMap を使用すると、設定データのハードコーディングを防ぐことができます。ConfigMap は、機密性のない暗号化されていない設定情報を保存および共有するのに便利です。

OpenTelemetry Collector/エージェントは、ConfigMap を使用してエージェントと K8s Cluster Receiver の設定を保存します。変更後にエージェントの現在の設定を確認するには、以下のコマンドを実行します:

``` bash
kubectl get cm
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Collector で使用されている ConfigMap はいくつありますか？
{{% /notice %}}

Namespace から ConfigMap のリストを取得したら、`otel-agent` 用のものを選択し、以下のコマンドで表示します:

``` bash
kubectl get cm splunk-otel-collector-otel-agent -o yaml
```

{{% notice title="注意" style="info" %}}
オプション `-o yaml` は、ConfigMap の内容を読みやすい YAML 形式で出力します。
{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
`otel-apache.yaml` の設定は、Collector エージェントの ConfigMap に表示されていますか？
{{% /notice %}}
