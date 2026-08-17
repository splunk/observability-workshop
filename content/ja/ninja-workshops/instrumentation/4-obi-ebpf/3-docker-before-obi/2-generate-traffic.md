---
title: 2. トラフィックの生成
weight: 2
---

## フロントエンドへのアクセス

{{% notice title="演習" style="green" icon="running" %}}

curlを使用してトラフィックを生成します:

``` bash
curl -s http://localhost:3000/create-order | python3 -m json.tool
```

{{% /notice %}}

以下のようなJSONレスポンスが表示されます:

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

リクエストは3つのサービスすべてを通過しました。しかし、現時点では誰も監視していません。

## コードの確認

ソースコードを確認し、計装がまったく行われていないことを確認してください:

{{% notice title="演習" style="green" icon="running" %}}

``` bash
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/frontend/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/order-processor/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/payment-service/
```

{{% /notice %}}

3つのコマンドはすべて何も返しません。アプリケーションコードには**トレースヘッダー、SDK、計装が一切ありません**。
