---
title: Splunk Infrastructure exercise with the Kubernetes Navigator
linkTitle: Exercise part 2
description: This section of the workshop provides an exercise using Splunk infra monitoring based on the Kubernetes Navigator.
weight: 10
---

{{% button icon="clock" %}}10 minutes{{% /button %}}

This is the second section, of the infra monitoring exercise,
You should now have your single cluster visible.

![Alt Cluster](../images/k8s-cluster.png?width=30vw)

In the Kubernetes Navigator, your cluster is represented by the square with the black line, it will contain one or more  blue squares representing the node(s), each of them wil contain one or more colored boxes that represent pods.
And as you can guess, *Green* means healthy & *Red* means that there is a problem.

Given there are two red boxes or tiles, lets see what is going on and if this will affect our E-commerce site.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First, set the time window we are working with to the last 15 minutes. You do this by using the drop down in the Filter pane ![time-window](../../../images/time-window.png?classes=inline) at the top of the page to *the last 15 minutes*.
* First hoover with you mouse over the Cluster, Node and pods, both a *Green* & *Red* ones. The resulting information pane that appears will tell you the state of the object, Note, That the *Red* Pods show that they are in *Pod Phase : Failed* . This means they have crashed and are are not working.
* Lets examine the Cluster Metric charts that provide information on your cluster,(the charts below the cluster image).  They provide general information about the health of your cluster like the memory consumption and the number of pods per node.
* See if they provide any insight what the impact of the *Red* pods on our e-commerce site is?

* Let's check if the Spunk Kubernetes Analyzer can tell us something more useful, so click on **K8s analyzer**.
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}
The Spunk Kubernetes Analyzer is a smart process that runs in the background in the Splunk Observability Suite, it is designed to detect relations between anomalies.  
{{% /notice %}}

* The *K8s analyser* should have detected that the two *Red* pods are similar, indicated by the 2 after each line, and come from the same Namespace.
* In the K8s analyzer view can you find what name space?  (hint, look for *k8s.namespace.name*.)

* Next, we want to check this on the node level as well, so drill down to the node, first by hoovering your mouse over the cluster until you see a blue line appear around the node with a ![blue triangle ](../images/node-blue-traingle.png?classes=inline) in the left top, follow by clicking on it. Your view should now show little boxes in each pod, these are representing the actual containers that contain the actual code that is running but the *K8s analyser* should confirm that this issue is also occurring on the node level.

![Analyser result](../images/k8s-analyser-result.png?width=20vw)

* Click on **K8s node**. This will show the node metrics, and if you examine the charts, you can see that there are only *two pods in the development name* space.

* It is easier to see if you filter on the *k8s.namespace.space=development* in the Filter Pane. The *# Total Pods* chart shows only two pods and in the *Node Workload* chart  teh is only the *test-job* and it has failed.
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}
The above scenario is common in a shared kubernetes environment, where teams deploy application in different stages. Kubernetes is designed to keep those environment completely separate.

{{% /notice %}}
{{% /notice %}}

None of the pods that make up our e-commerce site run in the Development name space and all the other pods are green, we can safely assume these pods do not affect us, so move on to look at few more things.
