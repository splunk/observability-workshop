---
title: SplunkでRUMを確認する
linkTitle: SplunkでRUMを確認する
weight: 2
time: 5 minutes

---
このステップでは、RUMセッションがリクエストにコンテキストを追加する仕組みと、Splunk Observability Cloudでどのように表示されるかを確認します。これはAPMの問題がRUMにどのように反映されるかを示す「問題状態」です。

## RUMリクエストパス

{{% notice title="注意" style="green" icon="running" %}}
デプロイ後、RUMデータが表示されるまで **2〜5分** お待ちください。
{{% /notice %}}

1. **<http://localhost:30080>** を開きます
2. ブラウザのDevTools → **Network** タブを開きます
3. 注文を行います
4. Networkタブで `POST /api/orders` リクエストを確認します
5. リクエストに `traceparent` ヘッダー（Splunk RUMによって注入）が含まれていることを確認します

ヘッダーの例

```
traceparent: 00-2476afefb1c010fa965d0e96d09c76c4-03d3d28b2b0f6290-01
```

![nginx-trcprnt](../images/traceparent-nginx.png)

{{% notice title="注意" style="green" icon="running" %}}
traceIDの値（青色でハイライト表示）をコピーしてください。次のステップで使用します。
{{% /notice %}}

ブラウザは正しく計装されており、リクエストが期待どおりに処理されていることが確認できます。

## Splunk RUMで確認する

1. **Digital Experience → Session Search** に移動します
2. **Environment → `workshop-context-prop`** でフィルタリングします
3. 最近のセッションを開きます
4. `fetch` リクエストを探します
5. `api/catalog` のAPM相関リンクが表示されます
6. ハイパーリンクにカーソルを合わせて、相関するTraceの詳細を確認します

![rumtrc](../images/nginx-rum-trc.png)
