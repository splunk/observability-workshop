---
title: 1. A business signal
weight: 1
time: 6 minutes
---

The following handoff sets the scene for your investigation:

> **Finance:** We have flagged a gap between completed order value and collected payments. Please investigate the discrepancy and identify which orders are affected.
>
> **Operations:** We checked the same period. Checkout requests are completing without an increase in errors or latency.

A request can complete successfully while producing the wrong business outcome. Normal request-health signals are useful context, but they do not explain Finance's discrepancy.

Start with **checkout**, which coordinates the purchase. Look for completed-order records containing an order identifier, currency, full order value, and amount charged. These fields connect Finance's report to individual purchases.

You will investigate directly in **Logs**, using one base search and adding business fields as columns in the results table. This lets you examine each purchase and its charge together.

{{% notice title="Optional health check" style="info" %}}
Review the checkout service in **APM**, using the same environment and time window, to confirm the request-health assessment. Completing an APM investigation is not required for this module.

![Checkout service showing a 100% request success rate and latency for the same window used in the log investigation](../images/checkout-health.jpg "Successful requests establish technical health. Logs will explain the business outcome.")
{{% /notice %}}
