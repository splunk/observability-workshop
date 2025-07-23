---
title: Confirm Metrics in Observability Cloud
linkTitle: 3.4 Confirm Metrics in Observability Cloud
weight: 5
---

Now that an Ingest Pipeline has been configured to convert Kubernetes Audit Logs into metrics and send them to Splunk Observability Cloud the metrics should be available. To confirm the metrics are being collected complete the following steps:

{{% notice title="Exercise: Confirm Metrics in Splunk Observability Cloud" style="green" icon="running" %}}

**1.** Login to the **Splunk Observability Cloud** organization you were invited for the workshop. In the upper-right corner, click the **+** Icon → **Chart** to create a new chart.

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** In the **Plot Editor** of the newly created chart enter the metric name you used while configuring the **Ingest Pipeline**.

![Review Metric](../../images/review_metric.png?width=40vw)

{{% notice title="Info" style="info" %}}
You should see the metric you created in the Ingest Pipeline. Keep this tab open as it will be used again in the next section.

In the next step you will update the ingest pipeline to add dimensions to the metric, so you have additional context for alerting and troubleshooting.
{{% /notice %}}

{{% /notice %}}
