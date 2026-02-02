---
title: 6. APM Waterfall
weight: 6
---

A trace is a collection of spans that share the same trace ID, representing a unique transaction handled by your application and its constituent services.

Each span in Splunk APM captures a single operation. Splunk APM considers a span to be an error span if the operation that the span captures results in an error.

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
