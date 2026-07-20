---
title: RabbitMQ Propagationの修正
linkTitle: 8. RabbitMQ Propagationの修正
weight: 8
time: 15 minutes 

---

このステップでは、メッセージの **producer** と **consumer** の**アプリケーションコードを編集**し、W3C Trace ContextがRabbitMQ AMQPヘッダーを通じて伝播されるようにします。

{{% notice title="注意" style="info" %}}
RabbitMQにはブローカーレベルのトレース設定がありません。伝播は常にアプリケーションコードで実装されます。

`payment-api`から `fulfillment-worker` への**非同期ハンドオフ**には、AMQPメッセージヘッダーでの**手動コンテキストインジェクションとエクストラクション**が必要です。

いずれかの側でこれを省略すると、消費される各メッセージは**新しいルートTrace**を開始します。これは本番環境で最もよく見られる非同期オブザーバビリティのギャップの1つです。
{{% /notice %}}

## 修正方法

### 1. Producer - (payment-api)

```
vi services/payment-api/server.js
```

**`buildFulfillmentMessageHeaders()`** を見つけ、戻り値を `injectTraceHeaders()` でラップします。

{{< tabs >}}
{{% tab title="修正前" %}}

```javascript
function buildFulfillmentMessageHeaders(order, payment) {
  return {
    'x-order-id': order.orderId,
    'x-payment-id': payment.paymentId,
  };
}
```

{{% /tab %}}
{{% tab title="修正後" %}}

```javascript
function buildFulfillmentMessageHeaders(order, payment) {
  return injectTraceHeaders({
    'x-order-id': order.orderId,
    'x-payment-id': payment.paymentId,
  });
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Consumer - (fulfillment-worker)

ファイルを開いて編集します。

```
vi services/fulfillment-worker/worker.js
```

ファイルの先頭にimportを追加します。

```javascript
import { extractTraceContext } from './shared/propagation.js';
```

**`extractMessageContext()`** スタブを共有エクストラクターに置き換えます。

{{< tabs >}}
{{% tab title="修正前" %}}

```javascript
// Remove this stub:
function extractMessageContext(_headers) {
  return context.active(); // ignores AMQP headers
}
```

{{% /tab %}}
{{% tab title="修正後" %}}

```javascript
import { extractTraceContext } from './shared/propagation.js';

// Instead of ignoring AMQP headers, use the shared helper in processFulfillment instead:
const parentContext = extractTraceContext(msg.properties.headers ?? {});
```

{{% /tab %}}
{{< /tabs >}}
