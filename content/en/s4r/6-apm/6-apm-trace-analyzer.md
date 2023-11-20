---
title: 6. APM Trace Analyzer
weight: 6
---

In the right-hand pane, click on **Traces**. To ensure we are using **Trace Analyzer** make sure the button {{% button %}}Switch to Classic View{{% /button %}} is showing. If it is not, click on {{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}}.

Splunk Observability Cloud provides several tools for exploring application monitoring data. **Trace Analyzer** is suited to scenarios where you have high-cardinality, high-granularity searches and explorations to research unknown or new issues.

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

In **Trace Analyzer** you can filter traces by any indexed/unindexed span tag. In this case, we want to filter the traces by `version` as we know from the previous exercise that `v350.10` is causing problems.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* In the time picker select **Last 1 hour**.
* Make sure **Sample Ratio** is set to `1:1` and **not** `1:10`.
* Click on **Group traces by** and select `version`.
* Click on the ellipsis next to `v350.10` and click **Add to filter**.
* Click **Add filters**, type in **orderId** and select **orderId** from the **Unindexed Tags** list.
* Paste in your **Order Confirmation ID** from when you went shopping earlier in the workshop and hit enter.

![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /notice %}}

We have now filtered down to the exact trace where you encountered a poor user experience with a very long checkout wait. Click on the trace in the list.

Next, we will walk through the trace waterfall.
