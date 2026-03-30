---
title: 1. アプリのインストールと実行
weight: 1
---

## Python 環境のセットアップ

Phase 0ディレクトリに移動し、仮想環境を作成します:

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
`env` と入力したときに、環境に `ACCESS_TOKEN`、`REALM`、`INSTANCE` の値が設定されている必要があります。

**存在しない場合は、以下のようにエクスポートしてください**

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export INSTANCE="<YOUR_IDENTIFIER>"
```

{{% /notice %}}

## アプリの実行

Flaskアプリをバックグラウンドで起動します:

``` bash
python3 app.py &
```

起動時に、アプリは単一の `app.heartbeat` メトリクスをSplunk Ingest APIに直接送信します。以下のように表示されるはずです:

``` text
Heartbeat sent to Splunk (200)
 * Running on http://0.0.0.0:5150
```

エンドポイントにアクセスして、動作を確認します:

``` bash
curl http://localhost:5150/hello
```

以下のようなレスポンスが返されるはずです:

``` json
{
  "host": "<YOUR_INSTANCE>",
  "message": "Hello from the OBI Workshop warm-up!"
}
```

## Splunk での確認

1. [Metric Finder](https://app.signalfx.com/#/metrics) を開き、`app.heartbeat` を検索します
2. 設定した値と一致する `host.name` を持つメトリクスが表示されるはずです。

![app.heartbeat](./images/heartbeat.png)

{{% notice title="Note" style="info" %}}
この時点で、アプリが動作しており、Splunkがデータを受信できることが確認できました。しかし、**トレースはゼロ**です。APMは空の状態です。アプリには計装コードが一切含まれていません。
{{% /notice %}}
