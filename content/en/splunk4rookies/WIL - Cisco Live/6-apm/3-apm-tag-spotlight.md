---
title: 3. APM Tag Spotlight*
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

* To view the tags for the **paymentservice** click on the **paymentservice** and then click on **Tag Spotlight** in the right-hand side functions pane (you may need to scroll down depending upon your screen resolution).* Once in **Tag Spotlight** ensure the toggle **Show tags with no values** is off.

{{% /notice %}}

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

The views in **Tag Spotlight** are configurable for both the chart and cards. The view defaults to **Requests & Errors**.

It is also possible to configure which tag metrics are displayed in the cards. It is possible to select any combinations of:

* Requests
* Errors
* Root cause errors
* P50 Latency
* P90 Latency
* P99 Latency

Also ensure that the **Show tags with no values** toggle is unchecked.

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Which card exposes the tag that identifies what the problem is?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The *version* card. The number of requests against `v350.10` matches the number of errors i.e. 100%**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

Now that we have identified the version of the **paymentservice** that is causing the issue, let's see if we can find out more information about the error. Click on **← Tag Spotlight** at the top of the page to get back to the Service Map.
