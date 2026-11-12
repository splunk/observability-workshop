---
title: 2. Scope the investigation
weight: 2
time: 6 minutes
---

Start with a clear scope so that every comparison refers to the same application and period.

{{% exercise title="Open Logs and select your environment" %}}

1. Open **Logs** from the main navigation in Splunk Observability Cloud. Use **Builder** for this exercise.
2. Select the **connection** and **index** provided by your instructor.
3. In the time picker, select **Custom → Absolute** and enter the investigation window provided by your instructor. Check the displayed timezone, then select **Apply**. Keep this window unchanged while comparing results.
4. Remove any trace ID, severity, or other filters left over from an earlier investigation.
5. Select **Add Filter → Fields**, search for `deployment.environment`, select the field, enter your workshop environment, and select **include**. Repeat for `service.name = checkout`.
6. Select **Run search**. 

{{% /exercise %}}

The **timeline** summarizes matching log activity. The **Logs table** contains individual events, and the **Fields** list helps you explore their structured attributes.

![Checkout logs scoped to the workshop environment, one index, and a fixed investigation window](../images/checkout-scope.jpg)

Checkout coordinates an order across several services and emits several kinds of events. On the next page, you will choose the event that records a completed purchase.

{{% notice title="Check your scope" style="info" %}}
If no checkout events appear, check your connection, index, environment, and time window with your instructor. A blank search is not evidence that the application is healthy or that the discrepancy has been resolved.
{{% /notice %}}
