---
title: K8sでOpenTelemetryコレクターをインストール
linkTitle: 7. K8sでOpenTelemetryコレクターをインストール
weight: 7
time: 15 minutes
---

## ワークショップパート 1 の振り返り

ワークショップのこの時点で、以下を正常に完了しました：

- Linux ホストに Splunk distribution of OpenTelemetry コレクターをデプロイ
- Splunk Observability Cloud にトレースとメトリクスを送信するよう設定
- .NET アプリケーションをデプロイし、OpenTelemetry で計装
- .NET アプリケーションを Docker 化し、o11y cloud にトレースが流れることを確認

上記のステップを**完了していない**場合は、ワークショップの残りの部分に進む前に以下のコマンドを実行してください：

```bash
cp /home/splunk/workshop/docker-k8s-otel/docker/Dockerfile /home/splunk/workshop/docker-k8s-otel/helloworld/
cp /home/splunk/workshop/docker-k8s-otel/docker/entrypoint.sh /home/splunk/workshop/docker-k8s-otel/helloworld/
```

> **重要** これらのファイルがコピーされたら、`/home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile` を
> エディターで開き、Dockerfile の `$INSTANCE` をあなたのインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行することで確認できます。

## ワークショップパート 2 の紹介

ワークショップの次の部分では、Kubernetes でアプリケーションを実行したいと思います。
そのため、Kubernetes クラスターに Splunk distribution of OpenTelemetry コレクターを
デプロイする必要があります。

まず、いくつかの重要な用語を定義しましょう。

### 重要な用語

#### Kubernetes とは何ですか？

_「Kubernetes は、宣言的な設定と自動化の両方を促進する、コンテナ化されたワークロードとサービスを管理するためのポータブルで拡張可能なオープンソースプラットフォームです。」_

Source: <https://kubernetes.io/docs/concepts/overview/>

Dockerfile に小さな修正を加えた後、アプリケーション用に以前ビルドした Docker イメージを
Kubernetes クラスターにデプロイします。

#### Helm とは何ですか？

Helm は Kubernetes 用のパッケージマネージャーです。

_「最も複雑な Kubernetes アプリケーションだとしても、定義、インストール、アップグレード役立ちます」_

#### Helm を使用したコレクターのインストール

プロダクト内ウィザードではなくコマンドラインを使用して、コレクターをインストールするための独自の
`helm`コマンドを作成しましょう。

まず、helm リポジトリを追加する必要があります：ます。」

Source: <https://helm.sh/>

Helm を使用して K8s クラスターに OpenTelemetry コレクターをデプロイします。

#### Helm の利点

- 複雑性の管理
  - 数十のマニフェストファイルではなく、単一の values.yaml ファイルを扱う
- 簡単な更新
  - インプレースアップグレード
- ロールバックサポート
  - helm rollback を使用してリリースの古いバージョンにロールバック

## ホストコレクターのアンインストール

先に進む前に、Linux ホストに先ほどインストールしたコレクターを削除しましょう：
\

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

## Helm を利用して Collector をインストールする

ウィザードの代わりに、コマンドラインを利用して collector をインストールします。

まず初めに、Helm リポジトリに登録する必要があります

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

リポジトリが最新であることを確認します：

```bash
helm repo update
```

helm チャートのデプロイメントを設定するために、`/home/splunk`ディレクトリに`values.yaml`という名前の新しいファイルを作成しましょう：

```bash
# swith to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```

> Press ‘i’ to enter into insert mode in vi before pasting the text below.　"i"を押下すると vi はインサートモードになります。ペースト前に押下してください

そして、下記のコードをコピーしてください

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

> vi での変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

次のコマンドを使用してコレクターをインストールできます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
  helm install splunk-otel-collector --version 0.111.0 \
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

## コレクターが実行中であることを確認

以下のコマンドでコレクターが実行されているかどうかを確認できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-8xvk8                            1/1     Running   0          49s
splunk-otel-collector-k8s-cluster-receiver-d54857c89-tx7qr   1/1     Running   0          49s
```

{{% /tab %}}
{{< /tabs >}}

## O11y Cloud で K8s クラスターを確認

Splunk Observability Cloud で、**Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters**にナビゲートし、
クラスター名（`$INSTANCE-cluster`）を検索します：

![Kubernetes node](../images/k8snode.png)
