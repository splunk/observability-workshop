---
title: The Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator
weight: 2
---
### This page is still under construction...  This will be a quick guide though the navigator  

## 1.  The Cluster Map

Visit the Infrastructure overview page and select Kubernetes, this will bring you to the Kubernetes Cluster map. Here you find all the Cluster represented  that are sending data to the Observability platform. Your first tasks is to identify your own cluster. It will be named after you ec2 instance node name: `tko-5-X-k3s-cluster` where  `X` is the number of the ec2 assigned to you.
To find you node name look at the prompt of you ec2 cluster. Assuming you are assigned the first ec2 instance  the prompt should show `ubuntu@tko-5-1`

This means your cluster is then named: `tko-5-1-k3s-cluster`

Next, make sure you set/fix the cluster name in the overview bar by selecting the drop down box for clusters and select just your cluster.

## 2. Examine the Kubernetes analyzer (Cluster Map only)

Once you have the selected you cluster, let's investigate the Kubernetes Analyzer the Kubernetes navigator offers.
You can find it by expanding the right hand pane by clicking on the ![sidebar_button](/tko/session-5/docs/images/sidebar-button.png) button. This will show a quick view into the health of you cluster via the Kubernetes Analyzer.
The Analyzer uses AI-driven insights to examine patterns that nodes, pods, or containers could have in common.

{{% alert title="Workshop Question" color="danger" %}}

How many trouble indicators are there?

{{% /alert %}}

## 3.  Nodes view

The next pane is the nodes overview, it will follow the selection you have made in the Maps overview, here you will find the host(s) that make up your cluster. in this case we have the massive number of 1, but at a production cluster ther can be multiple pages of hosts.

{{% alert title="Workshop Question" color="danger" %}}

How much memory and cores does each node have ?

{{% /alert %}}

If you select the line of the node your interested in , you will see that the right pane has change d and is now providing  detailed information for the at specific node.  YOU can expand this to a full screen by clicking on the expand ![expand_button](/tko/session-5/docs/images/expand-button.png) button

_________________

``` bash
kubectl get cm splunk-otel-collector-otel-agent -n splunk -o yaml
```

{{% alert title="Workshop Question" color="danger" %}}

Is the content of **otel-apache.yaml** saved in the ConfigMap for the collector agent?

{{% /alert %}}

More information can be found here : [DNS for Service and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)