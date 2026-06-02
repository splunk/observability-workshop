---
title: Kubernetes における OpenTelemetry Collector のデプロイ
linkTitle: 1. OTel Collector のデプロイ
weight: 1
---

## 1. EC2 インスタンスへの接続

ワークショップインスタンスへは、Mac、Linux、Windows いずれのデバイスからも SSH を使用して接続できます。インストラクターから提供されたシートのリンクを開いてください。このシートには、ワークショップインスタンスの IP アドレスとパスワードが記載されています。

{{% notice style="info" %}}
ワークショップインスタンスには、本ワークショップ用の正しい **Access Token** と **Realm** が事前に設定されています。これらを設定する必要はありません。
{{% /notice %}}

## 2. Helm を使用した Splunk OTel のインストール

Splunk Helm chart を使用して OpenTelemetry Collector をインストールします。まず、Splunk Helm chart リポジトリを追加し、更新します。

{{< tabs >}}
{{% tab title="helm repo add" %}}

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="helm repo add output" %}}

```text
Using ACCESS_TOKEN=<REDACTED>
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN=<REDACTED>
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

以下のコマンドで OpenTelemetry Collector の Helm をインストールします。このコマンドは編集**しないでください**。

{{< tabs >}}
{{% tab title="helm install" %}}

``` bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

{{% /tab %}}
{{< /tabs >}}

## 3. デプロイの確認

`kubectl get pods` を実行することで、デプロイの進行状況を監視できます。通常、約 30 秒後に新しい Pod が起動して実行中であることが報告されます。

続行する前に、ステータスが **Running** と報告されていることを確認してください。

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

``` text
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-ks9jn                            1/1     Running   0          27s
splunk-otel-collector-agent-lqs4j                            0/1     Running   0          27s
splunk-otel-collector-agent-zsqbt                            1/1     Running   0          27s
splunk-otel-collector-k8s-cluster-receiver-76bb6b555-7fhzj   0/1     Running   0          27s
```

{{% /tab %}}
{{< /tabs >}}

`helm` インストール時に設定されたラベルを使って、ログを tail します（終了するには `ctrl + c` を押す必要があります）。

{{< tabs >}}
{{% tab title="kubectl logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{< /tabs >}}

または、インストール済みの `k9s` ターミナル UI を使用することもできます。

![k9s](../images/k9s.png)

{{% notice title="失敗したインストールの削除" style="warning" %}}
Splunk OpenTelemetry Collector のインストール中にエラーが発生した場合は、以下のコマンドでインストールを削除してやり直すことができます。

``` sh
helm delete splunk-otel-collector
```

{{% /notice %}}
