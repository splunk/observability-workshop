---
title: 4. Explore RUM in Splunk
linkTitle: 4. Explore RUM in Splunk
weight: 4
time: 10 minutes
description: In this step, you'll observe how RUM sessions appear add context to requests and how they appear in Splunk Observability Cloud. This is the "problem state" of how the APM issue reflects in RUM. 

---

## The RUM request path

1. Open **http://localhost:30080**
2. Open browser DevTools → **Network** tab
3. Place 3–5 orders for different products
4. In the Network tab, inspect a `POST /api/orders` request
5. Confirm the request includes a `traceparent` header (injected by Splunk RUM)

Example header:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

The browser appears to be correcly instrumented and processing requests as expected.

---

{{% notice title="Note" style="green" icon="running" %}}
Allow **2–5 minutes** after deploy for RUM data to appear..
{{% /notice %}}

## Observe in Splunk RUM

1. Navigate to **Digital Experience → Session Search**
2. Filter **Environment → `workshop-context-prop`**
3. Open a recent session
4. Click on a `fetch` or `Click`resource for `/api/orders`
4. Look for the **Backend Trace** link

![rum](./images/rumsesh-b4.png)

---

# Check-Point

{{% notice title="Note" style="green" icon="running" %}}
Both RUM and APM show a **Broken state:** 

RUM cannot link to the backend APM trace because the gateway stripped the `traceparent` header before it reached `storefront-api`. Splunk RUM relies on `Server-Timing` and matching trace IDs for correlation.

In the next steps, we will resolve these issues.
{{% /notice %}}

---
