---
title: The Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator
weight: 2
---

## 1. The Cluster Map

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will bring you to the Kubernetes Cluster Map.

Here you will find all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform. Your first task is to identify your own cluster.

The cluster will be named after your EC2 instance name: `ws-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of you EC2 instance, assuming you are assigned the 7th ec2 instance the prompt will show

``` bash
ubuntu@ws-5-7 ~ $
```

This means your cluster is named: `ws-5-7-k3s-cluster`

Use the Cluster drop down on the top toolbar to filter the view to only show your Cluster, you can enter a partial name into the search box such as 'ws-5-7' to quickly find your allocated Cluster.

## 2. Examine the Kubernetes analyzer (Cluster Map only)

With your Cluster selected in the Cluster drop down, open the Kubernetes Cluster Analyzer, you can find it by expanding the right hand pane by clicking on the ![sidebar_button](../images/sidebar-button.png) button in the top right corner. The Analyzer provides a quick view into the health of your cluster.

![cluster-analyzer](../images/cluster-analyzer.png)

In our little cluster we have not yet had enough time or data to do more than highlight a condition detected like a pod restart. Over time, the system will show relationships and patterns between objects. You will find that as you drill down into your Clusters resources, the Analyzer adjusts what it displays depending on the chosen resource.

{{% alert title="Workshop Question" color="success" %}}
How many trouble indicators are there in your Cluster?
{{% /alert %}}

## 3.  Nodes & Node Details Tabs

In a production environment you would expect to see multiple Nodes within a Cluster which would now all be visible and shown as individual pale blue squares, each containing green squares which represent pods, however in our workshop environment you each have a single node within your Cluster, represented by the large single blue square.

Drill down into the single Node by hovering over the pale blue background, then clicking on either the magnifying glass that appears in the top left corner, or double clicking on the pale blue background, this will take you to the Node level view.

![cluster](../images/cluster.png)

You should now be able to see all the Pods and Containers running on your single Node Cluster...

![cluster-detail](../images/cluster-detail.png)

but more importantly, the 'side panel' should have also switched to the Info Tab and is now showing lots of contextual information about the Node.

![side-panel-node.png](../images/side-panel-node.png)

There are various Panes showing details on the Properties of the Node, and all the various Workloads running on it, even though we are still on the 'Map' tab within Kubernetes Navigator.

---

At the top of the side panel, click on the Expand icon ![expand-sidebar.png](../images/expand-sidebar.png) which takes you to the full screen tab of the currently displayed resource, which in this case is a Node, so we end up on the Node Details Tab.

Node Details shows you lots of great detail about what is happening on this Node, with charts for total CPU Usage, Mem Usage, Network traffic etc for all the Pods running on the Node with a list of any Events just to the right of these Charts.

You also have scrollable table views of both the Workloads and Containers running on the Node.  Clicking on any of the names in the tables will reopen the side panel with the appropriate panes for either Workloads or Containers.  Each of these can then also be expanded just like you did with the Node side panel, by clicking the expand button ![expand-sidebar.png](../images/expand-sidebar.png)

{{% alert title="Workshop Question" color="success" %}}
How much memory and how many CPU cores does our one node have?
{{% /alert %}}

## 4. Workloads & Workload Details Tabs

Assuming you have been able to answer the question about the Node CPU cores, you will now need to switch to the Workloads tab on the top toolbar.  The Workloads tab details all the workloads that are deployed within your cluster.

This table provides lots of valuable insights into the state of your workloads, and will show you if any of them are not in their desired state.

The default view has no Grouping applied but experiment with the various Group By options to see how the table changes.  Note how you can also use the various fields in the top toolbar to filter the data displayed, this would be essential in a large environment with hundreds or even thousands of different Workloads.

{{% alert title="Workshop Question" color="success" %}}
What type is the `splunk-otel-collector-agent` workload, and what is its desired configuration?
{{% /alert %}}

To get more detail on a specific Workload, simply click on its name in the Workload column (we assume you have the 'splunk-otel-collector-agent' workload selected), this will open the side panel, then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Workload Detail Tab.

---

### Workload Detail tab

Here you will get the general info about your Workload, the CPU and Memory the Containers are consuming, the Pods and their Phase, details of any Events, and finally a list of Pods related to this Workload.

As with the other Kubernetes Navigator views clicking on the name of a Pod within the table view will load the Side Panel with details about that resource, allowing you to 'click through' to these resources.  Select any of the listed Pods, then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Pod Detail Tab.

{{% alert title="Workshop Question" color="success" %}}
How many containers does the `splunk-otel-collector-agent` Pod contain?
{{% /alert %}}

## 5. Pod Detail & Container Details Tabs

The last two Tabs that make up the Kubernetes Navigator are Pod Detail and Container Detail.

The Pod Detail view will show you the Pod Properties, CPU, Memory and Network usage along with any events relevant to the Pod.

Clicking through to the Container Detail Tab, you should know how to do this by now, but just to play safe, select one of the Containers in the list then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Container Detail Tab.  

If you navigated straight to the Container Detail Tab by simply clicking on the Tab, try using the Container ID drop down to select a container, now you will see the benefit of 'clicking through' to get to the desired Container!

You can now see the details for the Selected Container, with the Container Properties pane offering lots of detail on its configuration.