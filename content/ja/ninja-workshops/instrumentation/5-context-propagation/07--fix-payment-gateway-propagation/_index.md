---
title: Payment Gatewayのコンテキスト伝播を修正する
linkTitle: 7. Payment Gatewayのコンテキスト伝播を修正する
weight: 7
time: 15 minutes

---

このステップでは、payment gatewayプロキシの **アプリケーションコードを編集** し、W3C Trace Contextを`payment-api`に転送するようにしてから、サービスを **リビルドして再デプロイ** します。

{{% notice title="注意" style="info" %}}
エッジNGINXゲートウェイの修正（ステップ06）後、トレースはブラウザから`frontend-api`を経由して`order-api`まで接続される場合があります。しかし、 **frontend-api** が`payment-gateway`経由で支払いを送信する際、プロキシはW3Cトレースヘッダー **なしで** `payment-api`に転送します。

この断絶は一般的な **Node.jsプロキシのバグ** です。サービスは計装されておりAPMで確認できますが、送信側の`fetch`がトレースコンテキストを伝播しません。
{{% /notice %}}

Splunk APMでは以下の動作が確認できます

- `frontend-api` → `payment-gateway` - 接続済み
- `payment-gateway` → `payment-api` - **未接続**

![nginx-aft1](./images/07-index.png)

payment gatewayは独自の **Span** を生成するため（サービスマップには表示されます）、上流の呼び出しは`payment-api`で新しいトレースを開始します。これは、カスタムBFF/プロキシを追加して送信HTTPコールでのコンテキスト伝播を忘れた実際のチームや、「二重Span」を避けるために`suppressTracing()`を使用して誤って伝播を壊してしまうケースを再現しています。

## 修正方法

プロジェクトルート[~/workshop/context-propagation]から、server.jsファイルを開き **`buildUpstreamHeaders()`** を見つけます。

```
vi services/payment-gateway/server.js
```

#### W3Cトレースコンテキストを上流ヘッダーに注入する

1. returnの前に`propagation.inject()`のコメントを解除/追加します
2. 上流fetchの`suppressTracing`を削除します

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

{{% notice title="次に進む前に作業を確認してください" style="primary" icon="running" %}}
./workshop/context-propagationフォルダから以下のコマンドを実行して、変更内容を期待される解答と比較します

```bash
diff ./services/payment-gateway/server.js ./services/payment-gateway/server-fixed.js
```

{{% / notice %}}
