---
title: 4. APM Service Breakdown
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

* In the right-hand pane click on the {{% button style="grey"  %}}Breakdown{{% /button %}}.
* Select `tenant.level` in the list.  This is a tag that exposes the customers' status and can be useful to see trends related to customer status.
* Back in the Service Map Click on **gold** to select it.
* Click on {{% button style="grey"  %}}Breakdown{{% /button %}} and select `version`, this is the tag that exposes the service version.
* Repeat this for **silver** and **bronze**.
{{< tabs >}}
{{% tab title="Question" %}}
**What can you conclude from what you are seeing?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Every tenant is being impacted by `v350.10`**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

You will now see the **paymentservice** broken down into three services, **gold**, **silver** and **bronze**. Each tenant is broken down into two services, one for each version (`v350.10` and `v350.9`).

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on the outer main box that surrounds the 3 red circles, the box will become highlighted.

{{% /notice %}}

{{% notice title="Span Tags" style="info" %}}
Using span tags to break down services is a very powerful feature. It allows you to see how your services are performing for different customers, different versions, different regions, etc. In this exercise, we have determined that `v350.10` of the **paymentservice** is causing problems for all our customers.
{{% /notice %}}

Next, we need to drill down into a trace to see what is going on.
