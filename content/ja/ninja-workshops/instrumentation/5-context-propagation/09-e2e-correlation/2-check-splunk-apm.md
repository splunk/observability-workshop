---
title: Splunk APMで確認する
weight: 2
time: 5 minutes
 
---
このステップでは、Splunk Observability Cloudで完全なAPMエンドツーエンド相関がどのように表示されるかを確認します。

## Splunk APMで確認する

### Traceを確認する

1. RUMセッションから - RUMからリンクされたトレースを開きます
    または（UIの `traceparent` ヘッダーまたは完了した購入リクエストからトレースIDを貼り付けます）

前のステップのRUMセッションに移動するRUM相関ハイパーリンクが表示されます。

![trace-aft1](../images/s-trace-aft.png)

### Service Mapを確認する

1. **APM → Service Map** に移動します
2. 環境をフィルタリングします: `workshop-context-prop`
3. すべてのサービスがトラフィックエッジとともに表示されることを確認します
   - `frontend-api` → `catalog-api`
   - `frontend-api` → `order-api`（gateway経由）
   - `frontend-api` → `payment-gateway` → `payment-api`
   - `payment-api` → `fulfillment-worker`（RabbitMQ経由）

これにより、すべてのサービスおよびインフラストラクチャレイヤーにわたるエンドツーエンド相関が確認できます。

![servicemap-aft1](../images/servicemap-aft.png)
