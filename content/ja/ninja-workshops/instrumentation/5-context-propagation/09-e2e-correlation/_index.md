---
title: E2E Correlation
linkTitle: E2E Correlation
weight: 9
time: 10 minutes
 
---
この最後のステップでは、ブラウザのクリックからNGINXゲートウェイ、APIサービス、RabbitMQ、バックグラウンドワーカーまで、トレースが途切れなく流れていることを確認します。すべてがSplunk Observability Cloudで単一のトレースとして表示されます。

## エンドツーエンドの検証

### 新しいWebリクエストの送信

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"mount-eq6-pro","quantity":1,"customerEmail":"final-test@cosmic.shop"}' \
  | python3 -m json.tool
```

{{% /tab %}}
{{% tab title="Expected Output" %}}

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
トレースID（32文字の16進数セグメント）をコピーします。Splunk APMでの検索に使用します。
{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}
{{% notice title="注意" style="info" %}}
フルフィルメントワーカーがRabbitMQメッセージを処理するまで2秒待ちます。
{{% /notice %}}

```bash
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{% tab title="Expected Output" %}}

```
Fulfilled order ORD-1719763200456 (payment PAY-1719763200456) for SkyWatcher EQ6-R Pro Mount
```

{{% /tab %}}
{{< /tabs >}}
