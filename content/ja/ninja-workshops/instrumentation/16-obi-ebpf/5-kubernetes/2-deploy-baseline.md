---
title: 2. ベースラインのデプロイ
weight: 2
---

## ワークショップアプリケーションのデプロイ

アプリケーションは独自の名前空間にデプロイします。

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

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) は、Collector を Kubernetes にデプロイする本番運用向けの方法です。Collector のデプロイメント、サービス、設定を自動的に処理します。

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

ここでは OBI を有効化**せずに** Splunk OTel Collector をインストールします。次のステップで OBI を有効化し、有効化前後の違いを確認します。

{{% notice title="Note" style="info" %}}
環境変数 `ACCESS_TOKEN`、`REALM`、`INSTANCE` は、ワークショップインスタンスにあらかじめ設定されています。`env` を実行して存在を確認してください。
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

## すべてが稼働していることの確認

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

NodePort 経由でフロントエンドにアクセスします。

``` bash
kubectl port-forward -n obi-workshop svc/frontend 30000:3000 &; sleep 5
```

ポートフォワードが完了したら、curl でページにアクセスできます。

``` bash
curl -s http://localhost:30000/create-order | jq
```

## APM が空であることの確認

{{% notice title="Exercise" style="green" icon="running" %}}

Splunk APM を開き、environment `<INSTANCE>-ebpf` でフィルタリングしてください。Collector からのインフラメトリクスは表示されますが、**新規のアプリケーショントレースはまだ表示されない**はずです。サービスは稼働していますが、まだ計装されていない状態です。

{{% /notice %}}
