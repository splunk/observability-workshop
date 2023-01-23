---
title: The Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator
weight: 2
---

## 1. The Cluster Map

Goto the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will bring you to the Kubernetes Cluster Map.

Here you will find all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform. Your first task is to identify your own cluster.

The cluster will be named after your EC2 instance name: `tko-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of you EC2 instance, assuming you are assigned the first ec2 instance the prompt will show

``` bash
ubuntu@tko-5-1 ~ $
```

This means your cluster is named: `tko-5-1-k3s-cluster`

Next, make sure you set/fix the cluster name in the overview bar by selecting the drop down box for clusters and select just your cluster.

In the map view you can drill down by selecting either the whole cluster, a node, a pod or a container in the map to get  a quick view of the selected object on the right.

## 2. Examine the Kubernetes analyzer (Cluster Map only)

If you have drilled down into you cluster, reselect you own cluster by removing it from the drop down box, then selecting it again. Now lets investigate the Kubernetes Analyzer the Kubernetes Navigator offers.

You can find it by expanding the right hand pane by clicking on the ![sidebar_button](../images/sidebar-button.png) button.

This will show a quick view into the health of you cluster via the Kubernetes Analyzer. The Analyzer uses AI-driven insights to examine patterns that nodes, pods, or containers have in common.

In our little cluster we have not yet had enough time or data to do more then highlight a condition detected like a pod restart detected. Over time, the system will show relations and patterns between between objects.

For the sake of this workshop, you can still use the detected condition to select the pane to do start an investigation.

Start with the workload pane for pods and container information and use the Nodes pane for conditions related to Node related conditions.

{{% alert title="Workshop Question" color="danger" %}}
How many trouble indicators are there if you are looking at the Cluster?
{{% /alert %}}

You find if you drill down into you cluster on the map, you also use  the analyzer views at each level.

## 3.  Nodes & Node Details view

The next panes are the nodes overview and the Node Details view, The Node view will follow the selection you have made in the Maps overview. In the Nodes view you will find a list of the hosts that make up your cluster. In the case  of our workshop cluster we have the massive number of 1, but at a regular cluster there will be multiple  and large production clusters can have multiple pages of hosts. This page will allow you to see at a glance and optional a scroll how your nodes are doing.

{{% alert title="Workshop Question" color="danger" %}}
How much memory and cores does our one node have?
{{% /alert %}}

---

{{% alert title="Note" color="info" %}}
If you click on a line in any of the table in the navigator you will see that the right pane will change and will provide information for that specific object.
{{% /alert %}}

---

Select the Node and get the detailed view of the node in the right hand pane.

The side bar also contains a list of workloads and containers running on the Node. Last but, not least there is a section that will show any node events that have occurred.

You can expand this to a full screen by clicking on the expand ![expand_button](../images/expand-button.png) button.

If you do this you will switch to the Node Details view which is a full screen representation of the information in the side bar in the Node view.

This view is useful if you wish to search for workloads and/or specific containers for further examination. The side bar will change to a quick view on workloads or container depending if you clicked on a workload or container line in the tables.

## 4. Workloads & Workload Details view

The next panes are the nodes overview and the Node Details view.  The workloads view shows you all teh workloads that are deployed on your cluster. It will show type, name space it it is and the desired and current Pod configuration for your workload.

{{% alert title="Workshop Question" color="danger" %}}
What type is the `splunk-otel-collector-agent` workload, and what is its desired configuration?
{{% /alert %}}

You can select a workload by double clicking on its name, this will expand the right side pane again, this time with the Details of the selected workload.

Here you will get the general info of your workload, the containers CPU and memory% in use, the number of pods per phase. Again you have a view on the latest Workload events and a list of  pods that make up your workload.

The list of pods allows you to drill deeper into the Pods view.

Again you expand this view to a full screen by clicking on the expand ![expand_button](../images/expand-button.png) button.

Expanding the side bar will bring you to the Workload details view. This provides the same data as the side bar but in full page view with is useful if you try to see what is going on with a specific workload deployment.

This will also give a more detailed view on the behavior of the container(s) in your workload, again you can drill down to the container view by clicking on the name of one of you containers from the workload.

## 5. Pod Detail & Container Details view

The last two panes that make up the Kubernetes Navigator are the pod detail and the Container details.

The Container detail view is best used by drilling down from either the Pod detail or the workload detail, as you require a container id to single out a specific container. However it provides in a full screen view all the properties and memory and cpu usage in detail for the selected container. This will allow you to go back in time by the slider under each chart to find potential misbehavior for the selected pod (or you can use the time picker on top).

The Pod Detail view will show you the Pod properties and  CPU, Memory and Network usage along with any events relevant to the pod.

It has a list of all the containers in the selected pod, and here you can see at a glance how healthy you containers are and how they uses its resources like memory and CPU allocations.

{{% alert title="Workshop Question" color="danger" %}}
Select the `splunk-otel-collector-agent` Pod from the drop down, how many containers does it contain?
{{% /alert %}}
