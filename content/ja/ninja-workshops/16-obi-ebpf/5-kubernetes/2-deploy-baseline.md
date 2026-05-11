---
title: 2. ベースラインのデプロイ
weight: 2
---

## ワークショップアプリケーションのデプロイ

アプリケーションは専用の namespace にデプロイします

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/03-obi-k8s
kubectl apply -f namespace.yaml
kubectl apply -f apps.yaml
kubectl apply -f load-generator.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
namespace/obi-workshop created
deployment.apps/frontend created
service/frontend created
deployment.apps/order-processor created
service/order-processor created
deployment.apps/payment-service created
service/payment-service created
deployment.apps/load-generator created
```

{{% /tab %}}
{{< /tabs >}}

## Splunk OTel Collector のインストール

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) は、Kubernetes に Collector をデプロイするための本番環境向けの方法です。Collector のデプロイメント、サービス、および設定を自動的に処理します。

### Helm リポジトリの追加

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
"splunk-otel-collector-chart" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

### Collector のインストール

ここでは OBI を**有効にせずに** Splunk OTel Collector をインストールします。次のステップで OBI を有効にして、ビフォー・アフターを確認します。

{{% notice title="Note" style="info" %}}
環境変数 `ACCESS_TOKEN`、`REALM`、`INSTANCE` はワークショップインスタンスに事前設定されています。`env` を実行して、これらが存在することを確認してください。
{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm -n obi-workshop install splunk-otel-collector \
  splunk-otel-collector-chart/splunk-otel-collector \
  --set="splunkObservability.realm=${REALM}" \
  --set="splunkObservability.accessToken=${ACCESS_TOKEN}" \
  --set="clusterName=${INSTANCE}-k8s" \
  --set="environment=${INSTANCE}-ebpf"
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME: splunk-otel-collector
LAST DEPLOYED: Thu Feb 27 22:30:15 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
```

{{% /tab %}}
{{< /tabs >}}

## すべてが実行中であることを確認

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n obi-workshop
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME                                     READY   STATUS    RESTARTS   AGE
frontend-7d8b9f4c5-x2k4n                1/1     Running   0          30s
load-generator-5c6d7e8f9-m3j2k          1/1     Running   0          28s
order-processor-8e9f0a1b2-p4q5r         1/1     Running   0          30s
payment-service-9f0a1b2c3-s6t7u         1/1     Running   0          30s

NAME                                                  READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-abc12                      1/1     Running   0          45s
splunk-otel-collector-cluster-receiver-xyz34           1/1     Running   0          45s
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションのテスト

NodePort を経由してフロントエンドにアクセスします

``` bash
kubectl port-forward -n obi-workshop svc/frontend 30000:3000 &; sleep 5
```

ポートフォワードが完了したら、curl でページにアクセスできます

``` bash
curl -s http://localhost:30000/create-order | jq
```

## APM が空であることを確認

{{% notice title="Exercise" style="green" icon="running" %}}

Splunk APM で環境 `<INSTANCE>-ebpf` をフィルタリングして確認してください。Collector からのインフラストラクチャメトリクスは表示されますが、**新しいアプリケーショントレースはまだ表示されない**はずです。サービスは実行中ですが、まだ計装されていません。

{{% /notice %}}
