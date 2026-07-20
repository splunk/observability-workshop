---
title: 2. トラフィックの生成
weight: 2
---

## フロントエンドにアクセスする

{{% notice title="演習" style="green" icon="running" %}}

curlを使用してトラフィックを生成します。

``` bash
curl -s http://localhost:3000/create-order | jq
```

{{% /notice %}}

以下のようなJSONレスポンスが表示されます。

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

リクエストは3つのサービスすべてを通過しました。しかし現時点では、誰も監視していません。

## コードを確認する

ソースコードを確認し、計装がまったく含まれていないことを確認します。

{{% notice title="演習" style="green" icon="running" %}}

``` bash
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/frontend/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/order-processor/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/payment-service/
```

{{% /notice %}}

3つのコマンドすべて何も返しません。アプリケーションコードには **トレーシングヘッダー、SDK、計装のいずれもゼロ** です。
