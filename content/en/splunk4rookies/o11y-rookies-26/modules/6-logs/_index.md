---
title: The silent revenue leak
weight: 6
layout: chapter
time: 30 minutes
description: Investigate a payment shortfall in an apparently healthy application using structured logs, comparisons, and reusable searches.
params:
  images:
    - images/lo.webp
hidden: true
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are an **SRE supporting the Astronomy Shop**. Finance has asked you to investigate a payment discrepancy, although the application's request errors and latency look normal.

{{% /notice %}}

In this scenario, you will use **Logs** to investigate business outcomes recorded by the application. You will:

- Find the events needed to reconcile completed purchases with collected payments.
- Add business fields as result columns to spot unexpected charges and identify the associated promotion.
- Save the investigation for reuse and plan how to verify recovery.

This module is self-contained. You do not need to complete the APM or RUM modules first. Have your workshop login, connection, index, and environment name ready. If needed, use the [login instructions](/splunk4rookies/o11y-rookies-26/modules/1-intro/2-login/) and [Astronomy Shop overview](/splunk4rookies/o11y-rookies-26/modules/1-intro/1-astronomy-shop/).

{{< presenter >}}
Prepare the scenario before learners begin:

1. Record the current feature-flag settings so you can restore them afterward. Set **promoDiscountBug** to **100%**. Disable **paymentFailure**, **paymentUnreachable**, **rumBlueGreen**, and other active faults. The introduction uses **paymentFailure = 50%**, so transition deliberately between modules.
2. Generate new traffic and verify the flags have taken effect. Use fresh browser sessions if earlier routing settings persist. Flag UI changes may reset after a flagd pod restart; recheck the settings before the session.
3. Select a clean investigation window after the configuration change. Verify at least **20 completed orders**, including **three affected orders and three unaffected controls**. These are workshop readiness targets. Extend the clean window or increase load if needed; do not rely on learners waiting for random examples.
4. Confirm request errors and latency are normal for the same environment and period. Use that evidence to support the Operations handoff on the next page. Keep an optional APM service view ready for a brief demonstration.
5. Verify `order placed` events have the required numeric fields. Check currency conversion is healthy before comparing `.usd` amounts; otherwise prepare the exercise with `app.order.currency = USD` and have learners retain that filter throughout. At the recommended flag setting, expect **NONE** and **PROMOTEST100**. The recorded screenshot window also includes **SPRING10** orders with legitimate **10% discounts**; these are not evidence of the fault.
6. Verify access to the connection, index, and saved queries. Confirm search-record limits will not truncate the exercise population. Give learners the environment and exact investigation window; use the same window throughout the analysis.

At **100%**, every promo redemption uses the broken rule, but only about 30% of orders redeem a promo. An already enabled fault can produce a persistent shortfall without a visible downward trend. Do not promise a revenue decline in the timeline.

The last page includes cleanup. Restore the recorded settings only when the shared environment is ready to move to the next module.
{{< /presenter >}}

{{< pager prev="/splunk4rookies/o11y-rookies-26/modules/" prevLabel="Back to Modules" >}}
