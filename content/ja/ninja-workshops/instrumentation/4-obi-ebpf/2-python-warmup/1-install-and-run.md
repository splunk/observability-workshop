---
title: 1. アプリのインストールと実行
weight: 1
---

## Python環境のセットアップ

Phase 0ディレクトリに移動し、仮想環境を作成します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
cd ~/workshop/obi/01-obi-python
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
Collecting flask>=3.0,<4.0
  Downloading ...
Successfully installed flask-3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## Splunk認証情報の設定

認証情報を環境変数としてエクスポートします。各プレースホルダーを実際の値に置き換えてください。

{{% notice title="Exercise" style="green" icon="running" %}}
`env` と入力した際に、環境に `ACCESS_TOKEN`、`REALM`、`INSTANCE` の値が設定されている必要があります。

**存在しない場合は以下のようにエクスポートします**

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export INSTANCE="<YOUR_IDENTIFIER>"
```

{{% /notice %}}

## アプリの実行

Flaskアプリをバックグラウンドで起動します。

``` bash
python3 app.py &
```

起動時にアプリは単一の `app.heartbeat` メトリクスをSplunk Ingest APIに直接送信します。以下のように表示されます。

``` text
Heartbeat sent to Splunk (200)
 * Running on http://0.0.0.0:5150
```

まずEnterキーを押してプロンプトに戻ります。
次にエンドポイントにアクセスして動作を確認します。

``` bash
curl -s http://localhost:5150/hello | jq
```

以下のレスポンスが返されます。

``` json
127.0.0.1 - - [04/May/2026 13:10:16] "GET /hello HTTP/1.1" 200 -
{
  "host": "<YOUR_INSTANCE>",
  "message": "Hello from the OBI Workshop warm-up!"
}
```

## Splunkでの確認

1. [Splunk Observability Cloud UI](http://app.us1.signalfx.com)を開き（URLはワークショップの場所によって異なります）、Metric Finderで `app.heartbeat` を検索します（または[チャートを作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aapp.heartbeat)します）
2. 設定した値と一致する `host.name` 属性を持つメトリクスが表示されます。

![app.heartbeat](./images/heartbeat.png)

{{% notice title="注意" style="info" %}}
この時点で、アプリは実行されており、Splunkがデータを受信できることが確認できています。しかし、 **トレースはゼロ** でAPMは空です。アプリには計装コードが一切含まれていません。
{{% /notice %}}
