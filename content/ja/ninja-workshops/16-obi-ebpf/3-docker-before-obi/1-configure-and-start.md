---
title: 1. スタックの設定と起動
weight: 1
---

## Splunk 認証情報の追加

{{% notice title="演習" style="green" icon="running" %}}

**注:** 環境で `env` コマンドを使用して `ACCESS_TOKEN`、`REALM`、`INSTANCE` を取得してください。これらを設定ファイルに貼り付ける必要があります。

Phase 1/2 ディレクトリに移動し、エディタで `docker-compose.yaml` を開きます:

``` bash
cd ~/workshop/obi/02-obi-docker
vim docker-compose.yaml #or editor of choice
```

`splunk-otel-collector` サービスを見つけ、4つのプレースホルダー値を実際の認証情報に置き換えます:

``` yaml
    environment:
      SPLUNK_INGEST_TOKEN: "YOUR_ACCESS_TOKEN_HERE"       # <-- Your Splunk ingest token
      SPLUNK_REALM: "YOUR_REALM"                          # <-- Your realm (us0, us1, eu0, etc.)
      WORKSHOP_HOST_NAME: "<example: shw-ece9>"           # <-- the value from INSTANCE when you use `env` on terminal
      WORKSHOP_ENVIRONMENT: "<example: shw-ece9-ebpf>"    # <-- The hostname value above suffixed with `-ebpf`
```

ファイルを保存します。

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
**なぜ `WORKSHOP_HOST_NAME` と `WORKSHOP_ENVIRONMENT` が必要なのか？** ワークショップの参加者全員が同じ Splunk 組織にテレメトリを送信します。これらの値はすべてのメトリクスとトレースの `host.name` および `deployment.environment` 属性になるため、Splunk で**自分の**データをフィルタリングできます。
{{% /notice %}}

## スタックの起動

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker-compose up --build -d
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
[+] Building 12.3s (24/24) FINISHED
[+] Running 6/6
 ✔ Container 02-obi-docker-payment-service-1      Started
 ✔ Container 02-obi-docker-order-processor-1       Started
 ✔ Container 02-obi-docker-frontend-1              Started
 ✔ Container 02-obi-docker-splunk-otel-collector-1 Started
 ✔ Container 02-obi-docker-load-generator-1        Started
```

{{% /tab %}}
{{< /tabs >}}

これにより、ソースから3つのアプリケーションイメージがビルドされ、以下が起動します:

- **frontend**: [http://localhost:3000](http://localhost:3000)
- **order-processor**: ポート 8080
- **payment-service**: ポート 8081
- **splunk-otel-collector**: ポート 4317/4318 でテレメトリを受信
- **load-generator**: 2秒ごとに `/create-order` に自動リクエスト
