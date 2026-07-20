---
title: Payment Gatewayのコンテキスト伝播を修正する
linkTitle: 7. Payment Gatewayのコンテキスト伝播を修正する
weight: 7
time: 15 minutes

---

このステップでは、payment gatewayプロキシの **アプリケーションコードを編集** して、W3C Trace Contextを `payment-api` に転送し、サービスを **リビルドして再デプロイ** します。

{{% notice title="注意" style="info" %}}
エッジNGINXゲートウェイの修正（ステップ06）後、ブラウザから `frontend-api` を経由して `order-api` までトレースが接続される場合があります。しかし、**frontend-api** が `payment-gateway` 経由で支払いを送信する際、プロキシはW3C traceヘッダー **なし** で `payment-api` に転送します。

この断絶は一般的な **Node.jsプロキシのバグ** です。サービスは計装されておりAPMで表示されますが、送信側の `fetch` がトレースコンテキストを伝播しません。
{{% /notice %}}

Splunk APMでは次の動作が確認できます。

- `frontend-api` → `payment-gateway` - 接続済み
- `payment-gateway` → `payment-api` - **切断**

![nginx-aft1](./images/07-index.png)

payment gatewayは独自の **Span** を生成するため（サービスマップには表示されます）、上流の呼び出しは `payment-api` で新しいトレースを開始します。これは、カスタムBFF/プロキシを追加して送信HTTPコールでコンテキストの伝播を忘れる実際のチームの状況を反映しています。また、「二重Span」を避けようとして `suppressTracing()` を使用し、誤って伝播を壊してしまうケースも同様です。

## 修正

server.jsファイルを開き、**`buildUpstreamHeaders()`** を探します。

```
vi services/payment-gateway/server.js
```

#### W3C traceコンテキストを上流ヘッダーに注入する

1. returnの前に `propagation.inject()` のコメントを解除/追加します
2. 上流のfetchから `suppressTracing` を削除します

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
