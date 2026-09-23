---
title: 5. APM Service Breakdown
weight: 5
---

{{% exercise title="Break down the service by version" %}}

The Service Map normally represents each service as a single circle. The Breakdown option divides a selected service into separate circles based on the values of a span tag. This lets you compare versions, regions, customer groups, or other dimensions directly on the map.

* Select the **payment** service in the Service Map.
* In the right-hand pane open {{% button style="grey"  %}}Breakdown{{% /button %}}.**(1)**. and select `version` in the list.
The **payment** service is now displayed as a separate circle for each version. The color of each circle indicates its health, while the value beneath it shows its latency.

{{< notice >}}
The available breakdown options depend on the span tags in your environment. Tag names and values may differ if your organization uses different instrumentation or naming standards.
{{< /notice >}}

{{< tabs >}}
{{% tab title="Question" %}}
**Which version of the *payment* service is associated with the errors and high latency? What evidence on the map supports your conclusion?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Version *v350.10* is associated with the problem. Its circle is *red* and its latency is *several seconds*, while *v350.9* has no error indication and responds in milliseconds. Your exact latency values may differ, but the contrast between the versions should be similar.**
{{% /tab %}}
{{< /tabs >}}

![APM Service Breakdown](../images/apm-service-breakdown.png)

#### Why this matters
Breaking a service down by span tags helps isolate a problem to a specific version or other deployment characteristic. In this case, the comparison suggests that the issue is specific to v350.10, rather than affecting every instance of the payment service.

#### Continue to a trace
* Select the red circle for **v350.10 (2)**.
* In the right-hand pane, click on the **Traces (3)** tab in the right-hand pane.

{{% /exercise %}}
