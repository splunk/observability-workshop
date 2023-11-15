---
title: Splunk Infrastructure exercise with the Kubernetes Navigator
linkTitle: Exercise part 3
description: This section of the workshop provides an exercise using Splunk infra monitoring based on the Kubernetes Navigator.
weight: 20
---

{{% button icon="clock" %}}10 minutes{{% /button %}}

Lets look at some other parts of th Ui like the *Information Pane* on the right of the navigator or the *Related Content Pane* at the bottom

First lets look at the *Information Pane*, this pane provides alert information, info on detected services and shows the Meta Data related to the object you're looking at.

![info pane](../images/k8s-info-pane.png?width=15vw)

Meta Data is send along wth the metrics an are very useful to identify trends when identifying issues. An example could be a pod failing when deployed on a specific Operating System.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Can you identify what the Operating System and Architecture is what our node is running using the Meta Data?

{{% /notice %}}

As we have seen in the previous exercise, these fields are very useful to filter the view in charts and Navigators down to a specific subset of metrics we are interested in.

An other feature of the Splunk Observability UI, is what we call *Related content*.  

{{% notice title=" Related Content" style="info" %}}
The Splunk Observability User Interface will attempt to show you additional information that is related to what you're actively looking at.  
A good example of this is the Kubernetes Navigator showing you related Content tiles in the information Pane for the services found running on this node.

{{% /notice %}}

In the *Information pane*You should see two tiles for services detected, the two databases used by our e-commerce application. Let's use this *Related Content*.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First make sure you no longer have a filter for the development namespace active. (Simply click on the **x** behind it to remove it from the Filter Pane) as there are no databases in the Development Name space.
* Hoover on the *Redis* tile, and click on the {{% button style="blue" %}}Goto all my Redis instances{{% /button %}} button
* The Navigator view should change to the overall Redis instances view.
* Select the the instance running on your cluster. (Click on the blue link, named *redis-[the name of your workshop]*, in the Redis Instances pane).
* We should now see just the information for your Redis Instance & there should also be an *Information Pane*.
* Again we see Meta Data, but we also see that UI is showing in the *Related Content* tiles that this Redis Server runs in a Container running on Kubernetes.
* Let's verify that by double clicking on the *Kubernetes* Tile.
* We should be back in the Kubernetes Navigator, at the container level.
* confirm that the name of the cluster, node are all visible at the top of the page and we are back looking at our cluster.

{{% /notice %}}

This completes the tour of the Splunk Observability SuiteUI. Let's go an look at our E-commerce site and do some shopping in the next page.
