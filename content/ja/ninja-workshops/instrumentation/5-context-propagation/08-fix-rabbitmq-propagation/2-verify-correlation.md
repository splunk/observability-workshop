---
title: 相関の検証
weight: 2
time: 10 minutes
 
---
このステップでは、Splunk Observability Cloudでpayment gatewayからfulfilment-apiまでのTraceが単一のTraceとして連続的に流れることを確認します。

## 相関の検証

### テスト注文を行う

{{% notice title="検証" style="green" icon="running" %}}
再デプロイ後に **新しい** 注文を行ってください。修正前に発行されたメッセージにはTraceコンテキストが含まれていません。
{{% /notice %}}

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"filter-nebula-uhc","quantity":1,"customerEmail":"propagation-test@cosmic.shop"}' \
  | python3 -m json.tool

sleep 2
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{% tab title="出力例" %}}

```json
{
    "message": "Purchase complete — order placed and payment submitted for fulfillment",
    "order": {
        "orderId": "ORD-1783658853932",
        "productId": "filter-nebula-uhc",
        "productName": "UHC Nebula Filter 1.25\"",
        "quantity": 1,
        "total": 89.99,
        "customerEmail": "propagation-test@cosmic.shop",
        "createdAt": "2026-07-10T04:47:33.932Z",
        "requestTraceId": "2481d53cc6e0b317ec92b41d32b9cc31"
    },
    "payment": {
        "paymentId": "PAY-1783658853945",
        "orderId": "ORD-1783658853932",
        "amount": 89.99,
        "status": "authorized",
        "method": "stellar-credits",
        "processedAt": "2026-07-10T04:47:33.945Z"
    }
}
Fulfilled order ORD-1783658559948 (payment PAY-1783658559954) for Cosmic Cliffs Observing Atlas
Fulfilled order ORD-1783658562526 (payment PAY-1783658562531) for ZWO ASI533MC Pro Camera
Fulfilled order ORD-1783658853932 (payment PAY-1783658853945) for UHC Nebula Filter 1.25"
```

{{% /tab %}}
{{< /tabs >}}

### Splunk APMで検証する

1. **APM → Trace Analyzer** に移動します
2. フィルター条件を設定します
   - Environment: `workshop-context-prop`
   - Services: `payment-api`
3. `payment-api: POST POST` で開始されるTraceを選択します

paymentサービスとfulfilmentサービスの相関が表示されます。

![rabbitmq-fix](../images/8-pmt-fulfil.png)
