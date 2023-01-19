---
title: The Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator
weight: 2
---
### This page is still under construction...  This will be a quick guide though the navigator  

## 1. The Cluster Map

Goto the **Infrastructure** page and select **Kubernetes**, this will bring you to the Kubernetes Cluster Map.

Here you will find all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform. Your first task is to identify your own cluster.

The cluster will be named after your EC2 instance name: `tko-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of you EC2 instance, assuming you are assigned the first ec2 instance the prompt will show

``` bash
ubuntu@tko-5-1 ~ $
```

This means your cluster is named: `tko-5-1-k3s-cluster`

Next, make sure you set/fix the cluster name in the overview bar by selecting the drop down box for clusters and select just your cluster.

## 2. Examine the Kubernetes analyzer (Cluster Map only)

Once you have the selected you cluster, investigate the Kubernetes Analyzer the Kubernetes Navigator offers.

You can find it by expanding the right hand pane by clicking on the ![sidebar_button](/tko/session-5/docs/images/sidebar-button.png) button.

This will show a quick view into the health of you cluster via the Kubernetes Analyzer. The Analyzer uses AI-driven insights to examine patterns that nodes, pods, or containers have in common.

{{% alert title="Workshop Question" color="danger" %}}

How many trouble indicators are there?

{{% /alert %}}

## 3. Nodes view

The next pane is the nodes overview, it will follow the selection you have made in the Maps overview, here you will find the host(s) that make up your cluster. in this case we have the massive number of 1, but at a production cluster ther can be multiple pages of hosts.

{{% alert title="Workshop Question" color="danger" %}}

How much memory and cores does each node have ?

{{% /alert %}}

If you select the line of the node your interested in , you will see that the right pane has change d and is now providing  detailed information for the at specific node.  YOU can expand this to a full screen by clicking on the expand ![expand_button](/tko/session-5/docs/images/expand-button.png) button

``` bash
kubectl get cm splunk-otel-collector-otel-agent -n splunk -o yaml
```

{{% alert title="Workshop Question" color="danger" %}}

Is the content of **otel-apache.yaml** saved in the ConfigMap for the collector agent?

{{% /alert %}}

More information can be found here : [DNS for Service and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
