---
title: Apache OTel Receiver
linkTitle: 3. Apache OTel Receiver
weight: 3
---

## 1. PHP/Apache 用の OTel Receiver の確認

YAMLファイル `~/workshop/k3s/otel-apache.yaml` を確認し、以下のコマンドで内容を検証します:

``` bash
cat ~/workshop/k3s/otel-apache.yaml
```

このファイルには、PHP/Apacheデプロイメントを監視するためのOpenTelemetryエージェントの設定が含まれています。

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

上記のファイルには、OTel `receiver_creator` を使用したApacheの観測ルールが含まれています。このReceiverは、観測されたエンドポイントが設定されたルールに一致するかどうかに基づいて、実行時に他のReceiverをインスタンス化できます。

設定されたルールは、検出された各エンドポイントに対して評価されます。ルールがtrueと評価された場合、そのルールのReceiverは、一致したエンドポイントに対して設定どおりに開始されます。

上記のファイルでは、OpenTelemetryエージェントに対して、名前が `apache` に一致し、ポート `80` が開いているPodを探すように指示しています。見つかると、エージェントは設定されたURLからApacheメトリクスを読み取るApache Receiverを設定します。上記のYAML内のサービス用のK8s DNSベースのURLに注目してください。

Apache設定を使用するには、以下のコマンドで既存のSplunk OpenTelemetry Collector Helmチャートをアップグレードして `otel-apache.yaml` ファイルを使用します:

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

ConfigMapは、アプリケーションに注入できるキーと値のペアで構成されるKubernetesのオブジェクトです。ConfigMapを使用すると、設定をPodから分離できます。

ConfigMapを使用すると、設定データのハードコーディングを防ぐことができます。ConfigMapは、機密性のない暗号化されていない設定情報を保存および共有するのに便利です。

OpenTelemetry Collector/エージェントは、ConfigMapを使用してエージェントとK8s Cluster Receiverの設定を保存します。変更後にエージェントの現在の設定を確認するには、以下のコマンドを実行します:

``` bash
kubectl get cm
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
Collectorで使用されているConfigMapはいくつありますか？
{{% /notice %}}

NamespaceからConfigMapのリストを取得したら、`otel-agent` 用のものを選択し、以下のコマンドで表示します:

``` bash
kubectl get cm splunk-otel-collector-otel-agent -o yaml
```

{{% notice title="注意" style="info" %}}
オプション `-o yaml` は、ConfigMapの内容を読みやすいYAML形式で出力します。
{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
`otel-apache.yaml` の設定は、CollectorエージェントのConfigMapに表示されていますか？
{{% /notice %}}
