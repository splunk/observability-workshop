---
title: 2. APM Service Dashboard
weight: 2
---

APM dashboards present request, error, and duration (RED) metrics based on Monitoring MetricSets created from endpoint spans for your services, endpoints, and Business Workflows. They also present related host and Kubernetes metrics to help you determine whether problems are related to the underlying infrastructure.

![Service Dashboard](../images/apm-service-dashboard.png)

Note: *Need to explain some of the charts in the dashboard, and include using it the exercise*

{{% notice title="Exercise" style="green" icon="running" %}}

* In the **Request rate** text chart, click the **...** and select **Copy**. Note that you now have a **1** before the **+**  at the top right of the page, indicating you have a copied chart to the clipboard.
* Click the **...** in the **Error rate** text chart and select **Add to clipboard**. Note that you now have **2** before the **+** on the top right of the page.

{{% /notice %}}

We will be using these charts later on in the workshop. Click the back button in your browser to return to the Service Map.

![APM Explore](../images/apm-explore.png)

<!--
{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* In the Service Map hover over the **paymentservice**. What can you conclude from the popup service chart?

{{% /notice %}}

![APM Service Chart](../images/apm-service-popup-chart.png)

We need to understand if there is a pattern to this error rate. We have a handy tool for that, **Tag Spotlight**.
-->