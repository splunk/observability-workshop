---
title: 1. スタックの構成と起動
weight: 1
---

## Splunk 認証情報の追加

{{% notice title="演習" style="green" icon="running" %}}

**注意:** ご自身の環境で `ACCESS_TOKEN`、`REALM`、`INSTANCE` を取得してください。これらを config に貼り付ける必要があります。

``` bash
echo $ACCESS_TOKEN; echo $REALM; echo $INSTANCE
```

Phase 1/2 ディレクトリに移動し、エディタで `docker-compose.yaml` を開きます。

``` bash
cd ~/workshop/obi/02-obi-docker
vim docker-compose.yaml #or editor of choice
```

`splunk-otel-collector` サービスを見つけ、4 つのプレースホルダー値を実際の認証情報に置き換えます。

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
**なぜ `WORKSHOP_HOST_NAME` と `WORKSHOP_ENVIRONMENT` が必要なのか？** ワークショップの参加者全員が同じ Splunk org にテレメトリを送信します。これらの値は、すべてのメトリクスとトレースに `host.name` および `deployment.environment` 属性として設定されるため、Splunk 上で**自分の**データだけをフィルタリングできます。
{{% /notice %}}

## スタックの起動

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker-compose up --build -d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

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

このコマンドが完了するまで数分かかります。3 つのアプリケーションイメージをソースからビルドし、以下を起動します。

- **frontend** が [http://localhost:3000](http://localhost:3000) で起動
- **order-processor** がポート 8080 で起動
- **payment-service** がポート 8081 で起動
- **splunk-otel-collector** がポート 4317/4318 でテレメトリを受信
- **load-generator** が 2 秒ごとに `/create-order` へ自動的にリクエストを送信
