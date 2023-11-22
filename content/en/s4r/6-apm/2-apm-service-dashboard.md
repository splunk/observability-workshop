---
title: 2. APM Service Dashboard
weight: 2
---

Splunk APM provides a set of built-in dashboards that present charts and visualized metrics to help you see problems occurring in real time and quickly determine whether the problem is associated with a service, a specific endpoint, or the underlying infrastructure.

APM dashboards present request, error, and duration (RED) metrics based on Monitoring MetricSets created from endpoint spans for your services, endpoints, and Business Workflows. They also present related host and Kubernetes metrics to help you determine whether problems are related to the underlying infrastructure.

{{% notice title="Exercise" style="green" icon="running" %}}

* From the main menu select **APM**, select **Explore**, then click on the **paymentservice**.
* Click on **View Dashboard** top right of the **paymentservice** pane.
* In the **Request rate** text chart, click the **...** and select **Copy**. Note that you now have a **1**  before the **+**  at the top right of the page, indicating you have a copied chart to the clipboard.
* Click the **...** in the **Error rate** text chart and select **Add to clipboard**. Note that you now have **2** before the **+** on the top right of the page.

{{% /notice %}}

We will be using these charts later on in the workshop.

![Service Dashboard](../images/apm-service-dashboard.png)
