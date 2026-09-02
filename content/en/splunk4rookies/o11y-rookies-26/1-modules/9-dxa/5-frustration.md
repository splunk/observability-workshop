---
title: 5. Frustration Signals
weight: 5
time: 10 minutes
---

Not every user interaction is intentional or successful. DXA tracks **frustration signals** — behavioral indicators that suggest users are hitting friction — so teams can fix problems before they drive churn or support tickets.

Common frustration signals include **rage clicks** (rapid repeated clicks), **dead clicks** (clicks on non-interactive elements), and **errors** during a session.

{{% exercise title="Monitor friction" %}}

1. Return to the project **Analyses** tab and open the **`Frustration`** time series.
2. Explore the chart, data table, and linked session replays.

![Time series chart showing rage clicks, errors, and dead clicks over time in the Astronomy Shop](../images/frustration-timeseries.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. What does this chart tell us?
1. Can you identify why users are expressing frustration?

{{% /tab %}}
{{% tab title="Answers" %}}

1. The chart tracks frustration signal types over time — rage clicks, errors, and dead clicks. Workshop sessions show multiple users hitting points of friction.
1. Look for sessions involving the **Show All Reviews** button. Users click it expecting reviews to expand, nothing happens, and they rage click. This is a classic dead-click pattern.

<!-- TODO screenshot: Session replay showing rage clicks on the non-responsive Show All Reviews button -->

![Session replay showing a user rage clicking the non-responsive Show All Reviews button](../images/frustration-replay.png)

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

{{% notice title="Business impact" style="info" %}}
Frustration signals correlate with customer satisfaction, support volume, and churn. Monitoring them over time lets you measure whether UX fixes actually reduce friction — a direct line to NPS and retention KPIs.
{{% /notice %}}

Individual frustration events explain *where* users struggle. **Conversion funnels** reveal whether those struggles block users from completing critical journeys like checkout.
