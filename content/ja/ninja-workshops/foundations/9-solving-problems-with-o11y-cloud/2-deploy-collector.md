---
title: OpenTelemetry Collector のデプロイと設定のカスタマイズ
linkTitle: 2. OpenTelemetry Collector のデプロイと設定のカスタマイズ
weight: 2
time: 15 minutes
---

「データを取り込む」ための最初のステップは、OpenTelemetry collector をデプロイすることです。Collector は環境内でテレメトリデータを受信して処理し、Splunk Observability Cloud にエクスポートします。

このワークショップでは Kubernetes を使用し、Helm を使って K8s クラスター上に collector をデプロイします。

## Helm とは何か

Helm は Kubernetes のパッケージマネージャーで、次のようなメリットがあります。

* 複雑さの管理
  * 多数のマニフェストファイルではなく、単一の values.yaml ファイルで管理できます
* 簡単な更新
  * インプレースアップグレードが可能です
* ロールバックのサポート
  * helm rollback を使うだけで、リリースの古いバージョンに戻せます

## Helm を使った Collector のインストール

該当ディレクトリに移動して、collector をインストールするスクリプトを実行しましょう。

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

> このスクリプトの実行には1分ほどかかる場合があります。

このスクリプトはどのように collector をインストールしたのでしょうか？まず、`~./profile` ファイルに設定された環境変数が読み込まれることを確認します。

> 重要: 以下のコマンドは `1-deploy-otel-collector.sh` スクリプトによって既に実行されているため、改めて実行する必要はありません。

``` bash
source ~/.profile
```

次に `splunk-otel-collector-chart` Helm チャートをインストールし、最新の状態に更新します。

``` bash
  helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
  helm repo update
```

最後に、`helm install` を使って collector をインストールします。

``` bash
  helm install splunk-otel-collector --version 0.149.0 \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-k3s-cluster" \
  --set="environment=tagging-workshop-$INSTANCE" \
  splunk-otel-collector-chart/splunk-otel-collector \
  -f otel/values.yaml
```

> `helm install` コマンドは `values.yaml` ファイルを参照しており、これによって collector の設定をカスタマイズします。詳細については後ほど見ていきます。

## Collector が動作していることの確認

次のコマンドで collector が動作しているかどうかを確認できます。

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

## K8s クラスターが O11y Cloud に表示されていることの確認

Splunk Observability Cloud で **Infrastructure** → **Kubernetes** → **Kubernetes Clusters** に移動し、自分のクラスター名（`$INSTANCE-k3s-cluster`）を検索します。

![Kubernetes node](../images/k8snode.png)

## Collector の設定の取得

Collector の設定をカスタマイズする前に、現在の設定がどのようになっているかをどうやって確認すればよいでしょうか？

Kubernetes 環境では、collector の設定は Config Map に保存されます。

クラスター内に存在する config map は次のコマンドで確認できます。

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

次のコマンドで collector agent の config map を確認できます。

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

## K8s での Collector 設定の更新方法

K8s では `values.yaml` ファイルを使って collector の設定をカスタマイズできます。

> `values.yaml` ファイルで利用できるカスタマイズオプションの完全な一覧は、[このファイル](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/helm-charts/splunk-otel-collector/values.yaml) を参照してください。

例を見てみましょう。

### Debug Exporter の追加

Collector に送信されるトレースを確認したいとします。この用途には debug exporter が利用でき、OpenTelemetry 関連の問題のトラブルシューティングに役立ちます。

`values.yaml` ファイルの編集には `vi` または `nano` を使用できます。ここでは vi を使った例を示します。

``` bash
vi /home/splunk/workshop/tagging/otel/values.yaml
```

次のテキストをコピーして `values.yaml` ファイルの末尾に貼り付け、debug exporter を追加します。

> vi では、以下のテキストを追加する前に `i` キーを押して挿入モードに入ります。

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

これらの変更後、`values.yaml` ファイルには次のような内容が含まれているはずです。

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

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押します。

ファイルを保存したら、次のコマンドで変更を適用できます。

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

`values.yaml` ファイルで collector の設定を変更した際は、config map を確認して、collector に実際に適用されている設定をレビューすると役立ちます。

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

期待どおり、debug exporter が traces パイプラインに追加されていることが確認できます。

``` yaml
  traces:
    exporters:
    - otlp_http
    - signalfx
    - debug
```

Debug exporter の出力については、クラスターにアプリケーションをデプロイし、トレースのキャプチャを開始したあとで確認していきます。
