---
title: 6. APM Waterfall
weight: 6
---

We have arrived at the **Trace Waterfall** from the **Trace Analyzer**. A trace is a collection of spans that share the same trace ID, representing a unique transaction handled by your application and its constituent services.

Each span in Splunk APM captures a single operation. Splunk APM considers a span to be an error span if the operation that the span captures results in an error.

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the {{% button style="red"  %}}!{{% /button %}} next to the **paymentservice** span in the waterfall.
* What is the error message being reported in the span metadata?

{{% /notice %}}

At the very bottom of the **Trace Waterfall** click on the word **Logs(1)**. This highlights that there are **Related Logs** for this trace.

![Related Logs](../images/apm-related-logs.png)

Related Content relies on specific metadata that allow APM, Infrastructure Monitoring, and Log Observer to pass filters around Observability Cloud. For related logs to work, you need to have the following metadata in your logs:

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

Click on the **Related Logs** link to view the logs for this trace. This will open the **Log Observer** in a new tab.
