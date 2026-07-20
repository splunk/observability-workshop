---
title: K8sにOpenTelemetry Collectorをインストールする
linkTitle: 7. K8sにOpenTelemetry Collectorをインストールする
weight: 7
time: 15 minutes
---

## ワークショップ パート1の振り返り

ワークショップのここまでで、以下を完了しました:

* LinuxホストにSplunkディストリビューションのOpenTelemetry Collectorをデプロイした
* トレースとメトリクスをSplunk Observability Cloudに送信するよう設定した
* .NETアプリケーションをデプロイし、OpenTelemetryで計装した
* .NETアプリケーションをDocker化し、トレースがo11y cloudに送信されていることを確認した

上記の手順を **まだ完了していない** 場合は、ワークショップの残りに進む前に以下のコマンドを実行してください:

``` bash
cp /home/splunk/workshop/docker-k8s-otel/docker/Dockerfile /home/splunk/workshop/docker-k8s-otel/helloworld/
cp /home/splunk/workshop/docker-k8s-otel/docker/entrypoint.sh /home/splunk/workshop/docker-k8s-otel/helloworld/
````

> **重要** これらのファイルをコピーしたら、`/home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile` をエディタで開き、Dockerfile内の `$INSTANCE` をインスタンス名に置き換えます。インスタンス名は `echo $INSTANCE` を実行して確認できます。

## ワークショップ パート2の概要

ワークショップの次のパートでは、アプリケーションをKubernetesで実行するため、KubernetesクラスターにSplunkディストリビューションのOpenTelemetry Collectorをデプロイする必要があります。

まず、いくつかの重要な用語を定義します。

### 重要な用語

#### Kubernetesとは

_「Kubernetesは、コンテナ化されたワークロードやサービスを管理するための、ポータブルで拡張可能なオープンソースプラットフォームであり、宣言的な設定と自動化の両方を容易にします。」_

出典: <https://kubernetes.io/docs/concepts/overview/>

先ほどビルドしたアプリケーションのDockerイメージを、Dockerfileに小さな修正を加えた後、Kubernetesクラスターにデプロイします。

#### Helmとは

HelmはKubernetesのパッケージマネージャーです。

_「最も複雑なKubernetesアプリケーションでも、定義、インストール、アップグレードを支援します。」_

出典: <https://helm.sh/>

Helmを使用して、K8sクラスターにOpenTelemetry Collectorをデプロイします。

#### Helmの利点

* 複雑さの管理
  * 数十のマニフェストファイルではなく、単一のvalues.yamlファイルで管理できる
* 簡単なアップデート
  * インプレースアップグレード
* ロールバックのサポート
  * helm rollbackを使用するだけで、リリースの古いバージョンにロールバックできる

## ホストCollectorのアンインストール

先に進む前に、Linuxホストにインストールした Collector を削除します:

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

## Helmを使用してCollectorをインストールする

製品内ウィザードではなくコマンドラインを使用して、Collectorをインストールする独自の `helm` コマンドを作成します。

まず、Helmリポジトリを追加します:

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

リポジトリを最新の状態にします:

``` bash
helm repo update
```

Helmチャートのデプロイを設定するために、`/home/splunk` ディレクトリに `values.yaml` という新しいファイルを作成します:

``` bash
# /home/splunk ディレクトリに移動
cd /home/splunk
# vi で values.yaml ファイルを作成
vi values.yaml
```

> 以下のテキストを貼り付ける前に、'i'キーを押してviの挿入モードに入ります。

次に、以下の内容を貼り付けます:

``` yaml
logsEngine: otel
agent:
  config:
    receivers:
      hostmetrics:
        collection_interval: 10s
        root_path: /hostfs
        scrapers:
          cpu: null
          disk: null
          filesystem:
            exclude_mount_points:
              match_type: regexp
              mount_points:
              - /var/*
              - /snap/*
              - /boot/*
              - /boot
              - /opt/orbstack/*
              - /mnt/machines/*
              - /Users/*
          load: null
          memory: null
          network: null
          paging: null
          processes: null
```

> viで変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押します。

以下のコマンドを使用してCollectorをインストールします:

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
  helm install splunk-otel-collector --version 0.149.0 \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
  splunk-otel-collector-chart/splunk-otel-collector 
```

{{% /tab %}}
{{% tab title="出力例" %}}

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

## Collectorが実行中であることを確認する

以下のコマンドでCollectorが実行中かどうかを確認できます:

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-dkn88                            1/1     Running   0          53s
splunk-otel-collector-agent-ksmh4                            1/1     Running   0          53s
splunk-otel-collector-agent-lc2lf                            1/1     Running   0          53s
splunk-otel-collector-k8s-cluster-receiver-dbf64995b-xgm9b   1/1     Running   0          53s
```

{{% /tab %}}
{{< /tabs >}}

## K8sクラスターがO11y Cloudに表示されることを確認する

Splunk Observability Cloudで、**Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`$INSTANCE-cluster`）を検索します:

![Kubernetes node](../images/k8snode.png)
