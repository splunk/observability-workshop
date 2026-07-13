---
title: SplunkでRUMを確認する
linkTitle: 4. SplunkでRUMを確認する
weight: 4
time: 10 minutes

---
このステップでは、RUMセッションがリクエストにコンテキストを追加する仕組みと、Splunk Observability Cloudでの表示を確認します。これはAPMの問題がRUMにどのように反映されるかを示す「問題状態」です。

## RUMリクエストパス

1. **<http://localhost:30080>** を開きます
2. ブラウザのDevToolsを開き、 **Network** タブを選択します
3. 異なる商品を3〜5件注文します
4. Networkタブで `POST /api/orders` リクエストを確認します
5. リクエストに `traceparent` ヘッダーが含まれていることを確認します（Splunk RUMによって注入されます）

ヘッダーの例:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

ブラウザは正しく計装されており、リクエストが期待どおりに処理されています。

{{% notice title="注意" style="green" icon="running" %}}
デプロイ後、RUMデータが表示されるまで **2〜5分** かかります。
{{% /notice %}}

## Splunk RUMで確認する

1. **Digital Experience → Session Search** に移動します
2. **Environment → `workshop-context-prop`** でフィルタリングします
3. 最新のセッションを開きます
4. `/api/orders` の `fetch` または `Click` リソースをクリックします
4. **Backend Trace** リンクを探します

![rum](../images/rumsesh-b4.png)

## チェックポイント

{{% notice title="注意" style="green" icon="running" %}}
RUMとAPMの両方が **Broken state（壊れた状態）** を示しています。

ゲートウェイが `traceparent` ヘッダーを `storefront-api` に到達する前に除去したため、RUMはバックエンドのAPM Traceにリンクできません。Splunk RUMは相関のために `Server-Timing` と一致するTrace IDに依存しています。

次のステップで、これらの問題を解決します。
{{% /notice %}}
