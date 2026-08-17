---
title: OpenTelemetry Collector のデプロイと設定のカスタマイズ
linkTitle: 2. OpenTelemetry Collector のデプロイと設定のカスタマイズ
weight: 2
time: 15 minutes
---

「データを取り込む」ための最初のステップは、OpenTelemetry Collector をデプロイすることです。Collector は環境内のテレメトリデータを受信・処理し、Splunk Observability Cloud にエクスポートします。

このワークショップでは Kubernetes を使用し、Helm を使って K8s クラスターに Collector をデプロイします。

## Helm とは

Helm は Kubernetes 用のパッケージマネージャーで、以下のメリットがあります

* 複雑さの管理
  * 数十のマニフェストファイルの代わりに、1つの values.yaml ファイルで管理できます
* 簡単なアップデート
  * インプレースアップグレードが可能です
* ロールバックのサポート
  * helm rollback を使用するだけで、リリースの古いバージョンにロールバックできます

## Helm を使用した Collector のインストール

正しいディレクトリに移動し、スクリプトを実行して Collector をインストールします。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd /home/splunk/workshop/tagging
./1-deploy-otel-collector.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
"splunk-otel-collector-chart" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
NAME: splunk-otel-collector
LAST DEPLOYED: Mon Dec 23 18:47:38 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

> スクリプトの実行には1分ほどかかる場合があります。

このスクリプトはどのように Collector をインストールしたのでしょうか？まず、`~./profile` ファイルに設定された環境変数が読み込まれていることを確認します。

> 重要：以下のコマンドは `1-deploy-otel-collector.sh` スクリプトによってすでに実行されているため、
> 手動で実行する必要はありません。

``` bash
source ~/.profile
```

次に、`splunk-otel-collector-chart` Helm チャートをインストールし、最新の状態に更新します。

``` bash
  helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
  helm repo update
```

最後に、`helm install` を使用して Collector をインストールします。

``` bash
  helm install splunk-otel-collector --version 0.149.0 \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-k3s-cluster" \
  --set="environment=tagging-workshop-$INSTANCE" \
  splunk-otel-collector-chart/splunk-otel-collector \
  -f otel/values.yaml
```

> `helm install` コマンドは `values.yaml` ファイルを参照しており、このファイルは Collector の設定を
> カスタマイズするために使用されます。詳細については以下で説明します。

## Collector が実行中であることを確認する

以下のコマンドで Collector が実行中かどうかを確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                            READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-kfvjb                               1/1     Running   0          2m33s
splunk-otel-collector-certmanager-7d89558bc9-2fqnx              1/1     Running   0          2m33s
splunk-otel-collector-certmanager-cainjector-796cc6bd76-hz4sp   1/1     Running   0          2m33s
splunk-otel-collector-certmanager-webhook-6959cd5f8-qd5b6       1/1     Running   0          2m33s
splunk-otel-collector-k8s-cluster-receiver-57569b58c8-8ghds     1/1     Running   0          2m33s
splunk-otel-collector-operator-6fd9f9d569-wd5mn                 2/2     Running   0          2m33s
```

{{% /tab %}}
{{< /tabs >}}

## K8s クラスターが O11y Cloud に表示されていることを確認する

Splunk Observability Cloud で、**Infrastructure** → **Kubernetes** → **Kubernetes Clusters** に移動し、クラスター名（`$INSTANCE-k3s-cluster`）を検索します。

![Kubernetes node](../images/k8snode.png)

## Collector の設定を取得する

Collector の設定をカスタマイズする前に、現在の設定がどのようになっているかを確認しましょう。

Kubernetes 環境では、Collector の設定は Config Map を使用して保存されています。

以下のコマンドで、クラスター内に存在する Config Map を確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get cm -l app=splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                 DATA   AGE
splunk-otel-collector-otel-k8s-cluster-receiver   1      3h37m
splunk-otel-collector-otel-agent                  1      3h37m
```

{{% /tab %}}
{{< /tabs >}}

次に、Collector エージェントの Config Map を以下のように表示できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Name:         splunk-otel-collector-otel-agent
Namespace:    default
Labels:       app=splunk-otel-collector
              app.kubernetes.io/instance=splunk-otel-collector
              app.kubernetes.io/managed-by=Helm
              app.kubernetes.io/name=splunk-otel-collector
              app.kubernetes.io/version=0.113.0
              chart=splunk-otel-collector-0.113.0
              helm.sh/chart=splunk-otel-collector-0.113.0
              heritage=Helm
              release=splunk-otel-collector
Annotations:  meta.helm.sh/release-name: splunk-otel-collector
              meta.helm.sh/release-namespace: default

Data
====
relay:
----
exporters:
  otlphttp:
    headers:
      X-SF-Token: ${SPLUNK_OBSERVABILITY_ACCESS_TOKEN}
    metrics_endpoint: https://ingest.us1.signalfx.com/v2/datapoint/otlp
    traces_endpoint: https://ingest.us1.signalfx.com/v2/trace/otlp
    (followed by the rest of the collector config in yaml format) 
```

{{% /tab %}}
{{< /tabs >}}

## K8s で Collector の設定を更新する方法

`values.yaml` ファイルを使用して、K8s の Collector 設定をカスタマイズできます。

> `values.yaml` ファイルで利用可能なカスタマイズオプションの包括的なリストについては、
> [このファイル](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml)を参照してください。

例を見てみましょう。

### Debug Exporter の追加

Collector に送信されるトレースを確認したい場合、debug exporter を使用できます。これは OpenTelemetry 関連の問題のトラブルシューティングに役立ちます。

`vi` または `nano` を使用して `values.yaml` ファイルを編集できます。ここでは vi を使用した例を示します。

``` bash
vi /home/splunk/workshop/tagging/otel/values.yaml
```

以下のテキストをコピーして `values.yaml` ファイルの末尾に貼り付け、debug exporter を追加します。

> 以下のテキストを追加する前に、vi で 'i' を押してインサートモードに入ってください。

``` yaml
    # NEW CONTENT
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - otlp_http
            - signalfx
            - debug
```

これらの変更後、`values.yaml` ファイルの内容は以下のようになります。

``` yaml
splunkObservability:
  profilingEnabled: true
  infrastructureMonitoringEventsEnabled: true
certmanager:
  enabled: true
operator:
  enabled: true
operatorcrds:
  install: true

agent:
  config:
    receivers:
      kubeletstats:
        insecure_skip_verify: true
        auth_type: serviceAccount
        endpoint: ${K8S_NODE_IP}:10250
        metric_groups:
          - container
          - pod
          - node
          - volume
        k8s_api_config:
          auth_type: serviceAccount
        extra_metadata_labels:
          - container.id
          - k8s.volume.type
    extensions:
      zpages:
        endpoint: 0.0.0.0:55679
    # NEW CONTENT
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - otlp_http
            - signalfx
            - debug
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから
> `enter/return` キーを押します。

ファイルを保存したら、以下のコマンドで変更を適用できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd /home/splunk/workshop/tagging

helm upgrade splunk-otel-collector  \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="environment=tagging-workshop-$INSTANCE" \
splunk-otel-collector-chart/splunk-otel-collector \
-f otel/values.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Mon Dec 23 19:08:08 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

`values.yaml` ファイルを通じて Collector の設定を変更した場合は、Config Map を確認して、Collector に適用された実際の設定をレビューすることをお勧めします。

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

期待どおり、debug exporter がトレースパイプラインに追加されていることが確認できます。

``` yaml
  traces:
    exporters:
    - otlp_http
    - signalfx
    - debug
```

アプリケーションをクラスターにデプロイしてトレースのキャプチャを開始したら、debug exporter の出力を確認します。
