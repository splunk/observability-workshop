---
title: Follow the breadcrumbs
linkTitle:  2. Find cause
weight: 2
archetype: chapter
time: 7 minutes
description: 
---

{{% exercise title="Investigate with RUM" %}}

In a user session with the order confirmation error message, click {{% button %}}Troubleshoot in RUM{{% /button %}} in the top right of the replay. You should land on the long **PlaceOrder** custom event in the RUM user session details.

![RUM session waterfall with PlaceOrder and APM link](../images/rum-waterfall-place-order.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. What is a likely cause of the Order Confirmation issue? How can you tell?
1. If you wanted to investigate this issue further, what would you do?

{{% /tab %}}
{{% tab title="Answers" %}}

1. The nearby POST request to the backend API is quite long, and throws a 500 error.
1. Because we've instrumented this app with both RUM and APM, we get related content between relevant requests. Hovering over the APM link on the long POST request, we see a likely root cause issue flagged on the payment service. So from here we could open the Place Order business operation in APM to see how widespread this issue is, and we can open the specific trace to see span details and any related logs.

{{% /tab %}}
{{< /tabs >}}

Walkthrough:
1. Hover over the `APM` link on the long POST request. After a moment, the popup shows related backend services and which are in an error state.
1. *(Optional)* Open the `PlaceOrder` Business Operation link in a new tab to view the **APM Service Map** and see how checkout connects to downstream services (for example, **payment** service).
1. *(Optional)* Open the **Trace ID** link in a new tab to see this specific trace, its spans, tag details, and any relevant logs.

![Related content from APM within RUM](../images/apm-hover.png)

{{% notice title="RUM + APM" style="primary" icon="lightbulb" %}}Tracing from the browser through backend services cuts time spent chasing the wrong service and lowers MTTx.{{% /notice %}}

{{% /exercise %}}
