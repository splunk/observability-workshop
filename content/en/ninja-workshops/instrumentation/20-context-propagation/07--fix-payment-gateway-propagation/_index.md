---
title: Fix Payment Gateway Propagation
linkTitle: 7. Fix Payment Gateway Propagation
weight: 7
time: 15 minutes
description: In this step, you'll **edit application code** in the payment gateway proxy so it forwards W3C Trace Context to `payment-api`, then **rebuild and redeploy** the service.

---

{{% notice title="Note" style="info" %}}
After fixing the edge NGINX gateway (step 06), traces may connect from the browser through `frontend-api` and into `order-api`. But when **frontend-api** submits payment via `payment-gateway`, the proxy forwards to `payment-api` **without** W3C trace headers.

This break is a common **Node.js proxy bug**: the service is instrumented and visible in APM, but the outbound `fetch` does not propagate trace context.

In Splunk APM you'll see this behaviour:

- `frontend-api` → `payment-gateway` - connected 
- `payment-gateway` → `payment-api` - **disconnected** 

The payment gateway still creates its **own spans** (so it shows in the service map), but the upstream call starts a new trace on `payment-api`. This mirrors real teams who add a custom BFF/proxy and forget to propagate context on outbound HTTP calls - or when code uses `suppressTracing()` trying to avoid "double spans" which accidentally breaks propagation.

{{% /notice %}}
---

## The fix

Open the server.js file and locate **`buildUpstreamHeaders()`**.

```
vi services/payment-gateway/server.js
```

### 1. Inject W3C trace context into upstream headers

Uncomment/add `propagation.inject()` before the return:

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  propagation.inject(context.active(), headers, {
    set: (carrier, key, value) => {
      carrier[key] = value;
    },
  });

  return headers;
}
```

### 2. Remove `suppressTracing` on the upstream fetch

Find the upstream call in `POST /payments`:

```javascript
// Before (broken):
const upstreamContext = suppressTracing(context.active());

// After (fixed):
const upstreamContext = context.active();
```

---

## Before and after

{{< tabs >}}
{{% tab title="Before" %}}

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };
  return headers;
}

const upstreamContext = suppressTracing(context.active());
```

{{% /tab %}}
{{% tab title="After" %}}

```javascript
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  propagation.inject(context.active(), headers, {
    set: (carrier, key, value) => {
      carrier[key] = value;
    },
  });

  return headers;
}

const upstreamContext = context.active();
```

{{% /tab %}}
{{< /tabs >}}

---
