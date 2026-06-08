---
title: 1. アプリのインストールと実行
weight: 1
---

## 前提条件

### 必須

- Docker Engine 24+（イメージビルドと k3d 用）
- **k3d** v5+ および **kubectl**
- `curl`、`docker`、`kubectl` が使えるターミナル
- **Splunk Observability Cloud** の組織と **アクセストークン** および **レルム**
- サービス、トレース、MetricSets を表示するための APM 権限

{{< tabs >}}
{{% tab title="ツールの確認" %}}

```bash
docker info --format '{{.ServerVersion}}'
k3d version
kubectl version --client
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
28.4.0
k3d version v5.9.0
k3s version v1.35.5-k3s1 (default)
Client Version: v1.36.1
Kustomize Version: v5.8.1
```

{{% /tab %}}
{{< /tabs >}}

### オプション

- JSON 出力用の `jq`
- Python と HTTP ヘッダーの基本的な知識

これで k3d にアプリケーションサービスをデプロイする準備が整いました。

{{% exercise title="インストールと実行" %}}

### 環境のセットアップ

Phase 1 ディレクトリに移動し、仮想環境を作成します

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
cd ~/workshop/context-propagation/scripts
./1-start-lab.sh
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
Creating k3d cluster 'trace-workshop'...
INFO[0000] portmapping '8080:8080' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] portmapping '13133:13133' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] Prep: Network
INFO[0000] Created network 'k3d-trace-workshop'
INFO[0000] Created image volume k3d-trace-workshop-images ...
```

{{% /tab %}}
{{< /tabs >}}

### Splunk 認証情報の設定

認証情報を環境変数としてエクスポートします。各プレースホルダーを実際の値に置き換えてください

`env` と入力したときに、環境に `ACCESS_TOKEN` と `REALM` の値が設定されている必要があります。

``` bash
export CLUSTER_NAME=trace-workshop-"<YOUR_INITIALS>"
export WORKSHOP_ENV="trace-propagation-<YOUR-INITIALS>"
```

一部またはすべての値が存在しない場合は、以下のようにエクスポートしてください

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export CLUSTER_NAME=trace-workshop-"<YOUR_INITIALS>"
export WORKSHOP_ENV="trace-propagation-<YOUR-INITIALS>"
```

### アプリの実行

アプリはバックグラウンドで自動的に起動し、バリデーションチェックを実行して 2 件（最大 15 件）のリクエストを送信します。

期待される出力

``` json
{
  "order_id": "ord-70764",
  "product": "widget",
  "tier": "premium",
  "amount": 149.99,
  "inventory": true,
  "payment": true,
  "fulfilment": "dhl"
}
```

何も表示されない場合やエラーが発生した場合は、バリデーションスクリプトを実行してください。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
cd ~/workshop/context-propagation/scripts
./validate-services.sh
```

{{% /tab %}}
{{% tab title="サービス出力例" %}}

``` text
Health endpoints:
  OK    edge-proxy → storefront health
  OK    inventory-service health
  OK    payment-proxy health
  OK    payment-service health
  OK    order-service health
  OK    email-service health ...
```

{{% /tab %}}
{{% tab title="リクエスト出力例" %}}

``` json
{
  "order_id": "ord-56584",
  "product": "widget",
  "tier": "enterprise",
  "amount": 999.98,
  "inventory": true,
  "payment": true,
  "fulfilment": "fedex"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

### Splunk APM の確認

1. [Splunk Observability Cloud UI](http://app.us1.signalfx.com)（URL はワークショップの場所によって異なります）を開き、APM -> Service Map で `trace-propagation-<your initials>` を検索します
2. 結果は何も返されません。

{{% notice title="注意" style="info" %}}
この時点で、アプリは実行されていますが、Splunk にデータがないことが確認できます。アプリにはインストルメンテーションコードが一切含まれていません。
{{% /notice %}}
