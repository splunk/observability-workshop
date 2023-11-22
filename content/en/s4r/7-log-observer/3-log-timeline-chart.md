---
title: 3. Log Timeline Chart
weight: 3
---

The Log Timeline chart is a powerful tool for visualizing log messages over time. It is a great way to see the frequency of log messages and to identify patterns. It is also a great way to see the distribution of log messages across your environment. These charts can be saved to a custom dashboard (we will come on to this later in the workshop).

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Click on the cog to open **Table Settingis**, untick **_raw** and ensure the following are selected:
  * `k8s.pod_name`
  * `message`
  * `version`
  ![Log Table Settings](../images/log-observer-table.png)
* From the time picker, select **Last 15 minutes**.
* Remove the `trace_id` from the filter and add `sf_service=paymentservice` and `sf_environment=[WORKSHOPNAME]`.
* Click **Save** and select **Save to Dashboard**
* Enter **Chart name**. This will be the name of the chart on the dashboard. Use the following format: `initials - Log timeline chart`
* Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and then click {{% button style="blue" %}}New Dashboard{{% /button %}}.
* Enter a name for the new dashboard. Use the following format: `initials - Service Health Dashboard` and click {{% button style="blue" %}}Save{{% /button %}}.
* Ensure the new dashboard is highlighted in the list and click {{% button style="blue" %}}OK{{% /button %}}.
* Click {{% button %}}Save{{% /button %}}.

{{% /notice %}}
