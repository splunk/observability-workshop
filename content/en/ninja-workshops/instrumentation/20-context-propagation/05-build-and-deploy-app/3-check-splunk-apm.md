---
title: 3. Explore APM in Splunk
linkTitle: 3. Explore APM in Splunk
weight: 3
time: 10 minutes
description: In this step, you'll observe how disconnected traces appear in Splunk Observability Cloud. This is the "problem state" that the rest of the workshop fixes. 

---

## The APM request path

When you clicked **Place order**, the request flowed through:

```
Browser (RUM span)
  → Frontend NGINX
    → Edge Gateway NGINX     ← break #1: trace headers dropped
      → Order API
        → Catalog API        ← direct HTTP (may share order-api trace)
        → Payment Gateway    ← break #2: strips headers to payment-api (visible in service map)
          → Payment API
            → RabbitMQ       ← break #3: no trace context in message
              → Fulfillment Worker  ← orphan root trace
```

Three breaks occur:

1. **HTTP break #1** at the edge NGINX gateway (browser → order API)
2. **HTTP break #2** at the payment-gateway proxy (order API → payment API)
3. **Messaging break** at RabbitMQ (payment API → fulfillment worker)

---

## Observe in Splunk APM

{{% notice title="Note" style="green" icon="running" %}}
Allow **2–5 minutes** after generating data for metrics to appear..
{{% /notice %}}

### Service map

1. Navigate to **APM → Service Map**
2. Filter environment: `workshop-context-prop`
3. You should see services: `order-api`, `payment-gateway`, `payment-api`, `fulfillment-worker`, `catalog-api`

![servicemap](./images/servicemap-b4.png)

### Trace search

1. Navigate to **APM → Trace Analyzer**
2. Filter:
   - Environment: `workshop-context-prop`
   - Service: `order-api`
   - Operation: `POST /api/orders` (or `storefront.place_order`)
3. Open a recent trace

**What you'll see (broken state):**

![trace-b4](./images/trace-b4.png)

---

## Knowledge Check

### Why NGINX breaks propagation

{{< details summary="Click here to see the answer" >}}
Our gateway uses a common production NGINX pattern:

```nginx
location /api/ {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://storefront_api;
}
```

``` text
When **any** `proxy_set_header` directive is present, NGINX stops automatically forwarding client headers to the upstream. Headers like `traceparent`, `tracestate`, and `baggage` are silently dropped unless explicitly configured.

This is one of the most common causes of broken trace correlation in production.
```
{{< /details >}}
---

### Why RabbitMQ breaks propagation

{{< details summary="Click here to see the answer" >}}
Our storefront publishes orders like this (broken state):

```javascript
channel.sendToQueue(ordersQueue, Buffer.from(JSON.stringify(order)), {
  persistent: true,
  headers: { 'x-order-id': order.orderId },  // no traceparent
});
```
``` text
Unlike HTTP, message brokers don't participate in W3C Trace Context automatically. The producer must **inject** trace context into message headers, and the consumer must **extract** it. Without this, the consumer starts a new root trace.
```
{{% /notice %}}

---
