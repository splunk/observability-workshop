---
title: 1. アプリのインストールと実行
weight: 1
---

## Python 環境のセットアップ

Phase 0 のディレクトリに移動し、仮想環境を作成します:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/01-obi-python
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Collecting flask>=3.0,<4.0
  Downloading ...
Successfully installed flask-3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## Splunk 認証情報の設定

認証情報を環境変数としてエクスポートします。各プレースホルダーを実際の値に置き換えてください:

{{% notice title="Exercise" style="green" icon="running" %}}
`env` と入力したときに、`ACCESS_TOKEN`、`REALM`、`INSTANCE` の値が環境に設定されている必要があります。

**値が存在しない場合は、以下のようにエクスポートしてください**

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export INSTANCE="<YOUR_IDENTIFIER>"
```

{{% /notice %}}

## アプリの実行

Flask アプリをバックグラウンドで起動します:

``` bash
python3 app.py &
```

起動時にアプリは `app.heartbeat` メトリクスを Splunk Ingest API に直接送信します。以下のように表示されるはずです:

``` text
Heartbeat sent to Splunk (200)
 * Running on http://0.0.0.0:5150
```

まず Enter キーを押してプロンプトに戻ります。
次にエンドポイントにアクセスして、動作を確認します:

``` bash
curl -s http://localhost:5150/hello | jq
```

以下のレスポンスが返されるはずです:

``` json
127.0.0.1 - - [04/May/2026 13:10:16] "GET /hello HTTP/1.1" 200 -
{
  "host": "<YOUR_INSTANCE>",
  "message": "Hello from the OBI Workshop warm-up!"
}
```

## Splunk での確認

1. [Splunk Observability Cloud UI](http://app.us1.signalfx.com)（URL はワークショップの開催場所によって異なります）を開き、Metric Finder で `app.heartbeat` を検索します（または[チャートを作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aapp.heartbeat)してください）
2. 設定した値と一致する `host.name` 属性を持つメトリクスが表示されるはずです。

![app.heartbeat](./images/heartbeat.png)

{{% notice title="Note" style="info" %}}
この時点で、アプリは稼働しており、Splunk がデータを受信できることが確認できています。しかし、**トレースはゼロ**で、APM は空です。アプリにはインストルメンテーションコードが一切含まれていません。
{{% /notice %}}
