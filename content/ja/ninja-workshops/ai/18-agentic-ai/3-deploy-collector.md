---
title: OpenTelemetry Collector のデプロイ
linkTitle: 3. OpenTelemetry Collector のデプロイ
weight: 3
time: 10 minutes
---

このワークショップでは、Kubernetes 上で実行されている Agentic AI アプリケーションからメトリクス、トレース、ログを収集するために OpenTelemetry を使用します。このセクションでは、Helm を使って Kubernetes クラスタに OpenTelemetry Collector をインストールします。これにより、環境からメトリクス、トレース、ログを収集して Splunk に送信できるようになります。

## Helm を使った Collector のインストール

まず、helm リポジトリを追加する必要があります。

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

そして、リポジトリが最新であることを確認します。

``` bash
helm repo update
```

helm chart のデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という新しいファイルを作成しましょう。

``` bash
# switch to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

そして、以下の内容を貼り付けます。

> 貼り付けたコードが `vi` によって自動インデントされるのを防ぐため、貼り付け前に `:set paste` と入力してください。

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

このカスタム設定により、エクスポーターが受信したヒストグラムメトリクスは、SignalFx 形式に変換されることなく OTLP 形式のまま Splunk Observability バックエンドに送信されます。この設定は、`gen_ai.evaluation.score` のような AI Agent Monitoring で使用されるヒストグラムメトリクスを期待どおりに処理するために重要です。

これで、以下のコマンドを使って Collector をインストールできます。

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

以下のコマンドで Collector が実行されているかを確認できます。

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

## K8s クラスタが O11y Cloud に表示されていることを確認する

### 新しい Kubernetes Experience を使用する場合

O11y Cloud で新しい Kubernetes Experience を使用する設定になっている場合は、このセクションの手順に従ってください。それ以外の場合は、**従来の Kubernetes Experience を使用する場合** のセクションを参照してください。

Splunk Observability Cloud で **Infrastructure** -> **Kubernetes overview** に移動し、クラスタ名（`<your instance name>-cluster`）を追加します。

> ヒント: インスタンス名を忘れた場合は、`echo $INSTANCE` コマンドを使ってください。

![Kubernetes overview filter](../images/k8sOverviewFilter.png)

**Apply Filters** をクリックすると、以下のようなクラスタの概要が表示されます。

![Kubernetes overview new experience](../images/k8sOverviewNewExperience.png)

### 従来の Kubernetes Experience を使用する場合

Splunk Observability Cloud で **Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスタ名（`<your instance name>-cluster`）を検索します。

> ヒント: インスタンス名を忘れた場合は、`echo $INSTANCE` コマンドを使ってください。

![Kubernetes cluster](../images/k8scluster.png)
