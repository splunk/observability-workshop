---
title: 3. Log Timeline Chart
weight: 3
---

The Log Timeline chart is a powerful tool for visualizing log messages over time. It is a great way to see the frequency of log messages and to identify patterns. It is also a great way to see the distribution of log messages across your environment. These charts can be saved to a custom dashboard (we will come on to this later in the workshop).

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Click on the cog to open **Table Settings**, untick **_raw** and ensure the following fields are selected:
  * `k8s.pod_name`
  * `message`
  * `version`

  ![Log Table Settings](../images/log-observer-table.png)

* From the time picker, select **Last 15 minutes**.
* Remove the `trace_id` from the filter and add `sf_service=paymentservice` and `sf_environment=[WORKSHOPNAME]`.
* Click **Save** and select **Save to Dashboard**.
* Enter **Chart name**, this will be the name of the chart on the dashboard. Use the following format: `Initials - Log Timeline Chart`
* Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and then click {{% button style="blue" %}}New Dashboard{{% /button %}}
* Enter a name for the new dashboard (no need to enter a description). Use the following format: `Initials - Service Health Dashboard` and click {{% button style="blue" %}}Save{{% /button %}}
* Ensure the new dashboard is highlighted in the list and click {{% button style="blue" %}}OK{{% /button %}}
* Click {{% button %}}Save{{% /button %}}

{{% /notice %}}

Next, we will create a **Log View** chart.

The **Log View** chart type will allow us to see log messages in our custom dashboard.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Click on **Save** and then **Save to Dashboard** again.
* Enter **Chart name**, this will be the name of the chart on the dashboard. Use the following format: `Initials - Log View Chart`
* Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and search for the Dashboard you created in the previous exercise.
* Click on the returned entry to highlight is and click {{% button style="blue" %}}OK{{% /button %}}
* Ensure **Log View** is selected as the **Chart Type** and click {{% button style="blue" %}}Save and go to dashboard{{% /button %}}
* All being well, you should see something like this:

  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)

{{% /notice %}}
