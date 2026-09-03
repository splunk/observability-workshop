---
title: 6. APM Trace Analyzer
weight: 6
---

We have arrived at the **Trace Analyzer**.

**Trace Analyzer** is a powerful tool in Splunk APM designed for exploring and analyzing distributed traces at scale. Because Splunk APM captures every trace with **full-fidelity** (*NoSample)*, you have complete visibility into all transactions flowing through your services.

Trace Analyzer enables you to:

* **Search with high-cardinality tags**: Filter traces using any indexed span tag, such as customer IDs, order IDs, or other custom business attributes.
* **Visualize trace patterns**: View trace and error counts over time to identify trends and anomalies.
* **Analyze latency distribution**: Use the heatmap view to understand trace duration patterns and spot outliers.
* **Drill down to specific traces**: Quickly find the exact trace you need, whether investigating a customer complaint or debugging a specific transaction.

This makes Trace Analyzer ideal for investigating unknown issues, researching specific transactions, and performing root cause analysis when you need to find a needle in a haystack.

{{% exercise title="Find a failing checkout trace" %}}

![APM Trace Analyzer](../images/apm-trace-analyzer.png)

The *Trace Analyzer* is already filtered to the affected version of the *payment* service.
* Confirm that the filters include:
  * Your workshop Environment
  * The **payment** service
  * **version** = *v350.10*
* If no traces are displayed, widen the time range until matching traces appear.
* Review the trace results and find a trace that:
  * contains errors in both the *checkout* and *payment* services **(1)**
  * has an initiating operation of `frontend-proxy: POST ingress` **(2)**
  * has a relatively long duration compared with the other results *(+6 sec)* 

* Select the blue **Trace ID ** for that trace.

This opens the **Trace Waterfall**, where you can examine every span in the selected trace and follow the request through the participating services.

{{% /exercise %}}
