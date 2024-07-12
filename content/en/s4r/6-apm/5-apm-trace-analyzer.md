---
title: 5. APM Trace Analyzer
weight: 5
---

As Splunk APM provides a **NoSample™** end-to-end visibility of every service Splunk APM captures every trace. For this workshop, the **Order Confirmation ID** is available as a tag. This means that we can use this to search for the exact trace of the poor user experience you encountered earlier in the workshop.

{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud provides several tools for exploring application monitoring data. **Trace Analyzer** is suited to scenarios where you have high-cardinality, high-granularity searches and explorations to research unknown or new issues.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* With the outer box of the **paymentservice** selected, in the right-hand pane, click on **Traces**.
* To ensure we are using **Trace Analyzer** make sure the button {{% button %}}Switch to Classic View{{% /button %}} is showing. If it is not, click on {{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}}.

{{% /notice %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

The **Trace & error count** view shows the total traces and traces with errors in a stacked bar chart. You can use your mouse to select a specific period within the available time frame.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the dropdown menu that says **Trace & error count**, and change it to **Trace duration** 

{{% /notice %}}

![APM Trace Analyzer Heat Map](../images/apm-trace-analyzer-heat-map.png)

The **Trace Duration** view shows a heatmap of traces by duration.  The heatmap represents 3 dimensions of data:

1. Time on the x-axis
2. Trace duration on the y-axis
3. The traces (or requests) per second are represented by the heatmap shades

You can use your mouse to select an area on the heatmap, to focus on a specific time period and trace duration range.  

{{% notice title="Exercise" style="green" icon="running" %}}

* Switch from **Trace duration** back to **Trace & Error count**.
* In the time picker select **Last 1 hour**.
* Note, that most of our traces have errors (red) and there are only a limited amount of traces that are error-free (blue).
* Make sure the **Sample Ratio** is set to `1:1` and **not** `1:10`.
* Click on **Add filters**, type in `orderId` and select **orderId** from the list.
* Paste in your **Order Confirmation ID** from when you went shopping earlier in the workshop and hit enter. If you didn't capture one, please ask your instructor for one.
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /notice %}}

We have now filtered down to the exact trace where you encountered a poor user experience with a very long checkout wait. A secondary benefit to viewing this trace is that the trace will be accessible for up to 13 months. This will allow developers to come back to this issue at a later stage and still view this trace for example.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the trace in the list.

{{% /notice %}}

Next, we will walk through the trace waterfall.
