---
title: 2. APM Service Dashboard
weight: 2
---

APM Service Dashboards provide request, error, and duration (**RED**) metrics based on Monitoring MetricSets created from endpoint spans for your services, endpoints, and Business Workflows. If you scroll down the dashboard you will also see the host and Kubernetes-related metrics which help you determine whether there are problems with the underlying infrastructure.

![Service Dashboard](../images/apm-service-dashboard.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* We want to use some of these chart in a later exercise, so lets grab them now while we are looking at them:  
  * In the **Request rate** text chart **(1)**, click the **...** and select **Copy**. Note that you now have a **1** before the **+**  at the top right of the page, indicating you have a copied chart to the clipboard. (3)
  * Click  again on the **...** in the **Request rate** line chart **(2)** and select **Add to clipboard**.
* Note that you now have **2** before the **+** on the top right of the page. **(3)**

{{% /notice %}}

![APM Explore](../images/apm-explore.png)

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**In the Service Map hover over the **paymentservice**. What can you conclude from the popup service chart?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The error percentage is very high.**
{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

![APM Service Chart](../images/apm-service-popup-chart.png)

We need to understand if there is a pattern to this error rate. We have a handy tool for that, **Tag Spotlight**.
