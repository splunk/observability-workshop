---
title: Apache OTel Receiver
linkTitle: 3. Apache OTel Receiver
weight: 3
---

## 1. PHP/Apache 用 OTel receiver の確認

YAML ファイル `~/workshop/k3s/otel-apache.yaml` を確認するため、以下のコマンドで内容を検証します。

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

## 2. OpenTelemetry 設定における Observation Rule

上記のファイルには、OTel の `receiver_creator` を用いた Apache の観測ルール（observation rule）が含まれています。この receiver は、観測されたエンドポイントが設定されたルールに合致するかどうかに基づき、実行時に他の receiver をインスタンス化できます。

設定されたルールは、検出された各エンドポイントに対して評価されます。ルールが true と評価されると、そのルールに対応する receiver が、合致したエンドポイントに対して設定通りに起動されます。

上記のファイルでは、OpenTelemetry エージェントに、名前が `apache` に合致し、ポート `80` が開いている Pod を探すように指示しています。見つかると、エージェントは設定された URL から Apache メトリクスを読み取るように Apache receiver を構成します。なお、上記の YAML 内のサービスに対する URL は、K8s の DNS ベースの URL になっている点に注意してください。

Apache の設定を利用するには、以下のコマンドで既存の Splunk OpenTelemetry Collector Helm チャートをアップグレードし、`otel-apache.yaml` ファイルを利用するようにします。

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

{{% notice title="NOTE" style="info" %}}
デプロイメントの **REVISION** 番号が変更されており、これは変更履歴を追跡するのに役立ちます。

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

ConfigMap は、アプリケーションに注入可能なキーと値のペアで構成される Kubernetes のオブジェクトです。ConfigMap を利用することで、設定を Pod から分離できます。

ConfigMap を使うことで、設定データのハードコーディングを避けられます。ConfigMap は、機密性のない暗号化されていない設定情報を保存・共有するのに便利です。

OpenTelemetry collector/agent は、エージェントと K8s Cluster receiver の設定を保存するために ConfigMap を使用します。変更後にエージェントの現在の設定を確認するには、いつでも以下のコマンドを実行できます。

``` bash
kubectl get cm
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
collector はいくつの ConfigMap を使用していますか？
{{% /notice %}}

namespace 内の ConfigMap 一覧を取得したら、`otel-agent` 用のものを選択し、以下のコマンドで内容を確認します。

``` bash
kubectl get cm splunk-otel-collector-otel-agent -o yaml
```

{{% notice title="NOTE" style="info" %}}
`-o yaml` オプションを指定すると、ConfigMap の内容が読みやすい YAML 形式で出力されます。
{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
`otel-apache.yaml` の設定が、collector agent の ConfigMap で確認できますか？
{{% /notice %}}
