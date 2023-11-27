---
title: 4. APM Service Breakdown
weight: 4
---

From the service map view, click on **paymentservice** to select it. You can use the Breakdown selector to break the service down by any indexed span tag.

More story here ...

{{% notice title="Exercise" style="green" icon="running" %}}

* In the right-hand pane there is a button {{% button style="grey"  %}}Breakdown{{% /button %}}. Click on this button to view the tags the service can be broken down by.
* Select `tenant.level`.
* What can you conclude from what you are seeing?
* Click on **gold** to select it.
* Click on {{% button style="grey"  %}}Breakdown{{% /button %}} and select `version`.
* Repeat this for **silver** and **bronze**.
* What can you conclude from what you are seeing?

{{% /notice %}}

You will now see the **paymentservice** broken down by `tenant.level` and each tenant broken down by `version`. You can see that the **paymentservice** is broken down into three services **gold**, **silver** and **bronze**. Each tenant is broken down into two services, one for each version (`v350.10` and `v350.9`).

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on any one of the red dotted lines coming from the **checkoutservice** to `v350.10`.
* Take a look at the **Service-to-Service Requests & Errors** chart.
* What percentage of errors are there?

{{% /notice %}}

Using span tags to break down services is a very powerful feature. It allows you to see how your services are performing for different customers, different versions, different regions, etc. In this exercise, we have determined that `v350.10` of the **paymentservice** is causing problems for our customers.

Next, we need to drill down into a trace to see what is going on.
