---
title: Install the OpenTelemetry Collector in K8s
linkTitle: 7. Install the OpenTelemetry Collector in K8s
weight: 7
time: 15 minutes
---

## ワークショップ パート1のおさらい

ワークショップのこの時点で、以下を達成しています。

* Splunk distribution of the OpenTelemetry Collector を Linux ホストにデプロイ
* トレースとメトリクスを Splunk Observability Cloud に送信するように設定
* .NET アプリケーションをデプロイし、OpenTelemetry でインストルメンテーション
* .NET アプリケーションを Docker コンテナ化し、トレースが o11y cloud に流れていることを確認

上記の手順を**完了していない**場合は、ワークショップの残りに進む前に以下のコマンドを実行してください。

``` bash
cp /home/splunk/workshop/docker-k8s-otel/docker/Dockerfile /home/splunk/workshop/docker-k8s-otel/helloworld/
cp /home/splunk/workshop/docker-k8s-otel/docker/entrypoint.sh /home/splunk/workshop/docker-k8s-otel/helloworld/
````

> **重要** これらのファイルをコピーした後、`/home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile` をエディタで開き、Dockerfile 内の `$INSTANCE` をご自身のインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行することで確認できます。

## ワークショップ パート2の紹介

ワークショップの次のパートでは、アプリケーションを Kubernetes 上で実行したいので、Splunk distribution of the OpenTelemetry Collector を Kubernetes クラスターにデプロイする必要があります。

まず、いくつかの重要な用語を定義しましょう。

### 重要な用語

#### Kubernetes とは?

_「Kubernetes は、コンテナ化されたワークロードとサービスを管理するための、ポータブルで拡張可能なオープンソースのプラットフォームであり、宣言的な構成と自動化の両方を促進します。」_

出典: <https://kubernetes.io/docs/concepts/overview/>

先ほどアプリケーション用にビルドした Docker イメージを、Dockerfile に少し修正を加えた後、Kubernetes クラスターにデプロイします。

#### Helm とは?

Helm は Kubernetes のパッケージマネージャーです。

_「Helm は、最も複雑な Kubernetes アプリケーションでさえも、定義、インストール、アップグレードするのを支援します。」_

出典: <https://helm.sh/>

Helm を使用して、OpenTelemetry collector を K8s クラスターにデプロイします。

#### Helm のメリット

* 複雑さの管理
  * 何十ものマニフェストファイルではなく、単一の values.yaml ファイルで対応できる
* 簡単なアップデート
  * インプレースアップグレード
* ロールバックのサポート
  * helm rollback を使うだけでリリースの古いバージョンに戻せる

## ホストコレクターのアンインストール

先に進む前に、Linux ホストに以前インストールしたコレクターを削除しましょう。

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

## Helm を使ったコレクターのインストール

製品内のウィザードではなくコマンドラインを使って、コレクターをインストールするための独自の `helm` コマンドを作成しましょう。

まず、helm リポジトリを追加する必要があります。

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

そして、リポジトリが最新であることを確認します。

``` bash
helm repo update
```

helm chart のデプロイを構成するため、`/home/splunk` ディレクトリに `values.yaml` という名前の新しいファイルを作成しましょう。

``` bash
# swith to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

> 以下のテキストを貼り付ける前に、vi で 'i' を押して挿入モードに入ってください。

そして、以下の内容を貼り付けます。

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

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

これで、以下のコマンドを使用してコレクターをインストールできます。

{{< tabs >}}
{{% tab title="Script" %}}

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

## コレクターが動作していることを確認する

以下のコマンドでコレクターが動作しているかどうかを確認できます。

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

Splunk Observability Cloud で **Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、ご自身のクラスター名（`$INSTANCE-cluster`）を検索します。

![Kubernetes node](../images/k8snode.png)
