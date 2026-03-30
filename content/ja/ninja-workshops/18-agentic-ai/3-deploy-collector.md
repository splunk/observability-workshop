---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

## Helm を使用した Collector のインストール

製品内ウィザードではなく、コマンドラインを使用して独自の `helm` コマンドを作成し、Collectorをインストールしましょう。

まず、helmリポジトリを追加する必要があります：

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

次に、リポジトリが最新であることを確認します：

``` bash
helm repo update
```

Helmチャートのデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という名前の新しいファイルを作成しましょう：

``` bash
# swith to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

> 以下のテキストを貼り付ける前に、'i' キーを押して vi の挿入モードに入ってください。

次に、以下の内容を貼り付けます：

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

これで、以下のコマンドを使用してCollectorをインストールできます：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
  helm upgrade --install splunk-otel-collector --version {{< otel-version >}} \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=agentic-ai-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
  splunk-otel-collector-chart/splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:01:43 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

## Collector の動作確認

以下のコマンドでCollectorが動作しているかどうかを確認できます：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-dkn88                            1/1     Running   0          53s
splunk-otel-collector-agent-ksmh4                            1/1     Running   0          53s
splunk-otel-collector-agent-lc2lf                            1/1     Running   0          53s
splunk-otel-collector-k8s-cluster-receiver-dbf64995b-xgm9b   1/1     Running   0          53s
```

{{% /tab %}}
{{< /tabs >}}

## K8s クラスターが O11y Cloud に表示されていることを確認

Splunk Observability Cloudで、**Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`$INSTANCE-cluster`）を検索します：

![Kubernetes node](../images/k8snode.png)
