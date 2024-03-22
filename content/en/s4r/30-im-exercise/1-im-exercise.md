---
title: Infrastructure Exercise - Part 1
linkTitle: Part 1
weight: 1
time: 5 minutes
---

This is the first section of our optimal Kubernetes Navigator exercise. Below is some high-level information regarding Kubernetes, just in case you're not familiar with it.

{{% notice title=" Kubernetes Terminology" style="info" %}}
K8s, short for Kubernetes, is an open-source container orchestration platform. It manages the deployment, scaling, and maintenance of containerized applications, and we use it in this workshop to host our e-commerce application

**Some terminology:**

* A Kubernetes cluster is a group of machines, called nodes, that work together to run containerized applications.
* Nodes are individual servers or VMs in the cluster. Typically, you would have several nodes in a cluster but you may have just one node, just like in this workshop.
* Pods are the smallest deployable units in Kubernetes, representing one or more containers that share the same network and storage, enabling efficient application scaling and management
* Applications are a collection of one or more Pods interacting together to provide a service.
* Namespaces help you keep your applications organized and separate within the cluster, by providing a logical separation for multiple teams or projects within a cluster.
* Workloads are like a task list and  define how many instances of your application should run, how they should be created, and how they should respond to failures
{{% /notice %}}

Please select the **K8s nodes** tile from the Tile pane if you have not yet done so.
(Select **Kubernetes** as your Technology). This will bring you to the Kubernetes Navigator Page.

![Kubernetes](../images/im-kubernetes.png)

The screenshot above shows the main part of the Kubernetes navigator. It will show all the clusters & their nodes that send metrics to Splunk Observability Cloud, and the first row of charts that show cluster-based Metrics. In the workshop, you will mostly see single-node Kubernetes clusters.

Before we dive deeper, let's make sure we are looking at our cluster.

{{% notice title="Exercise" style="green" icon="running" %}}

* First, use the ![k8s filter](../images/k8s-add-filter.png?classes=inline) option to pick your cluster.
* This can be done by selecting `k8s.cluster.name` from the filter drop-down box.
* You then can start typing the name of your cluster, (as provided by your instructor). The name should also appear in the drop-down values. Select yours and make sure just the one for your workshop is highlighted with a ![blue tick](../images/select-checkmark.png?classes=inline&width=30px).
* Click the {{% button style="blue"  %}} Apply Filter  {{% /button %}} button to focus on our Cluster
* We now should have a single cluster visible.
{{% /notice %}}

Let's move on to the next page of this exercise and look at your cluster in detail.
