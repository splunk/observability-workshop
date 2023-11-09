---
title: Splunk Infrastructure exercise with the Kubernetes Navigator
linkTitle: Exercise part 2
description: This section of the workshop provides an exercise using Splunk infra monitoring based on the Kubernetes Navigator.
weight: 10
---

{{% button icon="clock" %}}10 minutes{{% /button %}}

This is Part 2, of the Infrastructure Monitoring exercise, you should now have a single cluster visible.

![Alt Cluster](../images/k8s-cluster.png?width=30vw)

In the Kubernetes Navigator, the cluster is represented by the square with the black line around it and will contain one or more blue squares representing the node(s), each of them containing one or more colored boxes that represent pods. And, as you can guess, **green** means healthy and **red** means that there is a problem.

Given there are two red boxes or tiles, let's see what is going on and if this will affect our E-commerce site.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First, set the time window we are working with to the last 15 minutes. You do this by using the drop-down in the Filter pane **-3h** at the top of the page to **the last 15 minutes**.

* First hover with your mouse over the Cluster, Node and pods, both a **green** & **red** ones. The resulting information pane that appears will tell you the state of the object. Note, That the **red** Pods show that they are in **Pod Phase : Failed**. This means they have crashed and are not working.
Let's examine the Cluster Metric charts that provide information on your cluster, (the charts below the cluster image).  They provide general information about the health of your cluster like the memory consumption and the number of pods per node.

* See if they provide any insight into what the impact of the **red** pods on our e-commerce site is.

* Let's check if the Spunk Kubernetes Analyzer can tell us something more useful, so click on **K8s Analyzer**.
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}
The Spunk Kubernetes Analyzer is a smart process that runs in the background in Splunk Observability Cloud and is designed to detect relations between anomalies.  
{{% /notice %}}

* The **K8s Analyzer** should have detected that the two **red** pods are similar, indicated by the 2 after each line, and come from the same Namespace.
* In the K8s analyzer view can you find what namespace? (hint, look for `k8s.namespace.name`).

* Next, we want to check this on the node level as well, so drill down to the node, first by hovering your mouse over the cluster until you see a blue line appear around the node with a ![blue triangle ](../images/node-blue-traingle.png?classes=inline) in the left top, followed by clicking on it. Your view should now show little boxes in each pod, these represent the actual containers that contain the actual code that is running but the *K8s Analyzer* should confirm that this issue is also occurring on the node level.

![Analyser result](../images/k8s-analyser-result.png?width=20vw)

* Click on **K8s node**. This will show the node metrics, and if you examine the charts, you can see that there are only two pods in the development namespace.

* It is easier to see if you filter on the `k8s.namespace.space=development` in the Filter Pane. The **# Total Pods** chart shows only two pods and in the **Node Workload** chart there is only the *test-job* and it has failed.

{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}
The above scenario is common in a shared Kubernetes environment, where teams deploy applications in different stages. Kubernetes is designed to keep these environments completely separate.
{{% /notice %}}

{{% /notice %}}

None of the Pods that make up our e-commerce site run in the development namespace and all the other pods are green, we can safely assume these pods do not affect us, so let's move on to look at a few more things.
