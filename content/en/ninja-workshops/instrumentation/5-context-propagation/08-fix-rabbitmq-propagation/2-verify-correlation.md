---
title: Verify Correlation
weight: 2
time: 10 minutes
 
---
In this step, you'll confirm that traces flow continuously from payment gateway to fulfilment-api as a single trace in Splunk Observability Cloud.

## Correlation Validation

### Place a Test Order

{{% notice title="Validation" style="green" icon="running" %}}
Place **new** orders after redeploy - messages published before the fix will not carry trace context.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"filter-nebula-uhc","quantity":1,"customerEmail":"propagation-test@cosmic.shop"}' \
  | python3 -m json.tool

sleep 2
kubectl -n cosmic-shop logs deployment/fulfillment-worker --tail=3
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
    "message": "Purchase complete \u2014 order placed and payment submitted for fulfillment",
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

### Verify in Splunk APM

1. Navigate to **APM → Trace Analyzer**
2. Filter:
   - Environment: `workshop-context-prop`
   - Services: `payment-api`
3. Select a trace with `payment-api: POST POST` initiating operation

You will now see the correlation between the payment and the fulfilment services

![rabbitmq-fix](../images/8-pmt-fulfil.png)

