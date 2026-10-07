---
title: 5. Frustration Signals
weight: 5
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

![Session replay showing a user rage clicking the non-responsive Show All Reviews button](../images/frustration-replay.png)

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

{{% notice title="Business impact" style="info" %}}
Frustration signals correlate with customer satisfaction, support volume, and churn. Monitoring them over time lets us measure whether UX fixes actually reduce friction — a direct line to NPS and retention KPIs.
{{% /notice %}}

{{< webex chat="Shelly K." date="Today • 28/02/2026" seenby="SK" >}}
{{< webex-msg from="SK" name="Shelly K." time="13:10" >}}
hey, Sheila from Support let me know that they're not getting as many complaints about the app, which is great! Any idea why?
{{< /webex-msg >}}

{{< webex-msg me=true time="13:19" >}}
we made some changes to the UI based on what we saw in session replay, and the release aligns with a drop in frustration signals!{{< /webex-msg >}}

{{< webex-msg from="SK" name="Shelly K." time="13:20" >}}
AWESOME!
{{< /webex-msg >}}
{{< /webex >}}

Individual frustration events explain *where* users struggle. **Conversion funnels** reveal whether those struggles block users from completing critical journeys like checkout.
