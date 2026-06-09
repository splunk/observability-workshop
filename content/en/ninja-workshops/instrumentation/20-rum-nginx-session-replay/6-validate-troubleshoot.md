---
title: 6. Build Segments and Analyses
linkTitle: 6. Analyze DXA
weight: 6
---

With event definitions in place, build the DXA views that help product, UX, and engineering teams reason about behavior together.

## Create user segments

Open **User Segments** and create one or more segments:

| Segment | Example criteria | Use |
| --- | --- | --- |
| `Checkout visitors` | Users with `Begin checkout` | Measure checkout outcomes. |
| `Abandoned checkout` | Users with `Begin checkout` and without `Order submitted` | Investigate drop-off. |
| `Error-affected users` | Users with `Checkout error` | Compare technical failures with conversion. |
| `Workshop environment` | Session or RUM attribute `deployment.environment = workshop` | Keep lab data separate from other environments. |

Segments let you compare the same analysis across different user populations without changing the underlying event definitions.

## Create a conversion funnel

Open **Analyses**, select **New analysis**, and choose **Conversion funnel**. Build this funnel:

1. `Product viewed`
2. `Add to cart`
3. `Begin checkout`
4. `Order submitted`

Filter to the `Workshop environment` segment or the `workshop` deployment environment. Preview the results and look for the largest drop-off.

When you find a drop-off point, open the affected sessions. Use RUM waterfall data, JavaScript errors, and Session Replay to understand whether the issue is behavioral friction, performance, or an application error.

## Create a time series analysis

Create a time series analysis for:

- `Add to cart`
- `Begin checkout`
- `Order submitted`
- `Checkout error`

Compare the series by `version` or `deployment.environment` when enough data exists. This lets you see whether a release, campaign, or incident changed user behavior.

{{< tabs >}}
{{% tab title="Question" %}}
What does DXA add beyond the RUM session list?
{{% /tab %}}
{{% tab title="Answer" %}}
RUM is optimized for troubleshooting individual sessions, page performance, errors, and frontend-to-backend traces. DXA organizes the same RUM events into user segments, funnels, and trend analyses so teams can prioritize experience work by user impact and business outcome.
{{% /tab %}}
{{< /tabs >}}
