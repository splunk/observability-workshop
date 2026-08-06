---
title: 8. Wrap-Up
weight: 8
time: 5 minutes
---

## What you accomplished

In this module, you moved from raw browsing sessions to actionable product insights — all without writing code or changing the Astronomy Shop application:

1. **Generated real user sessions** in the Astronomy Shop
2. **Navigated DXA** and understood its relationship to RUM
3. **Explored event definitions** that name and filter user actions
4. **Analyzed feature adoption** with time series and session replay
5. **Monitored frustration signals** like rage clicks and dead clicks
6. **Investigated conversion funnels** and checkout drop-off
7. **Compared user segments** to uncover targeted improvement opportunities

## The DXA workflow

```text
RUM session data → Event definitions → Analyses → Session replay → Action
```

DXA turns observability data into product intelligence. Event definitions are reusable; analyses are configurable in the UI; session replay closes the loop from metric to root cause.

## Connecting signals to business KPIs

| DXA signal | Business KPI |
|------------|----------------|
| Funnel drop-off at checkout | Conversion rate / revenue |
| Frustration (rage clicks, dead clicks) | Customer satisfaction / NPS |
| Feature adoption time series | Feature ROI / product engagement |

## What's next

- **Journey maps** — visualize common user paths and friction points across the full application. See [Analyses in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics).
- **Create your own analyses** — build funnels and time series for journeys and features that matter to your team.
- **Define custom events** — use the element picker to track new interactions without engineering support.

For reference:

- [Introduction to Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/introduction-to-digital-experience-analytics)
- [Create and manage event definitions](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/create-and-manage-event-definitions)
- [Create user segments](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/create-user-segments)

{{% exercise title="Reflect" %}}

{{< tabs >}}
{{% tab title="Question" %}}
What is one DXA insight from this workshop that you would share with your product team on Monday morning?
{{% /tab %}}
{{% tab title="Answer" %}}
There is no single correct answer — strong responses connect a specific signal to a business outcome. For example: "Our checkout funnel shows a major drop-off between Place order and Order confirmation, and session replay confirms users see an error instead of a confirmation page. That is a direct conversion problem we should prioritize." Or: "Frustration signals spike on the Show All Reviews button — a dead click that erodes trust before users even reach checkout."
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

{{< pager prev="/en/splunk4rookies/o11y-rookies-26/1-modules/" prevLabel="Back to Lessons" >}}
