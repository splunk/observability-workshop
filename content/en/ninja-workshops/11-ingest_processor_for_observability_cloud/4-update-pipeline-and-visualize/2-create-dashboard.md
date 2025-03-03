---
title: Visualize Kubernetes Audit Event Metrics
linkTitle: 4.2 Visualize Kubernetes Audit Event Metrics
weight: 3
---

Now that your metric has dimensions you will create a chart showing the health of different Kubernetes actions using the `verb` dimension from the events.

{{% notice title="Exercise: Visualize Kubernetes Audit Event Metrics" style="green" icon="running" %}}

**1.** If you closed the chart you created in the previous section, in the upper-right corner, click the **+** Icon → **Chart** to create a new chart.

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** In the **Plot Editor** of the newly created chart enter `k8s_audit*` in the metric name field. You will use a wildcard here so that you can see all the metrics that are being ingested.

![Review Metric](../../images/review_metric.png?width=40vw)

**3.** Notice the change from one to many metrics, which is when you updated the pipeline to include the dimensions. Now that we have this metric available, let's adjust the chart to show us if any of our actions have errors associated with them.

![Metric Timeseries](../../images/metric_timeseries.png?width=40vw)

First you'll filter the Kubernetes events to only those that were not successful using the HTTP response code which is available in the **response_status** field. We only want events that have a response code of **409**, which indicates that there was a conflict (for example a trying to create a resource that already exists) or **503**, which indicates that the API was unresponsive for the request.

**4.** In the plot editor of your chart click the **Add filter**, use **response_status** for the field and select **409.0** and **503.0** for the values.

Next, you’ll add a function to the chart which will calculate the total number of events grouped by the **resource**, **action**, and **response status**. This will allow us to see exactly which actions and the associated resources had errors. Now we are only looking at Kubernetes events that were not successful.

**5.** Click **Add analytics** → **Sum** → **Sum:Aggregation** and add **resource**, **action**, and **response_status** in the **Group by** field.

![Add Metric Filters](../../images/add_metric_filters.png?width=40vw)

**6.** Using the chart type along the top buttons, change the chart to a **heatmap**. Next to the **Plot editor**, click **Chart options**. In the **Group by** section select **response_status** then **action**. Change the **Color threshold** from **Auto** to **Fixed**. Click the blue **+ button** to add another threshold. Change the **Down arrow to Yellow**, the **Middle to orange**. Leave the **Up arrow as red**. Enter **5 for the middle threshold** and **20 for the upper threshold**.

![Configure Thresholds](../../images/configure_thresholds.png?width=40vw)

**7.** In the upper right corner of the chart click the blue **Save as...** ![Preview Button](../../images/save_as_btn.png?height=20px&classes=inline) button. Enter a name for your chart (For Example: Kubernetes Audit Logs - Conflicts and Failures).

![Chart Name](../../images/chart_name.png)

**8.** On the **Choose a dashboard** select **New dashboard**.

![New Dashboard](../../images/new_dashboard.png)

**9.**  Enter a name for your dashboard that includes your initials, so you can easily find it later. Click **Save**.

![New Dashboard Name](../../images/dashboard_name.png)

**10.** Make sure the new dashboard you just created is selected and click **Ok**.

![Save New Dashboard](../../images/save_new_dashboard.png)

You should now be taken to your new Kubernetes Audit Events dashboard with the chart you created. You can add new charts from other metrics in your environment, such as application errors and response times from the applications running in the Kubernetes cluster, or other Kubernetes metrics such as pod phase, pod memory utilization, etc. giving you a correlated view of your Kubernetes environment from cluster events to application health.

![Audit Dashboard](../../images/audit_dashboard.png?width=40vw)

{{% /notice %}}
