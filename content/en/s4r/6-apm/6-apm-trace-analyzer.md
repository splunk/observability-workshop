---
title: 6. APM Trace Analyzer
weight: 6
---

In the right-hand pane, click on **Traces**. To ensure we are using **Trace Analyzer** make sure the button {{% button %}}Switch to Classic View{{% /button %}} is showing. If it is not, click on {{% button style="blue" %}}Switch to Trace Analyzer{{% /button %}}.

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

The **Trace Analyzer** view shows you all the traces for the selected service. You can filter the traces by any indexed span tag. In this case, we want to filter the traces by `version` as we know from the previous exercise that `v350.10` is causing problems.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Make sure **Sample Ratio** is set to `1:1` and **not** `1:10`.
* Click on **Group traces by** and select `version`.
* Click on the ellipsis next to `v350.10` and click **Add to filter**.
* Click on the **Duration** header twice to sort the traces by duration descending.

![Traces by Duration](../images/apm-traces-by-duration.png)

{{% /notice %}}

Now that we have a filtered list of traces, we need to select one to investigate. Click on the 1st trace in the list. This should be a trace with a long duration as per the screenshot above.

Next, we will walk through the trace waterfall.
