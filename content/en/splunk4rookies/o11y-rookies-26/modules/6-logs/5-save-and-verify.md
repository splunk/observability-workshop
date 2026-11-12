---
title: 5. Save the search and verify results
weight: 5
time: 6 minutes
---

Save a search so you can return to this investigation and check new orders after a fix. In this workshop, there are no legitimate free orders, so a positive-value completed purchase with a zero charge warrants investigation.

{{% exercise title="Save the investigation" %}}

1. Retain your connection, index, environment, checkout service, and `order placed` event. Remove any order ID, trace ID, pod, or promo-code restriction used to inspect an individual case.
2. Open an affected order and select the `0` value for `app.order.amount.charged.usd`. Select **More (⋯)** → **Add to filter**, then run the search to narrow the results to zero-charge orders.
3. Inspect a matching order and confirm that `app.order.amount.usd` is positive. The saved search finds zero charges; a responder uses the event details to verify the order's full value.
4. Select **Save as** → **Save query**. Enter a unique name such as **`<your-name> — zero-charge orders`**.

Add a short description, review the query's scope, and leave public sharing off unless your instructor asks you to share it. Select **Save**, then find the query in **Saved Queries**. Reapply the intended investigation window when reopening it.

![Save Query form containing the zero-charge filter, checkout service, workshop environment, and log index](../images/save-zero-charge-query.jpg "Review the query name and scope before saving.")

{{% /exercise %}}

Filtering on zero charges keeps this search useful even if a different promotion causes the same problem. In a real application, account for approved free orders and other legitimate exceptions when interpreting the results.

{{% notice title="Optional: express the exact condition with SPL" style="info" %}}
If you are familiar with SPL, the following search expresses both amount conditions. Replace the index and environment with your workshop values. **Builder and SPL keep separate query state**, so enter the complete search when switching modes.

```spl
index="astronomy-shop" deployment.environment="rookies26-revleak-demo" service.name="checkout" "order placed"
| where 'app.order.amount.usd' > 0 AND 'app.order.amount.charged.usd' = 0
```

Use the same investigation window to compare these results with the orders you inspected.
{{% /notice %}}

Plan how to verify that new purchases are being charged correctly after the team corrects the pricing rule. Your instructor may demonstrate these checks during the workshop.


{{% notice style="blue" title="Investigation complete" icon="wine-bottle" %}}
You started with a reconciliation discrepancy and used **Logs** to explain it. You found completed-order events and added amount, discount, and promotion columns to the results. This let you compare affected and unaffected orders in the same table and identify the promotion behind the zero charges. You then saved the investigation for reuse and planned how to verify recovery.

Request-health signals and business outcomes answer different questions. Structured logs helped connect them in this investigation.
{{% /notice %}}

{{< pager next="/splunk4rookies/o11y-rookies-26/modules/" nextLabel="Back to Modules" >}}
