---
title: 6. APM Waterfall
weight: 6
---

We have arrived at the **Trace Waterfall** from the **Trace Analyzer**. A trace is a collection of spans that share the same trace ID, representing a unique transaction handled by your application and its constituent services.

Each span in Splunk APM captures a single operation. Splunk APM considers a span to be an error span if the operation that the span captures results in an error.

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the {{% button style="red"  %}}!{{% /button %}} next to any of the `paymentservice:grpc.hipstershop.PaymentService/Charge` spans in the waterfall.

{{< tabs >}}
{{% tab title="Question" %}}
**What is the error message and version being reported in the span metadata?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Invalid request and `v350.10`**.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
Now that we have identified the version of the **paymentservice** that is causing the issue, let's see if we can find out more information about the error. This is where **Related Logs** come in.

![Related Logs](../images/apm-related-logs.png)

Related Content relies on specific metadata that allow APM, Infrastructure Monitoring, and Log Observer to pass filters around Observability Cloud. For related logs to work, you need to have the following metadata in your logs:

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

{{% notice title="Exercise" style="green" icon="running" %}}

* At the very bottom of the **Trace Waterfall** click on the word **Logs (1)**. This highlights that there are **Related Logs** for this trace.
* Click on the **Logs for trace XXX** entry in the pop-up, this will open the logs for the complete trace in **Log Observer**.

{{% /notice %}}
