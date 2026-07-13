---
title: クラスターの作成
linkTitle: 03. クラスターの作成
weight: 3
time: 15 minutes

---
このステップでは、k3dを使用してワークショップイメージ用のローカルコンテナレジストリを備えた軽量なKubernetesクラスターを作成します。

セットアップスクリプトは以下を作成します:

- `cosmic-shop` という名前のシングルサーバーk3dクラスター
- ワークショップイメージをプッシュするためのポート **5111** のローカルDockerレジストリ
- ショップUI（**30080**）とRabbitMQ管理UI（**15672**）のNodePortマッピング

## クラスターの作成

プロジェクトルートから実行します

{{< tabs >}}
{{% tab title="Script" %}}

```bash
make setup-k3d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Creating k3d cluster 'cosmic-shop' with local registry on port 5111...
...
k3d cluster 'cosmic-shop' ready.
```

{{% /tab %}}
{{< /tabs >}}

## 検証チェックリスト

#### 1. k3dクラスターの存在を確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
k3d cluster list
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAME         SERVERS   AGENTS   LOADBALANCER
cosmic-shop   1/1       1/1      true
```

{{% /tab %}}
{{< /tabs >}}

#### 2. Kubernetesへの接続を確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl cluster-info
kubectl get nodes
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
Kubernetes control plane is running at https://0.0.0.0:6443
...

NAME                       STATUS   ROLES                  AGE   VERSION
k3d-cosmic-shop-server-0   Ready    control-plane,master   45s   v1.28.x+k3s1
k3d-cosmic-shop-agent-0    Ready    <none>                 40s   v1.28.x+k3s1
```

すべてのノードのSTATUS列に `Ready` と表示されている必要があります。

{{% /tab %}}
{{< /tabs >}}

#### 3. k3dコンテナの実行を確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps --filter name=k3d-cosmic-shop --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
NAMES                     STATUS          PORTS
k3d-cosmic-shop-serverlb  Up 2 minutes    0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
k3d-cosmic-shop-server-0  Up 2 minutes
k3d-cosmic-shop-agent-0   Up 2 minutes
```

ロードバランサーがポート **30080** と **15672** を公開していることが表示されます。

{{% /tab %}}
{{< /tabs >}}

#### 4. RabbitMQのポートマッピングを明示的に確認

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```
0.0.0.0:30080->30080/tcp, 0.0.0.0:15672->15672/tcp, ...
```

**15672が表示されない** 場合、クラスターはRabbitMQのポートマッピングなしで作成されています。`make setup-k3d` でクラスターを再作成するまで、管理UIは <http://localhost:15672> で読み込めません（下記の[トラブルシューティング](#troubleshooting)を参照）。

{{% /tab %}}
{{< /tabs >}}

## トラブルシューティング

このステップで発生する可能性のある問題と推奨される対処方法を以下に示します。

{{< details summary="トラブルシューティングガイダンスはこちら" >}}

#### 問題1: ポートが既に使用されている

ポート30080または5111が使用中の場合、競合しているサービスを停止するか、`scripts/setup-k3d.sh` を編集して別のポートを使用してください。

#### 問題2: RabbitMQ UIが読み込めない（ロードバランサーに15672がない）

<http://localhost:15672> が読み込めない場合、k3dがポートをマッピングしているか確認します

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
```

**`15672` がない場合: クラスターを再作成せずに回避する方法** - 別のターミナルでport-forwardを実行します

```bash
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

そのターミナルを開いたまま、<http://localhost:15672（`guest`> / `guest`）を開きます。

#### 問題3: クラスターが既に存在する

`cosmic-shop` という名前のクラスターが既に存在する場合、スクリプトは作成をスキップします。最初からやり直すには以下を実行します

```bash
k3d cluster delete cosmic-shop
make setup-k3d
```

{{< /details >}}
