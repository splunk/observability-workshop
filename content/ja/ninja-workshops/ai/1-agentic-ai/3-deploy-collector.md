---
title: OpenTelemetry Collectorのデプロイ
linkTitle: 3. OpenTelemetry Collectorのデプロイ
weight: 3
time: 10 minutes
---

このワークショップでは、Kubernetesで動作するAgentic AIアプリケーションからメトリクス、トレース、ログを収集するためにOpenTelemetryを使用します。このセクションでは、Helmを使用してKubernetesクラスターにOpenTelemetry Collectorをインストールします。これにより、環境からメトリクス、トレース、ログを収集し、Splunkに送信します。

## Helmを使用してCollectorをインストール

まず、Helmリポジトリを追加します。

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

リポジトリを最新の状態に更新します。

``` bash
helm repo update
```

Helmチャートのデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という新しいファイルを作成します。

``` bash
# switch to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

次の内容を貼り付けます。

> [!TIP]
> 貼り付ける前に `:set paste` と入力して、`vi` が貼り付けたコードを自動インデントしないようにしてください。

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> [!TIP]
> viで変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

このカスタム設定により、Exporterが受信したヒストグラムメトリクスはSignalFx形式に変換されず、OTLP形式でSplunk Observabilityバックエンドに送信されます。この設定は、`gen_ai.evaluation.score` などのAI Agent Monitoringで使用されるヒストグラムメトリクスが期待どおりに処理されるために重要です。

次のコマンドを使用してCollectorをインストールします。

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

## Collectorの動作確認

次のコマンドでCollectorが動作しているか確認します。

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

## O11y CloudでK8sクラスターを確認

### 新しいKubernetesエクスペリエンスを使用する場合

O11y Cloudで新しいKubernetesエクスペリエンスを使用するように設定されている場合は、このセクションの手順に従ってください。それ以外の場合は、**従来のKubernetesエクスペリエンスを使用する場合** セクションを参照してください。

Splunk Observability Cloudで **Infrastructure** -> **Kubernetes overview** に移動し、クラスター名（`<your instance name>-cluster`）を追加します。

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

![Kubernetes overview filter](../images/k8sOverviewFilter.png)

**Apply Filters** をクリックすると、次のようなクラスターの概要が表示されます。

![Kubernetes overview new experience](../images/k8sOverviewNewExperience.png)

### 従来のKubernetesエクスペリエンスを使用する場合

Splunk Observability Cloudで **Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`<your instance name>-cluster`）を検索します。

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

![Kubernetes cluster](../images/k8scluster.png)
