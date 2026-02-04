---
title: 3. Log Timeline Chart
weight: 3
---

Once you have a specific view in Log Observer, it is very useful to be able to use that view in a dashboard, to help in the future with reducing the time to detect or resolve issues. As part of the workshop, we will create an example custom dashboard that will use these charts.

Let's look at creating a **Log Timeline** chart. The Log Timeline chart is used for visualizing log messages over time. It is a great way to see the frequency of log messages and to identify patterns. It is also a great way to see the distribution of log messages across your environment. These charts can be saved to a custom dashboard.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

First, we will reduce the amount of information to only the columns we are interested in:

* Click on the Configure Table {{% icon icon="cog" %}} icon above the **Logs table** to open the **Table Settings**, untick `_raw` and ensure the following fields are selected `k8s.pod.name`, `message` and `version`.
  ![Log Table Settings](../images/log-observer-table.png)
* Remove the fixed time from the time picker, and set it to the **Last 15 minutes**.
* To make this work for all traces, remove the `trace_id` from the filter and add the fields `sf_service=paymentservice` and `sf_environment=[WORKSHOPNAME]`.
* Click **Save** and select **Save to Dashboard**.
  ![save it](../images/save-query.png)
* In the chart creation dialog box that appears, for the **Chart name** use `Log Timeline`.
* Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and then click {{% button style="blue" %}}New dashboard{{% /button %}} in the Dashboard Selection dialog box.
* In the **New dashboard** dialog box, enter a name for the new dashboard (no need to enter a description). Use the following format: `Initials - Service Health Dashboard` and click {{% button style="blue" %}}Save{{% /button %}}
* Ensure the new dashboard is highlighted in the list **(1)** and click {{% button style="blue" %}}OK{{% /button %}} **(2)**.
  ![Save dashboard](../images/dashboard-save.png)
* Ensure that **Log Timeline** is selected as the **Chart Type**.
  ![log timeline](../images/log-timeline.png?classes=left&width=25vw)
* Click the {{% button %}}Save{{% /button %}} button (**do not** click **Save and goto dashboard** at this time).

{{% /notice %}}

Next, we will create a **Log View** chart.
