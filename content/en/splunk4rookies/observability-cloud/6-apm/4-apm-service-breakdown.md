---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="Break down by tenant level" %}}

* Select the **paymentservice** in the Service Map.
* In the right-hand pane click on the {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Select `tenant.level` in the list.
* Back in the Service Map click on **gold**.
* Click on {{% button style="grey"  %}}Breakdown{{% /button %}} and select `version`, this is the tag that exposes the service version.
* Repeat this for **silver** and **bronze**.
{{< quiz question="What can you conclude from what you are seeing?" >}}
{{< quiz-option correct=true >}}Every `tenant.level` is affected by `v350.10`.{{< /quiz-option >}}
{{< quiz-option >}}Only one tenant level is affected.{{< /quiz-option >}}
{{< quiz-option >}}`v350.9` is the version causing the errors.{{< /quiz-option >}}
{{< quiz-feedback >}}
**Every `tenant.level` is being impacted by `v350.10`**
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

You will now see the **paymentservice** broken down into three services, **gold**, **silver** and **bronze**. Each tenant is broken down into two services, one for each version (`v350.10` and `v350.9`).

![APM Service Breakdown](../images/apm-service-breakdown.webp)

{{% notice title="Span Tags" style="info" %}}
Using span tags to break down services is a very powerful feature. It allows you to see how your services are performing for different customers, different versions, different regions, etc. In this exercise, we have determined that `v350.10` of the **paymentservice** is causing problems for all our customers.
{{% /notice %}}

Next, we need to drill down into a trace to see what is going on.
