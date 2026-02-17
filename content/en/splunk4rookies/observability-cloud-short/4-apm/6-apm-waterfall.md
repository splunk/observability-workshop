---
title: 6. APM Waterfall
weight: 6
---

The **Trace Waterfall** view displays all spans within a trace as a hierarchical timeline. Each span appears as a horizontal bar, with the bar's length representing its duration and its position showing when it occurred relative to other spans.

A trace is a collection of spans that share the same trace ID, representing a unique transaction handled by your application and its constituent services.

A span represents a single unit of work within a trace, capturing information about a specific operation such as an API call, database query, or service request. Each span includes metadata like the operation name, start time, duration, and associated tags or attributes that provide context about the work being performed.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the {{% button style="red"  %}}!{{% /button %}} next to any of the `paymentservice:grpc.hipstershop.PaymentService/Charge` spans in the waterfall.

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{< tabs >}}
{{% tab title="Question" %}}
**What is the error message and version being reported in the Span Details?**
{{% /tab %}}
{{% tab title="Answer" %}}
**`Invalid request` and `v350.10`**.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
