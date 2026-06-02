---
title: 1. アプリのインストールと実行
weight: 1
---

## Python 環境のセットアップ

Phase 0 のディレクトリに移動し、仮想環境を作成します。

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

認証情報を環境変数としてエクスポートします。各プレースホルダーを実際の値に置き換えてください。

{{% notice title="Exercise" style="green" icon="running" %}}
`env` を実行したときに、環境変数として `ACCESS_TOKEN`、`REALM`、`INSTANCE` の値が設定されている必要があります。

**設定されていない場合は、次のようにエクスポートしてください**

``` bash
export ACCESS_TOKEN="<YOUR_TOKEN>"
export REALM="<YOUR_REALM>"
export INSTANCE="<YOUR_IDENTIFIER>"
```

{{% /notice %}}

## アプリの実行

Flask アプリをバックグラウンドで起動します。

``` bash
python3 app.py &
```

起動時に、アプリは `app.heartbeat` メトリクスを Splunk Ingest API に直接 1 件送信します。次のような出力が表示されます。

``` text
Heartbeat sent to Splunk (200)
 * Running on http://0.0.0.0:5150
```

まず Return キーを押してプロンプトに戻ります。
次に、エンドポイントにアクセスして動作を確認します。

``` bash
curl -s http://localhost:5150/hello | jq
```

次のようなレスポンスが返ってくるはずです。

``` json
127.0.0.1 - - [04/May/2026 13:10:16] "GET /hello HTTP/1.1" 200 -
{
  "host": "<YOUR_INSTANCE>",
  "message": "Hello from the OBI Workshop warm-up!"
}
```

## Splunk での確認

1. [Splunk Observability Cloud UI](http://app.us1.signalfx.com) を開き（URL はワークショップの開催場所によって異なります）、Metric Finder で `app.heartbeat` を検索します（または [チャートを作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aapp.heartbeat) します）。
2. 設定した値と一致する `host.name` 属性を持つメトリクスが表示されているはずです。

![app.heartbeat](./images/heartbeat.png)

{{% notice title="Note" style="info" %}}
この時点で、アプリは稼働しており、Splunk がデータを受信できることも確認できました。しかし、**トレースは 1 件もありません**。APM は空のままです。アプリには計装コードがまったく組み込まれていないからです。
{{% /notice %}}
