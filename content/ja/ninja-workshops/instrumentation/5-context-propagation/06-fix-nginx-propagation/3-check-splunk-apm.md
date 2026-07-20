---
title: Splunk APMで確認する
weight: 3
time: 5 minutes

---

このステップでは、以前切断されていたトレースがSplunk Observability Cloudでどのように表示されるかを確認します。これは「NGINXの修正後」の状態です。

```text
Browser (RUM span)
  → Frontend NGINX
    → Edge Gateway NGINX     ← Fix #1: trace headers Fixed
      → Order API
        → Catalog API        ← direct HTTP 
        → Payment Gateway    ← break #2: strips headers to payment-api
          → Payment API
            → RabbitMQ       ← break #3: no trace context in message
              → Fulfillment Worker  ← orphan root trace
```

## Splunkで確認する

1. **APM → Trace Analyzer** に移動します
4. 前のステップでtraceparentからコピーした **traceID** の値を貼り付けます
5. 'api/frontend-api' のAPMトレースが表示されます

#### 1. トレースの存在を確認する

**APM → Trace Analyzer** ビューで、上記のtraceparentからコピーしたtraceIDの値を貼り付けます。

![nginx-trcsrch](../images/nginx-trace-srch.png)

#### 2. トレースの部分的な相関を確認する

この修正後、フロントエンドのSpanはブラウザ/RUMセッションとトレースIDを共有するようになります。

![nginx-aft](../images/t-nginx-aft.png)

## チェックポイント

現在、他のサービスのAPM相関リンクは表示されていません。これは、ゲートウェイが `storefront-api` に到達する前に `traceparent` ヘッダーを除去したため、RUMがバックエンドのAPMトレースにリンクできないからです。Splunk RUMは `Server-Timing` と一致するトレースIDに依存して相関を行います。

次のステップでこれらの問題を解決します。
