---
title: Infrastructure Exercise - Part 3
linkTitle: Part 3
weight: 3
time: 10 minutes
---

Let's look at some other parts of the UI like the *Information Pane* on the right of the navigator or the *Related Content Pane* at the bottom.

First, let's look at the *Information Pane*, this pane provides alert and detected services information and the metadata related to the object you're looking at.

![info pane](../images/k8s-info-pane.png)

Meta Data is sent along with the metrics and is very useful for identifying trends when looking into issues. An example could be a pod failing when deployed on a specific Operating System.

{{% notice title="Exercise" style="green" icon="running" %}}

* Can you identify the Operating System and Architecture of the node from the metadata?

{{% /notice %}}

As we have seen in the previous exercise, these fields are very useful for filtering the view in charts and Navigators down to a specific subset of metrics we are interested in.

Another feature in the UI is **Related content**.

{{% notice title="Related Content" style="info" %}}

The Splunk Observability User Interface will attempt to show you additional information that is related to what you're actively looking at.
A good example of this is the Kubernetes Navigator showing you related Content tiles in the information Pane for the services found running on this node.

{{% /notice %}}

In the **Information Pane**, you should see two tiles for services detected, the two databases used by our e-commerce application. Let's use this **Related Content**.

{{% notice title="Exercise" style="green" icon="running" %}}

* First, make sure you no longer have a filter for the development namespace active. (Simply click on the **x** to remove it from the Filter Pane) as there are no databases in the Development Namespace.
* Hoover on the **Redis** tile, and click on the {{% button style="blue" %}}Goto all my Redis instances{{% /button %}} button
* The Navigator view should change to the overall Redis instances view.
* Select the the instance running on your cluster. (Click on the blue link, named **redis-[the name of your workshop]**, in the Redis Instances pane).
* We should now see just the information for your Redis Instance & there should also be an **Information Pane**.
* Again we see Meta Data, but we also see that UI is showing in the **Related Content** tiles that this Redis Server runs in a Container running on Kubernetes.
* Let's verify that by clicking on the **Kubernetes** Tile.
* We should be back in the Kubernetes Navigator, at the container level.
* Confirm that the names of our cluster and node are all visible at the top of the page and we are back looking at our K8s Cluster, where we started.

{{% /notice %}}

This completes the tour of Splunk Observability Cloud. Let's go and look at our e-commerce site and do some shopping.
