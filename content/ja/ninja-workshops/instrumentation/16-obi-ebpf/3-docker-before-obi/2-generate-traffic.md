---
title: 2. トラフィックの生成
weight: 2
---

## フロントエンドへのアクセス

{{% notice title="演習" style="green" icon="running" %}}

curl を使ってトラフィックを生成します。

``` bash
curl -s http://localhost:3000/create-order | jq
```

{{% /notice %}}

次のような JSON レスポンスが返ってくるはずです。

``` json
{
  "order": "confirmed",
  "payment": {
    "status": "success",
    "transaction_id": "txn-a1b2c3d4e5f6",
    "amount": 42
  }
}
```

リクエストは 3 つのサービスすべてを経由しました。しかし、現時点では誰もそれを観測していません。

## コードを確認する

少し時間を取ってソースコードを調査し、計装が一切行われていないことを確認しましょう。

{{% notice title="演習" style="green" icon="running" %}}

``` bash
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/frontend/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/order-processor/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/payment-service/
```

{{% /notice %}}

3 つのコマンドはいずれも何も返しません。アプリケーションコードのどこにも、**トレーシングヘッダーも、SDK も、計装も一切存在しません**。
