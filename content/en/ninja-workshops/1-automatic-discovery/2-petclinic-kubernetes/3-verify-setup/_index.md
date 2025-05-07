---
title: Verify Kubernetes Cluster metrics
linkTitle: 3. Verify Cluster Metrics
weight: 4
time: 10 minutes
---

Once the installation has completed, you can log in to **Splunk Observability Cloud** and verify that the metrics are flowing in from your Kubernetes cluster.

From the left-hand menu, click on **Infrastructure** and select **Kubernetes**, then select the **Kubernetes nodes** pane. Once you are in the **Kubernetes nodes** view, change the **Time** filter from **-4h** to the last 15 minutes **(-15m)** to focus on the latest data.

Next, from the list of nodes, select the Node name of your workshop instance. Note: You can get the unique part from your cluster name by using the `INSTANCE` from the output from the shell script you ran earlier. **(1)**

![NavigatorList](../images/navigatorlist.png)

Open the **Hierarchy Map** by clicking on the *Hierarchy Map* link in the gray pane to show the graphical representation of your node.

![HeirarchyMap](../images/hierarchymap.png)

You will now only have your cluster visible. Scroll down the page to see the metrics coming in from your cluster. Locate the **Node log events rate** **(1)** chart and click on a vertical bar to see the log entries coming in from your cluster.

![Logs](../images/k8s-peek-at-logs.png)
