---
title: Verify Kubernetes Cluster metrics
linkTitle: 3. Verify Cluster Metrics
weight: 4
time: 10 minutes
---

Once the installation has been completed, you can log in to **Splunk Observability Cloud** and verify that the metrics are flowing in from your Kubernetes cluster.

From the left-hand menu click on **Infrastructure** and select **Kubernetes**, then select the **Kubernetes nodes** pane. Once you are in the **Kubernetes nodes** view, change the **Time** filter from **-4h** to the last 15 minutes **(-15m)** to focus on the latest data.

Next, from the list of clusters, select the cluster name of your workshop instance (you can get the unique part from your cluster name by using the `INSTANCE` from the output from the shell script you ran earlier). **(1)**

![NavigatorI](../images/navigatorlist.png)

You can now select your node by clicking on it name **(1)** in the node list.

![NavigatorII](../images/nodelist.png)

Open the **Hierarchy Map** by clicking on the *Hierarchy Map*  **(1)** link in the gray pane to show the graphical representation of your node.

![NavigatorII](../images/hierarchymap.png)

You will now only have your cluster visible.
Scroll down the page to see the metrics coming in from your cluster. Locate the **Node log events rate** chart and click on a vertical bar to see the log entries coming in from your cluster.

![logs](../images/k8s-peek-at-logs.png)
