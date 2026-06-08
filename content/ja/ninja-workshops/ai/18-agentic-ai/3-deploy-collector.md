---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

このワークショップでは、Kubernetes 上で動作する Agentic AI アプリケーションからメトリクス、トレース、ログをキャプチャするために OpenTelemetry を使用します。このセクションでは、Helm を使用して Kubernetes クラスターに OpenTelemetry Collector をインストールします。これにより、環境からメトリクス、トレース、ログをキャプチャし、Splunk に送信します。

## Helm を使用して Collector をインストールする

まず、helm リポジトリを追加する必要があります:

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

次に、リポジトリが最新であることを確認します:

``` bash
helm repo update
```

helm チャートのデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という名前の新しいファイルを作成します:

``` bash
# switch to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

次に、以下の内容を貼り付けます:

> [!TIP]
> 貼り付ける前に `:set paste` と入力してください。これにより、`vi` が貼り付けたコードを自動インデントするのを防ぎます。

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> [!TIP]
> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

このカスタム設定により、エクスポーターが受信したヒストグラムメトリクスは、SignalFx 形式に変換されることなく OTLP 形式で Splunk Observability バックエンドに送信されます。この設定は、`gen_ai.evaluation.score` などの AI Agent Monitoring で使用されるヒストグラムメトリクスが期待どおりに処理されるために重要です。

次のコマンドを使用して Collector をインストールします:

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

## Collector が動作していることを確認する

次のコマンドで Collector が動作しているかどうかを確認できます:

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

### 新しい Kubernetes エクスペリエンスを使用する場合

O11y Cloud で新しい Kubernetes エクスペリエンスを使用するように設定されている場合は、このセクションの手順に従ってください。それ以外の場合は、**従来の Kubernetes エクスペリエンスを使用する場合**のセクションを参照してください。

Splunk Observability Cloud で、**Infrastructure** -> **Kubernetes overview** に移動し、クラスター名（`<your instance name>-cluster`）を追加します:

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

![Kubernetes overview filter](../images/k8sOverviewFilter.png)

**Apply Filters** をクリックすると、以下のようなクラスターの概要が表示されます:

![Kubernetes overview new experience](../images/k8sOverviewNewExperience.png)

### 従来の Kubernetes エクスペリエンスを使用する場合

Splunk Observability Cloud で、**Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`<your instance name>-cluster`）を検索します:

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

![Kubernetes cluster](../images/k8scluster.png)
