---
title: 1. Log Filtering
weight: 1
---

The Log Observer ui, or LO for short, can be used in multiple ways. In the introduction tour you have used LO **no code interface**   to search for specific entries in your logs. This section however, assumes you have arrived in LO from a viewed trace in APM using the **Related Content** link.

The advantages of this is, as it was with the link between RUM & APM, that your looking at your logs within the context of your previous actions.  In this case, the context is the time window, set to a *specific time range* that is relevant to the trace and the Filter that is set to the *trace_id* that uniquely identifies the trace.

![Trace Logs](../images/log-observer-trace-logs.png)

This view will include **all** the logs lines from **all * the  applications or services that participated in the the backend transaction, that was started by the Users interaction with the Online Boutique.

Even in the small application as our Online Boutique, the sheer amount of logs can make it hard to see the  the log lines that matter to the actual incident we where investigating. 

So lets run an exercise to drill down into the logs:

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Group By Severity
* Notice that the chart changes and you have a legend of debug, error and info
* Click on error, and add to filter
* Now only have all error fields

![Error Logs](../images/log-observer-errors.png)

{{% /notice %}}
