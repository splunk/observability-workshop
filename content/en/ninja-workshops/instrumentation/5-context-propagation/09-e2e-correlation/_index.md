---
title: E2E Correlation
linkTitle: E2E Correlation
weight: 9
time: 10 minutes
 
---
In this final step, you'll confirm that traces flow continuously from browser click through the NGINX gateway, API services, RabbitMQ, and the background worker - all visible as a single trace in Splunk Observability Cloud.

## End-to-End Validation

### Send New Web Request

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

{{% notice title="Task" style="info" %}}
Copy the trace ID (the 32-character hex segment) - you'll use it to search in Splunk APM.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Script" %}}
{{% notice title="Note" style="info" %}}
Wait 2 seconds for the fulfillment worker to process the RabbitMQ message.
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
