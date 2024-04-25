---
title: Verify Kubernetes Cluster metrics
linkTitle: 3. Verify everything is working
weight: 4
---

Once the installation has been completed, you can log in to **Splunk Observability Cloud** and verify that the metrics are flowing in from your Kubernetes cluster.

From the left-hand menu click on **Infrastructure** ![infra](../images/infra-icon.png?classes=inline&height=25px) and select **Kubernetes**, then select the **K8s nodes** pane. Once you are in the **K8s node** view, change the **Time** filter from **4h** to the **last 15 Minutes (-15m)** to focus on the latest data.

Next, click **Add filters** (next to the **Time filter**) and add the filter `k8s.cluster.name` **(1)**. Type or select the cluster name of your workshop instance (you can get the unique part from your cluster name by using the `INSTANCE` from the output from the shell script you ran earlier). (You can also select your cluster by clicking on its image in the cluster pane.)
You should now only have your cluster visible **(2)**.

![Navigator](../images/navigator.png)

You should see metrics **(3)** of your cluster and the log events **(4)** chart should start to be populated with log line events coming from your cluster. Click on one of the bars to peek at the log lines coming in from your cluster.

![logs](../images/k8s-peek-at-logs.png)
