---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

このワークショップでは、Kubernetes で実行されている Agentic AI アプリケーションからメトリクス、トレース、ログをキャプチャするために OpenTelemetry を使用します。このセクションでは、Helm を使用して Kubernetes クラスターに OpenTelemetry Collector をインストールします。これにより、環境からメトリクス、トレース、ログをキャプチャして Splunk に送信します。

## Helm を使用して Collector をインストールする

まず、helm リポジトリを追加する必要があります

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

次に、リポジトリが最新であることを確認します

``` bash
helm repo update
```

helm chart のデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という名前の新しいファイルを作成します

``` bash
# swith to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

次に、以下の内容を貼り付けます

> 貼り付ける前に `:set paste` と入力して、`vi` がコードを自動インデントしないようにしてください。

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押してください。

このカスタム設定により、エクスポーターが受信したヒストグラムメトリクスは、SignalFx 形式に変換されることなく、OTLP 形式で Splunk Observability バックエンドに送信されます。この設定は、`gen_ai.evaluation.score` などの AI Agent Monitoring で使用されるヒストグラムメトリクスが期待通りに処理されることを確実にするために重要です。

これで、以下のコマンドを使用して Collector をインストールできます

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

## Collector が実行されていることを確認する

以下のコマンドで Collector が実行されているかどうかを確認できます

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

## K8s クラスターが O11y Cloud に表示されていることを確認する

Splunk Observability Cloud で、**Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`<あなたのインスタンス名>-cluster`）を検索します

![Kubernetes cluster](../images/k8scluster.png)

> ヒント：インスタンス名を忘れた場合は、`echo $INSTANCE` コマンドを使用してください
