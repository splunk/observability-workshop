---
title: Payment Gatewayのプロパゲーション修正
linkTitle: 7. Payment Gatewayのプロパゲーション修正
weight: 7
time: 15 minutes

---

このステップでは、payment gatewayプロキシの **アプリケーションコードを編集** し、W3C Trace Contextを `payment-api` に転送するようにしてから、サービスを **リビルドして再デプロイ** します。

{{% notice title="注意" style="info" %}}
エッジNGINXゲートウェイを修正した後（ステップ06）、ブラウザから `frontend-api` を経由して `order-api` までトレースが接続される場合があります。しかし、 **frontend-api** が `payment-gateway` 経由で支払いを送信する際、プロキシはW3Cトレースヘッダー **なしで** `payment-api` に転送します。

この断絶は一般的な **Node.jsプロキシのバグ** です。サービスは計装されAPMに表示されますが、送信側の `fetch` がトレースコンテキストを伝播しません。
{{% /notice %}}

Splunk APMでは次の動作が確認できます。

- `frontend-api` → `payment-gateway` - 接続済み
- `payment-gateway` → `payment-api` - **切断**

![nginx-aft1](./images/07-index.png)

payment gatewayは独自の **Span** を生成するため（サービスマップに表示されます）、上流の呼び出しは `payment-api` で新しいトレースを開始します。これは、カスタムBFF/プロキシを追加して送信HTTPコールでのコンテキスト伝播を忘れた実際のチームや、「二重Span」を避けようとして `suppressTracing()` を使用し、誤ってプロパゲーションを壊してしまうケースを再現しています。

## 修正方法

server.jsファイルを開き、 **`buildUpstreamHeaders()`** を見つけます。

```
vi services/payment-gateway/server.js
```

### 1. W3Cトレースコンテキストを上流ヘッダーに注入する

returnの前に `propagation.inject()` のコメントを解除/追加します。

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  propagation.inject(context.active(), headers, {
    set: (carrier, key, value) => {
      carrier[key] = value;
    },
  });

  return headers;
}
```

### 2. 上流fetchから `suppressTracing` を削除する

`POST /payments` 内の上流呼び出しを見つけます。

```javascript
// Before (broken):
const upstreamContext = suppressTracing(context.active());

// After (fixed):
const upstreamContext = context.active();
```

## 修正前と修正後

{{< tabs >}}
{{% tab title="修正前" %}}

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };
  return headers;
}

const upstreamContext = suppressTracing(context.active());
```

{{% /tab %}}
{{% tab title="修正後" %}}

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  propagation.inject(context.active(), headers, {
    set: (carrier, key, value) => {
      carrier[key] = value;
    },
  });

  return headers;
}

const upstreamContext = context.active();
```

{{% /tab %}}
{{< /tabs >}}
