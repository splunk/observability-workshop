---
title: 相関の検証
linkTitle: 9. 相関の検証
weight: 9
time: 10 minutes
 
---
この最後のステップでは、ブラウザのクリックからNGINXゲートウェイ、APIサービス、RabbitMQ、バックグラウンドワーカーまで、トレースが途切れなく流れていることを確認します。すべてがSplunk Observability Cloudで単一のトレースとして表示されます。

## エンドツーエンドの検証

### 新しいWebリクエストの送信

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"mount-eq6-pro","quantity":1,"customerEmail":"final-test@cosmic.shop"}' \
  | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="期待される出力" %}}

```json
{
    "message": "Order accepted for fulfillment",
    "order": {
        "orderId": "ORD-1719763200456",
        "productName": "SkyWatcher EQ6-R Pro Mount",
        "total": 1899.0
    },
    "traceHint": {
        "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
        "spanId": "..."
    }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="タスク" style="info" %}}
トレースID（32文字の16進数）をコピーします。Splunk APMでの検索に使用します。
{{% /notice %}}

{{< tabs >}}
{{% tab title="スクリプト" %}}
{{% notice title="注意" style="info" %}}
fulfilment-apiを検証するために2秒待ちます
{{% /notice %}}

```bash
kubectl -n cosmic-shop logs deployment/order-worker --tail=3
```

{{% /tab %}}
{{% tab title="期待される出力" %}}

```
Fulfilled order ORD-1719763200456 for SkyWatcher EQ6-R Pro Mount
```

{{% /tab %}}
{{< /tabs >}}

## Splunk RUMでの検証

1. **Digital Experience → Sessions** に移動します
2. セッションを見つけます（環境 `workshop-context-prop`）
3. セッションタイムラインをクリックします
4. `POST /api/orders` フェッチイベントを選択します
5. 以下を確認します
   - レスポンスタイムが表示されている
   - **Backend Trace** リンクがAPMに遷移する
   - トレースIDがブラウザの `traceparent` ヘッダーと一致している

### ToDO: Update Image

![trace-b4](./images/trace-b4.png)

## Splunk APMでの検証

1. **APM → Traces** に移動します
2. フィルター条件
   - Environment: `workshop-context-prop`
   - Minimum duration: any
3. RUMからリンクされたトレースを開きます（または `traceparent` ヘッダーのトレースIDで検索します）

### 期待されるSpan階層

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736  (example)

├─ documentLoad / routeChange               [RUM]
├─ HTTP GET /api/catalog                    [RUM → storefront-api]
│   └─ GET /api/catalog                     [storefront-api]
│       └─ catalog.list_products            [catalog-api]
└─ HTTP POST /api/orders                    [RUM → storefront-api]
    └─ POST /api/orders                     [storefront-api]
        ├─ catalog.get_product              [catalog-api]
        ├─ storefront.publish_order         [storefront-api, PRODUCER]
        │   └─ order-worker.process_order   [order-worker, CONSUMER]
        │       ├─ validate_inventory
        │       ├─ prepare_shipment
        │       └─ send_confirmation
        └─ (response 202)
```

### TODO UPDATE Image

![trace-aft1](./images/trace-aft.png)

## Service Mapの検証

1. **APM → Service Map** に移動します
2. 環境をフィルタリングします: `workshop-context-prop`
3. すべてのサービスがトラフィックエッジ付きで表示されていることを確認します
   - `storefront-api` → `catalog-api`
   - `storefront-api` → `order-worker`（RabbitMQ経由）

### TODO: UPDATE Image

![servicemap-aft1](./images/servicemap-aft.png)
