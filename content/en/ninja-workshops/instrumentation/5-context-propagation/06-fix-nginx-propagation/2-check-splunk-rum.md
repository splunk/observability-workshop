---
title: Explore RUM in Splunk
linkTitle: Explore RUM in Splunk
weight: 2
time: 5 minutes

---
In this step, you'll observe how RUM sessions appear add context to requests and how they appear in Splunk Observability Cloud. This is the "problem state" of how the APM issue reflects in RUM. 

## The RUM Request Path

{{% notice title="Note" style="green" icon="running" %}}
Allow **2–5 minutes** after deploy for RUM data to appear..
{{% /notice %}}

1. Open **http://localhost:30080**
2. Open browser DevTools → **Network** tab
3. Place an order
4. In the Network tab, inspect a `POST /api/orders` request
5. Confirm the request includes a `traceparent` header (injected by Splunk RUM)

Example header:

```
traceparent: 00-2476afefb1c010fa965d0e96d09c76c4-03d3d28b2b0f6290-01
```
![nginx-trcprnt](../images/traceparent-nginx.png)

{{% notice title="Note" style="green" icon="running" %}}
Copy the traceID value (highlighted in blue) - we will use this in the next step.
{{% /notice %}}

The browser appears to be correcly instrumented and processing requests as expected.

## Observe in Splunk RUM

1. Navigate to **Digital Experience → Session Search**
2. Filter **Environment → `workshop-context-prop`**
3. Open a recent session
4. Locate `fetch` requests
5. You will see an APM correlation link for 'api/catalog`. 
6. Hover over the hyperlink to view correlated trace details

![rumtrc](../images/nginx-rum-trc.png)
