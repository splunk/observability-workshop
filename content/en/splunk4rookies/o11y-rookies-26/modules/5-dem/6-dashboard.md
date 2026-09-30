---
title: One view, both signals
linkTitle: 6. One view, both signals
weight: 6
time: 3 minutes
---

So far we have looked at RUM and Synthetics in their own screens. That is fine while we are building things, and useless during an incident. When the checkout breaks at 02:00, the question is never "what do the RUM charts say" — it is "is this real, how bad is it, and who is affected". Answering that means seeing both signals together.

This page is **look-only**. There is nothing to configure; the instructor will point us at the dashboard.

{{% exercise title="Read the combined dashboard" %}}

* From the main menu, select **Dashboards** and open the **Digital Experience — Astronomy Shop** dashboard group for this workshop.
* Work down the dashboard and answer these three questions in order:
  1. **Is it up?** Check the synthetic uptime and failed run count.
  2. **Is it real?** Check whether real user errors and checkout durations move at the same time.
  3. **Which part broke?** Check the synthetic transaction durations to see whether browsing or checkout degraded.

<!-- TODO screenshot: Combined RUM and Synthetics dashboard showing the synthetic row above the real user row -->
![Combined RUM and Synthetics dashboard](../images/dem-dashboard.png)

{{% /exercise %}}

{{% notice title="Dashboard not there yet?" style="info" %}}
If our workshop org does not have this dashboard, read the chart list below instead. It is a complete specification, so we can build the same view in our own org later — and the reasoning behind the pairings matters more than clicking through it.
{{% /notice %}}

## What goes on it

The dashboard is two rows. The top row is the synthetic test — always on, always comparable. The bottom row is real users — the ground truth.

### Row 1: synthetic (our test)

Filter these on the custom property `workshop:[NAME OF WORKSHOP]`, so the charts pick up everyone's test without being edited.

| Chart | Metric | Notes |
|---|---|---|
| Uptime | `synthetics.run.uptime.percent` | Single value chart, with our detector linked to it |
| Failed runs | `synthetics.run.count` | Filter `failed:true` |
| Run duration | `synthetics.run.duration.time.ms` | Mean aggregation, display units milliseconds |
| Transaction duration | `synthetics.duration.time.ms` | Split by the `transaction` dimension so `Browse` and `Checkout` plot separately |
| Synthetic LCP | `synthetics.webvitals_lcp.time.ms` | The lab measurement |
| Lighthouse score | `synthetics.lighthouse.score` | Requires interactive metrics enabled on the test |

### Row 2: real users (RUM)

Filter these to our environment and application, the same way we filtered the RUM Overview on page 1.

| Chart | Metric | Notes |
|---|---|---|
| Page views | `rum.page_view.count` | Traffic context — a metric that only makes sense next to the others |
| JavaScript errors | `rum.client_error.count` | All RUM errors carry the dimension `sf_error=true` |
| Checkout duration P75 | `rum.workflow.time.ns.p75` | Scoped to the `PlaceOrder` workflow |
| Real user LCP | `rum.webvitals_lcp.time.ns.p75` | The experience measurement |
| Real user CLS | `rum.webvitals_cls.score.p75` | A score, not a time — no units to set |
| Time to first byte | `rum.resource_request.ttfb.time.ns.p75` | Where front-end slowness turns into a back-end question |

Add a **text note** panel at the top left explaining what the dashboard is for and who owns it, and link the uptime detector to the uptime chart so its alert status shows as a coloured border and a bell icon on the dashboard itself.

## The three pairings that make it useful

Any six charts about RUM and six about Synthetics make a dashboard. These specific pairs make it answer questions:

| Pair these | Synthetic says | RUM says | Together they tell us |
|---|---|---|---|
| Synthetic LCP vs. real user LCP | What the page does under controlled conditions | What customers on real devices and networks got | Whether a slowdown is our application or our customers' conditions. If the lab is fast and reality is slow, the problem is weight, distance, or devices — not our code path |
| `Checkout` transaction duration vs. checkout P75 | How long a scripted purchase takes | How long real purchases take | Whether our test still represents reality. When these drift apart, the test has gone stale |
| Synthetic uptime vs. JavaScript errors | Whether the journey completes at all | Whether customers are hitting errors right now | Blast radius. Uptime at zero with high traffic is an emergency; uptime at zero at 03:00 with no traffic is an emergency we get to fix before anyone notices |

{{< notice tip >}}
That last row is the whole point of the module. Without the synthetic signal, the 03:00 case produces no data at all, and the first thing to arrive is a customer's post.
{{< /notice >}}

## Two things that will trip us up when we build it

- **Units do not match.** RUM timing metrics are reported in **nanoseconds** and Synthetics timing metrics in **milliseconds**. Set the display units on every timing chart, otherwise a perfectly healthy LCP will render as an alarming nine-digit number. CLS and Lighthouse are scores and need no units.
- **Do not build charts from scratch.** Open the out-of-the-box **RUM applications** dashboard group, copy the charts we want, and paste them into our own dashboard. Then adjust the filters. Get one chart exactly right, then copy and paste that chart and change only the metric.

Learn more in [Splunk RUM custom dashboards](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/splunk-rum-dashboards/splunk-rum-custom-dashboards) and [Browser test metrics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/browser-test-metrics).
