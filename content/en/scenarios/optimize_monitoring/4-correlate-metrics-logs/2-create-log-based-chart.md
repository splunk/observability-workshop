---
title: Create Log-based Chart
linkTitle: 4.2 Create Log-based Chart
weight: 3
authors: ["Tim Hard"]
time: 5 minutes
draft: false
---

In Log Observer, you can perform codeless queries on logs to detect the source of problems in your systems. You can also extract fields from logs to set up log processing rules and transform your data as it arrives or send data to Infinite Logging S3 buckets for future use. See [What can I do with Log Observer?](https://docs.splunk.com/observability/en/logs/get-started-logs.html#logobserverfeatures) to learn more about Log Observer capabilities.

In this section, you'll create a chart filtered to logs that include errors which will be added to the **K8s Pod Dashboard** you cloned in section [3.2 Dashboard Cloning](../../3-reuse-content-across-teams/2-clone-dashboards).


{{% notice title="Exercise: Create Log-based Chart" style="green" icon="running" %}}
Because you drilled into **Log Observer** from the **K8s Pod Dashboard** in the previous section, the dashboard will already be filtered to your cluster and store location using the `k8s.cluster.name` and `store.location` fields and the bar chart is split by `k8s.pod.name`. To filter the dashboard to only logs that contain errors complete the following steps:

**Log Observer** can be filtered using Keywords or specific key-value pairs.
1. In **Log Observer** click **Add Filter** along the top.
2. Make sure you've selected **Fields** as the filter type and enter `severity` in the **Find a field...** search bar.
3. Select `severity` from the fields list.

You should now see a list of severities and the number of log entries for each.
4. Under **Top values**, hover over Error and click the `=` button to apply the filter.

![Log Observer: Filter errors](../../images/loc-filter-errors.png?width=40vw)

The dashboard will now be be filtered to only log entries with a severity of Error and the bar chart will be split by the Kubernetes Pod that contains the errors. Next you'll save the chart on your **Kubernetes Pods Dashboard**.

5. In the upper right corner of the **Log Observer** dashboard click **Save**.
6. Select **Save to Dashboard**.
7. In the **Chart name** field enter a name for your chart.
8. (Optional) In the **Chart description** field enter a description for your chart.

![Log Observer: Save Chart Name](../../images/loc-save-chart-name.png?width=40vw)

9. Click **Select Dashboard** and search for the name of the Dashboard you cloned in section [3.2 Dashboard Cloning](../../3-reuse-content-across-teams/2-clone-dashboards). 
10. Select the dashboard in the Dashboard Group for your email address.

![Log Observer: Select Dashboard](../../images/loc-select-dashboard.png?width=40vw)

11. Click **OK**
12. For the **Chart type** select **Log timeline**
13. Click **Save and go to dashboard** 

You will now be taken to your **Kubernetes Pods Dashboard** where you should see the chart you just created for pod errors.

![Log Errors Chart](../../images/k8s-pod-log-error-chart.png?width=40vw)

Because you updated the original **Kubernetes Pods Dashboard**, your mirrored dashboard will also include this chart as well! You can see this by clicking the mirrored version of your dashboard along the top of the Dashboard Group for your user.

![Log Errors Chart](../../images/k8s-pod-select-dashboard.png?width=40vw)

<center><b>
Now that you've seen how data can be reused across teams by cloning dashboard, creating dashboard mirrors and how metrics can easily be correlated with logs, let's take a look at how to create alerts so your teams can be notified when there is an issue with their infrastructure, services, or applications.
</b></center>
{{% /notice %}}
