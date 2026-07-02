---
title: Verify Correlation
linkTitle: 9. Verify Correlation
weight: 9
time: 10 minutes
description: In this final step, you'll confirm that traces flow continuously from browser click through the NGINX gateway, API services, RabbitMQ, and the background worker — all visible as a single trace in Splunk Observability Cloud.
 
---

## End-to-end validation

### Command-line

```bash
curl -s -X POST http://localhost:30080/api/purchases \
  -H "Content-Type: application/json" \
  -d '{"productId":"mount-eq6-pro","quantity":1,"customerEmail":"final-test@cosmic.shop"}' \
  | python3 -m json.tool
```

**Expected output:**

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

Copy the trace ID (the 32-character hex segment) - you'll use it to search in Splunk APM.

Wait ~2 seconds, then confirm worker fulfillment:

```bash
kubectl -n cosmic-shop logs deployment/order-worker --tail=3
```

**Expected log:**

```
Fulfilled order ORD-1719763200456 for SkyWatcher EQ6-R Pro Mount
```

---

## Verify in Splunk RUM

1. Navigate to **Digital Experience → Sessions**
2. Find your session (environment `workshop-context-prop`)
3. Click the session timeline
4. Select the `POST /api/orders` fetch event
5. Confirm:
   - Response time is displayed
   - **Backend Trace** link navigates to APM
   - Trace ID matches the browser `traceparent` header

### To Update
![trace-b4](./images/trace-b4.png)

---

## Verify in Splunk APM

1. Navigate to **APM → Traces**
2. Filter:
   - Environment: `workshop-context-prop`
   - Minimum duration: any
3. Open the trace linked from RUM (or search by trace ID from the `traceparent` header)

### Validation criteria (fully fixed state)

| Check | Pass criteria |
|-------|---------------|
| Single trace ID across all services | RUM, storefront-api, catalog-api, order-worker spans share one ID |
| order-worker parent span | Child of `storefront.publish_order` |
| Span count per order | ≥ 8 spans (HTTP + messaging + fulfillment steps) |
| No orphan root spans | Zero standalone `order-worker` traces for new orders |

### Expected span hierarchy

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736  (example)

├─ documentLoad / routeChange          [RUM]
├─ HTTP GET /api/catalog               [RUM → storefront-api]
│   └─ GET /api/catalog                [storefront-api]
│       └─ catalog.list_products       [catalog-api]
└─ HTTP POST /api/orders               [RUM → storefront-api]
    └─ POST /api/orders                [storefront-api]
        ├─ catalog.get_product         [catalog-api]
        ├─ storefront.publish_order      [storefront-api, PRODUCER]
        │   └─ order-worker.process_order  [order-worker, CONSUMER]
        │       ├─ validate_inventory
        │       ├─ prepare_shipment
        │       └─ send_confirmation
        └─ (response 202)
```
### To Update
![trace-b4](./images/trace-b4.png)

---

## Verify service map

1. Navigate to **APM → Service Map**
2. Filter environment: `workshop-context-prop`
3. Confirm all services appear with traffic edges:
   - `storefront-api` → `catalog-api`
   - `storefront-api` → `order-worker` (via RabbitMQ)

### To Update
![trace-b4](./images/trace-b4.png)

---
