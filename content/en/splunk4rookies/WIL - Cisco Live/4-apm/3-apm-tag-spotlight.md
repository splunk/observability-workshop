---
title: 3. APM Tag Spotlight
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

* To view the tags for the **paymentservice** click on the **paymentservice** and then click on **Tag Spotlight** in the right-hand side functions pane (you may need to scroll down depending upon your screen resolution).
* Once in **Tag Spotlight** ensure the toggle **Show tags with no values** is off.

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

* The views in **Tag Spotlight** are configurable for both the chart and cards. The view defaults to **Requests & Errors**.

{{< tabs >}}
{{% tab title="Question" %}}
**Which card exposes the tag that identifies what the problem is?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *version* card. The number of requests against `v350.10` matches the number of errors i.e. 100%**
{{% /tab %}}
{{< /tabs >}}

* Now that we have identified the version of the **paymentservice** that is causing the issue, let's see if we can find out more information about the error.
* Click the **APM** link above **paymentservice** to return to the **APM Overview**.
* In **APM Overview**, click on **Service Map** in the right hand pane.
{{% /notice %}}
