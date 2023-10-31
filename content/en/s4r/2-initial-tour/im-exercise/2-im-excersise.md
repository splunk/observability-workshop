---
title: Splunk Infrastructure exercise with the Kubernetes Navigator
linkTitle: Exercise part 3
description: This section of the workshop provides an exercise using Splunk infra monitoring based on the Kubernetes Navigator.
weight: 20
---

{{% button icon="clock" %}}6 minutes{{% /button %}}

We are now going to work with the Information Pane on the right of the navigator.

![info pane](../images/k8s-info-pane.png?width=20vw)

This pane provides alert information, info on detected services and shows meta data related to the object your looking at, in this case a kubernetes node running on an ec2 instance in AWS.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

Meta Data is send along wth the metrics an are very useful to identify trends when identifying issues. An example could be a pod failing when deployed on a specific Operating system.

* Can you identify what the Operating System and Architecture is what our node is running using the Meta Data?

We can these fields to filter in charts and/or detectors to drill down to a specific subset of metrics we are interested in.

{{% /notice %}}

An other feature of the Splunk Observability UI, is what we call *Related content*.  

The Splunk Observability UI will try to show you links to information that is related to the topic you are actively looking at. A good example of this are the services  running on this node.

Let's use this *related content*:
{{% notice title="Info" style="green" title="Exercise" icon="running" %}}
You should have two services detected, *Mysql* & *Redis*, the two databases used by our e-commerce application.

* Hoover on the *Mysql* tile,
{{% /notice %}}

This completes the  quick tour of the Splunk Observability SuiteUI. Let's go an look at our E-commerce site and do some shopping in the next page.
