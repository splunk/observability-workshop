---
title: 1. Log Filtering
weight: 1
---

The Log Observer UI, or LO for short, can be used in multiple ways. In the introduction tour, you have used the LO **no-code interface** to search for specific entries in your logs. This section however, assumes you have arrived in LO from a viewed trace in APM using the **Related Content** link.

The advantage of this is, as it was with the link between RUM & APM, that you are looking at your logs within the context of your previous actions.  In this case, the context is the time window **(1)**, set to a **specific time range** that is relevant to the trace and the Filter **(2)** is set to the **trace_id** that uniquely identifies the trace.

![Trace Logs](../images/log-observer-trace-logs.png)

This view will include **all** the log lines from **all** applications or services that participated in the back-end transaction started by the end-user interaction with the Online Boutique.

Even in a small application as our Online Boutique, the sheer amount of logs found can make it hard to see the specific log lines that matter to the actual incident we where investigating.

So, let us run an exercise to drill down into the logs:

{{% notice title="Exercise" style="green" icon="running" %}}

We need to focus on just the Error messages in the logs:

* Set the *Group By* drop-down box to **Severity** by selecting it from the list offered then click the {{% button style="blue" %}}Apply{{% /button %}} button.
* Notice that the chart changes and you have a legend of debug, error and info.

![legend](../images/severity-logs.png)

* Selecting just the error logs can be done by either clicking on the word **error** (1) in the legend, followed by selecting the *Add to filter* option from the resulting dialog Box or by simply adding  *severity = error* directly to filter box.
* Either way, you now should have only all the error log lines.
* You could add the service name (*sf_service=paymentservice*) to the filter if there errors lines for multiple services, but in our case that is not really necessary.

![Error Logs](../images/log-observer-errors.png)

{{% /notice %}}

Next, we will look at log entries in detail.
