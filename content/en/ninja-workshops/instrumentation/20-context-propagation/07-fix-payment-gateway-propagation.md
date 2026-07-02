---
title: Fix Payment Gateway Propagation
linkTitle: 7. Fix Payment Gateway Propagation
weight: 7
time: 15 minutes
description: In this step, you'll enable W3C Trace Context forwarding on the **payment-gateway** proxy so traces correlate from **frontend-api** through to the payment API. Unlike the edge NGINX gateway, `payment-gateway` is an **instrumented Node.js service** - it appears as its own node in the Splunk APM **Service Map**.

---

{{% notice title="Note" style="info" %}}
After fixing the edge NGINX gateway (step 06), traces now connect from the browser through `frontend-api` and into `order-api`. But when **frontend-api** submits payment via `payment-gateway`, the proxy forwards to `payment-api` **without** W3C trace headers.

In Splunk APM you'll see this behaviour:

- `frontend-api` → `payment-gateway` - connected 
- `payment-gateway` → `payment-api` - **disconnected** 
{{% /notice %}}
---

## The fix
