---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="Break down the service by version" %}}

* Select the **paymentservice** in the Service Map.
* In the right-hand pane click on the {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Select `version` in the list.
{{< quiz question="What can you conclude from what you are seeing?" >}}
{{< quiz-option correct=true >}}`v350.9` has no errors. `v350.10` has a problem.{{< /quiz-option >}}
{{< quiz-option >}}Both versions are healthy.{{< /quiz-option >}}
{{< quiz-option >}}Only `v350.9` is failing.{{< /quiz-option >}}
{{< quiz-feedback >}}
**There are no errors for `v350.9`, but `v350.10` clearly has a problem.**
{{< /quiz-feedback >}}
{{< /quiz >}}

![APM Service Breakdown](../images/apm-service-breakdown.webp)

{{% notice title="Span Tags" style="info" %}}
Using span tags to break down services is a very powerful feature. It allows you to see how your services are performing for different customers, different versions, different regions, etc. In this exercise, we have determined that `v350.10` of the **paymentservice** is causing problems.
{{% /notice %}}

* Next, we need to drill down into a trace to see what is going on. Click on the red circle for `v350.10` **(1)** in the **paymentservice**, then click on the **Traces** **(2)** tab in the right-hand pane.

{{% /exercise %}}
