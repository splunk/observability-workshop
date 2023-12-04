---
title: 5. APM Trace Analyzer
weight: 5
---
{{% notice title="Trace Analyzer" style="info" %}}

Splunk Observability Cloud provides several tools for exploring application monitoring data. **Trace Analyzer** is suited to scenarios where you have high-cardinality, high-granularity searches and explorations to research unknown or new issues.
{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* With the outer box of the **paymentservice**  selected, in the right-hand pane, click on **Traces**.
* To ensure we are using **Trace Analyzer** make sure the button {{% button %}}Switch to Classic View{{% /button %}} is showing. If it is not, click on {{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}}.

{{% /notice %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* In the time picker select **Last 1 hour**.
* Note, that most of our traces have errors (red) and there are only a limited amount of traces error free (blue).
* Make sure the **Sample Ratio** is set to `1:1` and **not** `1:10`.
* Click on **Add filters**, type in `orderId` and select **orderId** from the list.
* Paste in your **Order Confirmation ID** from when you went shopping earlier in the workshop and hit enter.
  ![Traces by Duration](../images/apm-trace-by-duration.png)

{{% /notice %}}

We have now filtered down to the exact trace where you encountered a poor user experience with a very long checkout wait.  As a secondary benefit of viewing this trace now, you also made sure that trace will be accessible up to 13 months from now. This will allow developers to come back to this issue at a later stage, and still view this trace for example.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the trace in the list.

{{% /notice %}}

Next, we will walk through the trace waterfall.
