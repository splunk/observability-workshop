---
title: 4. APM Service Breakdown
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

* Select the **wire-transfer-service** in the Service Map.
* In the right-hand pane click on the {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Select `tenant.level` in the list.
* Back in the Service Map click on **gold** (our most valuable user tier).
* Click on {{% button style="grey"  %}}Breakdown{{% /button %}} and select `version`, this is the tag that exposes the service version.
* Repeat this for **silver** and **bronze**.
{{< tabs >}}
{{% tab title="Question" %}}
**What can you conclude from what you are seeing?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Every `tenant.level` is being impacted by `v350.10`**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

You will now see the **wire-transfer-service** broken down into three services, **gold**, **silver** and **bronze**. Each tenant is broken down into two services, one for each version (`v350.10` and `v350.9`).

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Span Tags" style="info" %}}
Using span tags to break down services is a very powerful feature. It allows you to see how your services are performing for different customers, different versions, different regions, etc. In this exercise, we have determined that `v350.10` of the **wire-transfer-service** is causing problems for all our customers.
{{% /notice %}}

Next, we need to drill down into a trace to see what is going on.
