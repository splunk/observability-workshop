---
title: One view, two perspectives
linkTitle: 6. One view, two perspectives
weight: 6
time: 5 minutes
---

Synthetics provides the **lab** perspective of user experience, while RUM provides the **field** perspective. While the lab is controlled and operating regardless of user traffic, the field reflects the reality of our end users - including all uncontrolled variables like activity, device version, network, geolocation, and so on.

{{% exercise title="Read the combined dashboard" %}}

* From the main menu, select **Dashboards** and open the **Digital Experience — Astronomy Shop** dashboard group for this workshop.
* Work down the dashboard and answer these three questions in order:
  1. **Is it available?** Check the synthetic uptime and failed run count.
  2. **What's happening for end users?** Check whether real user errors and checkout durations move at the same time.
  3. **What is broken?** Check the synthetic transaction durations to see whether browsing or checkout degraded.

<!-- TODO screenshot: Combined RUM and Synthetics dashboard showing the synthetic row above the real user row -->
![Combined RUM and Synthetics dashboard](../images/dem-dashboard.png)

{{% /exercise %}}

<!--
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
-->
## Better together

What does comparing Synthetic metrics to RUM help us understand? Here are some examples.

| Pair these | Synthetic says | RUM says | Together they tell us |
|---|---|---|---|
| Synthetic LCP vs. real user LCP | What the page does under controlled conditions | What customers on real devices and networks got | Whether a slowdown is our application or our customers' conditions. If the lab is fast and reality is slow, the problem could be related to the users' network, devices, or a scenario outside of our testing. |
| `Checkout` synthetic transaction duration vs. Real User checkout workflow duration | How long a scripted workflow takes | How long real workflows take | Real users take longer to complete workflows for many reasons. If the synthetic transaction is still fast, we are providing the best possible starting point for users. If the synthetic transaction slows down, we need to address something on our side. |
| Synthetic uptime vs. RUM Page Views | If the workflow is healthy | If users are attempting any workflows | Lack of RUM traffic doesn't mean we can't catch issues with critical user journeys. |

{{< quiz question="Why is it important to understand these two points of view?" >}}
{{< quiz-option >}}There's not a problem if only our Synthetics test is failing but our RUM data looks fine.{{< /quiz-option >}}
{{< quiz-option >}}If Synthetics is all green but RUM is showing issues, it's always the end users' fault - or the network.{{< /quiz-option >}}
{{< quiz-option correct=true >}}Synthetics helps us understand if a root cause of an issue is within our control, while RUM helps us prioritize issues based on end user impact.{{< /quiz-option >}}
{{< quiz-feedback >}}
Issues surfaced by both Synthetics and RUM can have many causes. It's important to understand the baseline of performance and experience in both the lab and the field, and understand what changing comparison between them means for our application health.
{{< /quiz-feedback >}}
{{< /quiz >}}

Learn more in [Splunk RUM custom dashboards](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/splunk-rum-dashboards/splunk-rum-custom-dashboards) and [Browser test metrics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/browser-test-metrics).
