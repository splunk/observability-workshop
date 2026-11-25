---
title: 5. Frustration Signals
weight: 5
---

Not every user interaction is intentional or successful. DXA tracks **frustration signals** — behavioral indicators that suggest users are hitting friction — so teams can fix problems before they drive churn or support tickets.

Common frustration signals include **rage clicks** (rapid repeated clicks), **dead clicks** (clicks on non-interactive elements), and **errors** during a session.

{{% exercise title="Monitor friction" %}}

1. Return to the project **Analyses** tab and open the **`Frustration`** time series.
2. Explore the chart, data table, and linked session replays.

![Time series chart showing rage clicks, errors, and dead clicks over time in the Astronomy Shop](../images/frustration-timeseries.webp)

Look at the chart. It tracks each type of frustration signal over time: rage clicks, errors and dead clicks. Workshop sessions show multiple users hitting points of friction. Open some of the linked session replays to see what users were doing.

{{< quiz question="Which part of the Astronomy Shop is causing users to express frustration?" >}}
{{< quiz-option >}}The Ask AI text input on the product page.{{< /quiz-option >}}
{{< quiz-option >}}The Add To Cart button.{{< /quiz-option >}}
{{< quiz-option correct=true >}}The Show All Reviews button.{{< /quiz-option >}}
{{< quiz-option >}}The currency selector.{{< /quiz-option >}}
{{< quiz-feedback >}}
Users click **Show All Reviews** expecting the reviews to expand, but nothing happens, so they click it again and again. Clicking an element that does not respond is a classic **dead-click** pattern, and repeated clicking turns it into a **rage click**.

![Session replay showing a user rage clicking the non-responsive Show All Reviews button](../images/frustration-replay.webp)
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Business impact" style="info" %}}
Frustration signals correlate with customer satisfaction, support volume, and churn. Monitoring them over time lets us measure whether UX fixes actually reduce friction — a direct line to NPS and retention KPIs.
{{% /notice %}}

Individual frustration events explain *where* users struggle. **Conversion funnels** reveal whether those struggles block users from completing critical journeys like checkout.
