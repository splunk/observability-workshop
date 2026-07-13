---
title: Splunk APMで確認する
linkTitle: 3. Splunk APMで確認する
weight: 3
time: 10 minutes
 
---

このステップでは、Splunk Observability Cloudで切断されたトレースがどのように表示されるかを確認します。これはワークショップの残りの部分で修正する「問題のある状態」です。

## APMリクエストパス

**Place order** をクリックしたとき、リクエストは以下の経路を通ります。

```
Browser (RUM span)
  → Frontend NGINX
    → Edge Gateway NGINX     ← break #1: trace headers dropped
      → Order API
        → Catalog API        ← direct HTTP 
        → Payment Gateway    ← break #2: strips headers to payment-api
          → Payment API
            → RabbitMQ       ← break #3: no trace context in message
              → Fulfillment Worker  ← orphan root trace
```

3つの断絶が発生します。

1. **HTTP break #1** Edge NGINXゲートウェイ（browser → order API）
2. **HTTP break #2** payment-gatewayプロキシ（order API → payment API）
3. **Messaging break** RabbitMQ（payment API → fulfillment worker）

## Splunk APMで確認する

{{% notice title="注意" style="green" icon="running" %}}
データ生成後、メトリクスが表示されるまで **2〜5分** かかります。
{{% /notice %}}

### Service map

1. **APM → Service Map** に移動します
2. 環境をフィルタリングします: `workshop-context-prop`
3. 以下のサービスが表示されます: `order-api`, `payment-gateway`, `payment-api`, `fulfillment-worker`, `catalog-api`

![servicemap](../images/servicemap-b4.png)

### Trace search

1. **APM → Trace Analyzer** に移動します
2. フィルタを設定します:
   - Environment: `workshop-context-prop`
   - Service: `order-api`
   - Operation: `POST /api/orders`（または `storefront.place_order`）
3. 最近のトレースを開きます

**表示される内容（断絶状態）:**

![trace-b4](../images/trace-b4.png)

## 理解度チェック

#### NGINXがプロパゲーションを断絶する理由

{{< details summary="ここをクリックして回答を表示" >}}
ゲートウェイは本番環境で一般的なNGINXパターンを使用しています。

```nginx
location /api/ {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://storefront_api;
}
```

``` text
いずれかの `proxy_set_header` ディレクティブが存在すると、NGINXはクライアントヘッダーのアップストリームへの自動転送を停止します。`traceparent`、`tracestate`、`baggage` などのヘッダーは、明示的に設定しない限り暗黙的にドロップされます。

これは本番環境でトレースの相関が断絶する最も一般的な原因の1つです。
```

{{< /details >}}

#### RabbitMQがプロパゲーションを断絶する理由

{{< details summary="ここをクリックして回答を表示" >}}
ストアフロントは以下のように注文を発行しています（断絶状態）。

```javascript
channel.sendToQueue(ordersQueue, Buffer.from(JSON.stringify(order)), {
  persistent: true,
  headers: { 'x-order-id': order.orderId },  // no traceparent
});
```

``` text
HTTPとは異なり、メッセージブローカーはW3C Trace Contextに自動的に参加しません。プロデューサーはメッセージヘッダーにトレースコンテキストを注入（inject）し、コンシューマーはそれを抽出（extract）する必要があります。これがないと、コンシューマーは新しいルートトレースを開始します。
```

{{% /notice %}}
