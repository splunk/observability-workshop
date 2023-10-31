---
title: Splunk Infrastructure exercise with the Kubernetes Navigator
linkTitle: Exercise part 2
description: This section of the workshop provides an exercise using Splunk infra monitoring based on the Kubernetes Navigator.
weight: 10
---

{{% button icon="clock" %}}8 minutes{{% /button %}}

This is the second section, of the infra monitoring exercise,
You should now have your single cluster visible.

![Alt Cluster](../images/k8s-cluster.png?width=40vw)

In the Kubernetes Navigator, your cluster is represented by the square with the black line, it will contain one or more  blue squares representing the node(s), each of them wil contain one or more colored boxes  that represent pods.
and as you can guess, *Green* means healthy & *Red* means that there is a problem.

Given there are two red boxes, lets see what is going on and if this will affect our E-commerce site.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First, set the time window we are working with to  th last 15 minutes. You do this by using the drop down in the Filter pane ![time-window](../images/time-window.png?classes=inline) to *the last 15 minutes*.
* The Cluster Metric charts you can see below the cluster representation,  provide information on your cluster, like the memory consumption and the number of pods per node. none of these will explain why there are red pods.
* Let's check if the Spunk Kubernetes Analyzer can tell us something more useful, so click on **K8s analyzer**.

* The Spunk Kubernetes Analyzer is a smart process that runs in the background in the Splunk Observability Suite,  designed to detect relations between anomalies.  
It should have detected that the two Red pods are similar and come from the same name space.
* Can you find what name space?  (hint, look for *k8s.namespace.name*)

![Analyser result](../images/k8s-analyser-result.png?width=25vw)

* Click on the name of namespace, this should add a filter to the filter pane, *k8s.namespace.name=development
* This filter will highlight all pods that are part of the development namespace. As you can see only the two *"bad"* pods are highlighted This is a quick indication that our e-commerce site is not affected by these error pods. 

* To confirm this click on **K8s node**. This will provide node metrics, and you can see that there are two pods in the development name space,  and in the node workloads chart, you should be able to see that the *test=job* is in a failed state.
* If you now remove  the filter for the *k8s.namespace.space* from the filter Pane, the Node workload chart will show you all the workload on this node now, and again only the *test-job* in *development* has failed.

The above scenario is common in a shared kubernetes environment, where teams deploy application in different stages. Kubernetes is designed to keep those environment completely separate.

{{% /notice %}}

We can safely assume these pods do not affect us, so move on to look at few more things.
