---
title: Fix RabbitMQ Propagation
linkTitle: 8. Fix RabbitMQ Propagation
weight: 8
time: 15 minutes 

---

In this step, you'll **edit application code** in the message **producer** and **consumer** so W3C Trace Context flows through RabbitMQ AMQP headers.

{{% notice title="Note" style="info" %}}
RabbitMQ has no broker-level trace setting - propagation is always implemented in application code. 


The **async handoff** from `payment-api` to `fulfillment-worker` requires **manual context injection and extraction** in AMQP message headers:

When either side omits this, each consumed message starts a **new root trace** - one of the most common async observability gaps in production.
{{% /notice %}}

## The Fix

### 1. Producer - (payment-api)

```
vi services/payment-api/server.js
```

Locate **`buildFulfillmentMessageHeaders()`** and wrap the return value with `injectTraceHeaders()`:

{{< tabs >}}
{{% tab title="Before" %}}

```javascript
function buildFulfillmentMessageHeaders(order, payment) {
  return {
    'x-order-id': order.orderId,
    'x-payment-id': payment.paymentId,
  };
}
```

{{% /tab %}}
{{% tab title="After" %}}

```javascript
function buildFulfillmentMessageHeaders(order, payment) {
  return injectTraceHeaders({
    'x-order-id': order.orderId,
    'x-payment-id': payment.paymentId,
  });
}
```
{{% /tab %}}
{{< /tabs >}}

### 2. Consumer - (fulfillment-worker)

Open file to edit:

```
vi services/fulfillment-worker/worker.js
```

Add the import at the top:

```javascript
import { extractTraceContext } from './shared/propagation.js';
```

Replace the **`extractMessageContext()`** stub with the shared extractor.

{{< tabs >}}
{{% tab title="Before" %}}

```javascript
// Remove this stub:
function extractMessageContext(_headers) {
  return context.active(); // ignores AMQP headers
}
```

{{% /tab %}}
{{% tab title="After" %}}

```javascript
import { extractTraceContext } from './shared/propagation.js';

// Instead of ignoring AMQP headers, use the shared helper in processFulfillment instead:
const parentContext = extractTraceContext(msg.properties.headers ?? {});
```

{{% /tab %}}
{{< /tabs >}}
