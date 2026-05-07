---
title: K8s に OpenTelemetry Collector をインストールする
linkTitle: 7. Install the OpenTelemetry Collector in K8s
weight: 7
time: 15 minutes
---

## ワークショップの Part 1 のおさらい

ここまでのワークショップで、次の内容を完了しました。

* Splunk distribution of the OpenTelemetry Collector を Linux ホストにデプロイ
* トレースとメトリクスを Splunk Observability Cloud に送信するように設定
* .NET アプリケーションをデプロイし、OpenTelemetry で計装
* .NET アプリケーションを Docker 化し、トレースが o11y cloud に流れていることを確認

上記のステップを**完了していない**場合は、ワークショップの残りの部分に進む前に、次のコマンドを実行してください。

```bash
cp /home/splunk/workshop/docker-k8s-otel/docker/Dockerfile /home/splunk/workshop/docker-k8s-otel/helloworld/
cp /home/splunk/workshop/docker-k8s-otel/docker/entrypoint.sh /home/splunk/workshop/docker-k8s-otel/helloworld/
```

> **重要** これらのファイルをコピーしたら、`/home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile` をエディタで開き、Dockerfile 内の `$INSTANCE` をインスタンス名に置き換えてください。インスタンス名は `echo $INSTANCE` を実行することで確認できます。

## ワークショップの Part 2 の概要

ワークショップの次のパートでは、アプリケーションを Kubernetes で実行したいので、Splunk distribution of the OpenTelemetry Collector を Kubernetes クラスターにデプロイする必要があります。

まずいくつかの重要な用語を定義しましょう。

### 重要な用語

#### Kubernetes とは

_「Kubernetes は、コンテナ化されたワークロードとサービスを管理するための、ポータブルで拡張可能なオープンソースプラットフォームであり、宣言的な構成と自動化の両方を促進します。」_

ソース: <https://kubernetes.io/docs/concepts/overview/>

先ほど Docker イメージとしてビルドしたアプリケーションを、Dockerfile に少し変更を加えた上で Kubernetes クラスターにデプロイします。

#### Helm とは

Helm は Kubernetes のパッケージマネージャーです。

_「Helm は、最も複雑な Kubernetes アプリケーションでさえ定義、インストール、アップグレードするのに役立ちます。」_

ソース: <https://helm.sh/>

K8s クラスターに OpenTelemetry collector をデプロイするために Helm を使用します。

#### Helm の利点

* 複雑さの管理
  * 多数のマニフェストファイルではなく、1つの values.yaml ファイルを扱う
* 簡単なアップデート
  * インプレースアップグレード
* ロールバックのサポート
  * `helm rollback` を使うだけで、リリースを以前のバージョンに戻せる

## ホスト Collector のアンインストール

先に進む前に、Linux ホストに先ほどインストールした collector を削除しましょう。

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

## Helm を使った Collector のインストール

製品内のウィザードではなくコマンドラインを使って、独自の `helm` コマンドで collector をインストールしましょう。

まず helm リポジトリを追加します。

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

そしてリポジトリが最新であることを確認します。

```bash
helm repo update
```

helm chart のデプロイ設定のため、`/home/splunk` ディレクトリに `values.yaml` という新しいファイルを作成します。

```bash
# /home/splunk ディレクトリに移動
cd /home/splunk
# vi で values.yaml ファイルを作成
vi values.yaml
```

> 以下のテキストを貼り付ける前に、vi で `i` を押してインサートモードに入ります。

その後、次の内容を貼り付けます。

```yaml
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

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力した後に `enter/return` キーを押します。

これで、次のコマンドを使って collector をインストールできます。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
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

```bash
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

## Collector が実行中であることを確認

次のコマンドで collector が実行中かを確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-dkn88                            1/1     Running   0          53s
splunk-otel-collector-agent-ksmh4                            1/1     Running   0          53s
splunk-otel-collector-agent-lc2lf                            1/1     Running   0          53s
splunk-otel-collector-k8s-cluster-receiver-dbf64995b-xgm9b   1/1     Running   0          53s
```

{{% /tab %}}
{{< /tabs >}}

## K8s クラスターが O11y Cloud に表示されているか確認

Splunk Observability Cloud で **Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters** に移動し、クラスター名（`$INSTANCE-cluster`）で検索します。

![Kubernetes node](../images/k8snode.png)
