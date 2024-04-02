---
title: Correlate Metrics and Logs
linkTitle: 4.1 Correlate Metrics and Logs
weight: 3
authors: ["Tim Hard"]
time: 5 minutes
draft: false
---

In this section, we'll dive into the seamless correlation of metrics and logs facilitated by the robust naming standards offered by **OpenTelemetry**. By harnessing the power of OpenTelemetry within **Splunk Observability Cloud**, we'll demonstrate how troubleshooting issues becomes significantly more efficient for Site Reliability Engineers (SREs) and operators. With this integration, contextualizing data across various telemetry sources no longer demands manual effort to correlate information. Instead, SREs and operators gain immediate access to the pertinent context they need, allowing them to swiftly pinpoint and resolve issues, improving system reliability and performance. 

{{% notice title="Exercise: View pod logs" style="green" icon="running" %}}
The **Kubernetes Pods Dashboard** you created in the previous section already includes a chart which contains all of the pod logs for your Kubernetes Cluster. The log entries are split by container in this stacked bar chart. To view specific log entires perform the following steps:

1. On the **Kubernetes Pods Dashboard** click into one of the bar charts. A modal will open with the most recent log entries for the container you've selected.

![K8s pod logs](../../images/k8s-pod-logs.png?width=40vw)

2. Click one of the log entries. 

![K8s pod log event](../../images/k8s-pod-log-event.png?width=40vw)

Here we can see the entire log event with all of the fields an values. You can search for specific field names or values within the event itself using the **Search for fields** bar in the event.

3. Enter the city you configured during the application deployment

![K8s pod log field search](../../images/k8s-pod-log-field-search.png?width=40vw)

The event will now be filtered to the `store.location` field. This feature is great for exploring large log entries for specific fields and values unique to your environment or to search for keywords like `Error` or `Failure`.

4. Close the event using the `X` in the upper right corner. 
5. Click the **Chart actions** (three horizontal dots) on the **Pod log event rate** chart
6. Click **View in Log Observer**

![View in Log Observer](../../images/k8s-pod-loc.png?width=40vw)

This will take us to **Log Observer**. In the next section you'll create a chart based on log events and add it to the **K8s Pod Dashboard** you cloned in section [3.2 Dashboard Cloning](../../3-reuse-content-across-teams/2-clone-dashboards). You'll also see how this new chart is automatically added to the mirrored dashboard you created in section [3.3 Dashboard Mirroring](../../3-reuse-content-across-teams/3-mirror-dashboards).

{{% /notice %}}