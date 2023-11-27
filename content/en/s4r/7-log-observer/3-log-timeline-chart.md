---
title: 3. Log Timeline Chart
weight: 3
---
Once you have found a specific view in Log Observer, it can be very useful to use that specific view in a dashboard, to help in the future with reducing the time to detect or resolve issues.
As part of the workshop, we will create an example Custom Dashboard that will use these charts.

Let's look at the first charting options *Log Timeline* first.

The Log Timeline chart is a powerful tool for visualizing log messages over time. It is a great way to see the frequency of log messages and to identify patterns. It is also a great way to see the distribution of log messages across your environment. These charts can be saved to a custom dashboard (we will come on to this later in the workshop).

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

First we will reduce the information to just the columns we are interested in and make the chart generic:

* Click on the **⚙️** (cog) at to open **Table Settings**, untick **_raw** and ensure the following fields are selected:
  * `k8s.pod_name`
  * `message`
  * `version`

![Log Table Settings](../images/log-observer-table.png)

* If need be, you can drag the column in the right orderby selecting the header and drag the **︙︙** that will appear.
* Remove the fixed time from the time picker, and select the **Last 15 minutes**.
* To make it work for all traces, remove the `trace_id` from the filter and add `sf_service=paymentservice` and `sf_environment=[WORKSHOPNAME]`.
* Click **Save** and select **Save to Dashboard**.

![save it](../images/save-query.png)

* In the chart creation dialog box that appears, enter the **Chart name**, this will be the name of the chart on the dashboard. Use the following format: `Initials - Log Timeline Chart`
* Ensure **Log Timeline** is selected as the **Chart Type**.

![log timeline](../images/log-timeline.png?width=20vw)

* Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and then click {{% button style="blue" %}}New Dashboard{{% /button %}} in the follow-up Dashboard Selection dialog box.
* Again you get a new dialog box, this time to create a dashboard. Enter a name for the new dashboard (no need to enter a description). Use the following format: `Initials - Service Health Dashboard` and click {{% button style="blue" %}}Save{{% /button %}}
* Ensure the new dashboard is highlighted in the list (1) and click {{% button style="blue" %}}OK{{% /button %}} (2)

![save dashboard](../images/dashboard-save.png?width=40vw)

* Click the {{% button %}}Save{{% /button %}} button.

{{% /notice %}}
