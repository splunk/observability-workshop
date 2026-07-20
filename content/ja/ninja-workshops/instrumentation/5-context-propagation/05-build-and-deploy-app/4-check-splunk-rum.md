---
title: Splunk RUMの確認
linkTitle: 4. Splunk RUMの確認
weight: 4
time: 10 minutes

---
このステップでは、RUMセッションがリクエストにコンテキストを追加する仕組みと、Splunk Observability Cloudでの表示を確認します。これはAPMの問題がRUMにどのように反映されるかを示す「問題状態」です。

## RUMリクエストパス

1. **<http://localhost:30080>** を開きます
2. ブラウザのDevTools → **Network** タブを開きます
3. 異なる商品を3〜5回注文します
4. Networkタブで `POST /api/orders` リクエストを確認します
5. リクエストに `traceparent` ヘッダー（Splunk RUMによって挿入）が含まれていることを確認します

ヘッダーの例:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

ブラウザは正しく計装されており、リクエストが期待通りに処理されていることが確認できます。

{{% notice title="注意" style="green" icon="running" %}}
デプロイ後、RUMデータが表示されるまで **2〜5分** かかる場合があります。
{{% /notice %}}

## Splunk RUMでの確認

1. **Digital Experience → Session Search** に移動します
2. **Environment → `workshop-context-prop`** でフィルタリングします
3. 最近のセッションを開きます
4. `fetch` リクエストを確認します
5. `api/catalog` に対するAPM相関リンクのみが表示されます

![rum](../images/rumsesh-b4.png)

{{% notice title="注意" style="green" icon="running" %}}
catalogのパスはエッジゲートウェイを経由しません。catalog-apiはfrontend-apiから直接呼び出されます。

   Browser → frontend NGINX → frontend-api → catalog-api

そのため、他の箇所でプロパゲーションが途切れていても、SplunkはGET /api/catalogのfetchをServer-Timingとcatalog呼び出しを含むfrontend-apiのTraceを通じてバックエンドAPMと相関させることができます。
{{% /notice %}}

## チェックポイント

RUMとAPMの両方が **問題のある状態** を示しています。

現在、他のサービスに対するAPM相関リンクが表示されていません。これは、ゲートウェイが `traceparent` ヘッダーを `storefront-api` に到達する前に削除してしまうため、RUMがバックエンドのAPM Traceにリンクできないためです。Splunk RUMは相関のために `Server-Timing` と一致するTrace IDに依存しています。

次のステップでこれらの問題を解決します。
