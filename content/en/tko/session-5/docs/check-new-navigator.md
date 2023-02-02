---
title: The New Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator v2
weight: 2
--- 
## 1. The k8s nodes & cluster Pane

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will offer you a set of Kubernetes services. For this exercise pick the `K8s nodes` pane.

![k8s-cluster-pane](../images/k8s-nodes.png)

The first thing you notice is that the pane indicates how many kubernetes nodes are being monitored for you. The pane also shows a tiny graph for a birds eye view of the load being handled across those Nodes.  Lastly, if there is a alert for one of the Nodes it will be highlighted here too as is shown above.

Click or select on the pane and you will be taken to the `Infrastructure/Kubernetes/K8s nodes` overview pane. Here you will find a  map representation of all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform.

### 1.1 Finding your K8s cluster name

Your first task is to identify and find your own cluster. The cluster will be named after your EC2 instance name: `ws-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of your EC2 instance, assuming you are assigned the 7th EC2 instance the prompt will show

``` bash
ubuntu@ws-5-7 ~ $
```

This means your cluster is named: `ws-5-7-k3s-cluster`  make a note as you will need this later in the workshop as a filter.

### 1.2 The k8s Cluster Map

Initially, the cluster detail map will show you all the clusters reporting into your Observability Cloud Org. If an alert has fired for any of the clusters it will be highlighted on the top right like shown below. (You can go directly to the alert from there):

![k8s-cluster-map](../images/nodeswithclusters.png)

In a production environment you can expect to see different sizes of Clusters with different number of nodes. Each node in a cluster will be shown as individual pale blue square, when you drill down in a node you will see green squares which represent pods as represented below.

![k8s-cluster-map](../images/cluster-node.png)

However in our workshop environment you each have a single node within your Cluster, represented by the large single blue square.

Now,you can find your own Cluster by finding it by name or by filtering by using the field `k8s.cluster.name` in the filter toolbar, *(marked with a blue stripe)*.
You can enter a partial name into the search box such as 'ws-5-7*', to quickly find your Cluster. Also, its is a good idea to switch the default time from the default 3 hours back to 15 minutes.

As soon as you found your cluster and its highlighted, and you are on the highest level you are in the nodes view view, the charts below show information all the nodes in your cluster.

{{% alert title="Workshop Question" color="success" %}}
How much memory and how many CPU cores does our one node have?
{{% /alert %}}

You can switch to the Cluster View by selecting the *K8s cluster* menu beneath the map view.
Here you can see  the details of you cluster or Cluster.

### 1.3. The Nodes & Cluster views

Now drill down into your single Node by hovering over the pale blue background, then clicking on either the magnifying glass that appears in the top left corner, or double clicking on the pale blue background, this will take you to the Node level view.

You should now be able to see all the Pods and Containers running on your single Node Cluster.

![cluster-detail](../images/cluster-detail.png)

As soon as you select your node in your cluster, you can see the overall performance of that node

### 1.4. Using the Crumb Trail

As you selected your Node you may notice that the `Crumb Trail` above the Map view is changing and showing more options.

With the node selected, hunt in your node map for the pod for the *splunk-otel-collector-agent* pod, and once found, select the *otel-collector* container from that pod.

Your Crumb Trail above your Map view should look somewhat like this:

![crumb-trail](../images/crumbtrail.png)

Note, you can walk back-up in the stack by clicking on the Pod, Node, Cluster & Service links to the level you want to be.now click on the Node link in the Crumb Trail.

{{% alert title="Workshop Question" color="success" %}}
Witch of the levels will provides the `Related Content` bar for your logs?
{{% /alert %}}

Now select the `Node` link in the Crumb Trail to get to your node view. 

{{% alert title="Workshop Question" color="success" %}}
How much pods are running on our node at this point?
{{% /alert %}}

## 2. Workloads & Workload Details Tabs

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this again will offer you a set of Kubernetes services. For this exercise pick the `K8s workloads` pane.

![k8sNode](../images/K8s-Workloads.png)





------

## halted here for today

You should now be able to see all the Pods and Containers running on your single Node Cluster...

![cluster-detail](../images/cluster-detail.png)

But, more importantly, the *side panel* should have also switched to the Info Tab and is now showing lots of contextual information about the Node.

![side-panel-node.png](../images/side-panel-node.png)

There are various Panes showing details on the Properties of the Node, and all the various Workloads running on it, even though we are still on the 'Map' tab within Kubernetes Navigator.

At the top of the side panel, click on the Expand icon ![expand-sidebar.png](../images/expand-sidebar.png) which takes you to the full screen tab of the currently displayed resource, which in this case is a Node, so we end up on the Node Details Tab.

Node Details shows you lots of great detail about what is happening on this Node, with charts for total CPU Usage, Memory Usage, Network traffic etc for all the Pods running on the Node with a list of any Events just to the right of these Charts.

You also have scrollable table views of both the Workloads and Containers running on the Node.  Clicking on any of the names in the tables will reopen the side panel with the appropriate panes for either Workloads or Containers.  Each of these can then also be expanded just like you did with the Node side panel, by clicking the expand button ![expand-sidebar.png](../images/expand-sidebar.png)

## 3. Workloads & Workload Details Tabs

Assuming you have been able to answer the question about the Node CPU cores, you will now need to switch to the Workloads tab on the top toolbar.  The Workloads tab details all the workloads that are deployed within your cluster.

This table provides lots of valuable insights into the state of your workloads, and will show you if any of them are not in their desired state.

The default view has no Grouping applied but experiment with the various Group By options to see how the table changes.  Note how you can also use the various fields in the top toolbar to filter the data displayed, this would be essential in a large environment with hundreds or even thousands of different Workloads.

{{% alert title="Workshop Question" color="success" %}}
What type is the `splunk-otel-collector-agent` workload, and what is its desired configuration?
{{% /alert %}}

To get more detail on a specific Workload, simply click on its name in the Workload column (we assume you have the 'splunk-otel-collector-agent' workload selected), this will open the side panel, then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Workload Detail Tab.

---

### 1.2 Using the K8s Selection Pane

The K8s Selection Pane is a common pane used across most of the Navigator's and will offer you a list view of the  Services you are looking at. In this case it shows a list of all the active K8s Clusters.

You will find that this pane is used in all the navigators used in this workshop (Cluster's, Nodes, Workloads & Apache Servers). The way the selection pane works is similar across the navigators. Just the information and selection criteria will match the chosen service.

![k8s-cluster-list](../images/navi-selection-pane.png)

First, Select the `Memory usage (bytes)` from the **Color by** drop down box *Marked with a green line*, as shown in the example above.


If there are many clusters, you can change the Result per page box *Marked by an orange line*, to increase the list size.

You will note that each cluster row has a colored mark at the end of each row. These will change according the `color by` option, *Marked by a green line*,thses colored bars are used to give a visual indication of health and/or usage.

These are the possible color by options for the k8s Cluster view:

![k8s-colorby-list](../images/Infk8sColorBy.png)

Next, you can change the the list view to a heat map view by selecting either the Heat map or List icon ![heat-map-toggle](../images/heatmaptoggle.png) *(Marked by a purple line).*

This will result in the follow representation:

![k8s-Heat-map](../images/heatmap.gif)

This might be a useful view if you have many cluster as they can be grouped together using the group by option *Marked by the green line* . The colors of each node will follow the color by  choice similar to the list view.

The last option, is the Find Outliers based on historical analytics of your clusters based on what is selected in the `colored by` box.  

This view is better used when you view all or a selection of you cluster (or any other navigator view). It will give you a quick insight which of your clusters are behaving differently than  they do normally and may need further investigation.
You may not see relevant info, the clusters in this workshop are short lived and may haven't send enough meaningful data for the historical analytics to detect deviations.

{{% alert title="Workshop Question" color="success" %}}
Find your Cluster in the Observability Kubernetes Navigator, and identify the number of containers that are running at this point.

**Tip:** You may need to switch  the Color By option to containers and refresh the screen a few times until the cluster data is correlated in the background. Also, it is recommended to set the time frame to be `15m` (down from `3h` which is default).
{{% /alert %}}

---

### 3.1 Workload Detail tab

Here you will get the general info about your Workload, the CPU and Memory the Containers are consuming, the Pods and their Phase, details of any Events, and finally a list of Pods related to this Workload.

As with the other Kubernetes Navigator views clicking on the name of a Pod within the table view will load the Side Panel with details about that resource, allowing you to 'click through' to these resources.  Select any of the listed Pods, then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Pod Detail Tab.

{{% alert title="Workshop Question" color="success" %}}
How many containers does the `splunk-otel-collector-agent` Pod contain?
{{% /alert %}}

## 4. Pod Detail & Container Details Tabs

The last two Tabs that make up the Kubernetes Navigator are Pod Detail and Container Detail. The Pod Detail view will show you the Pod Properties, CPU, Memory and Network usage along with any events relevant to the Pod.

Clicking through to the Container Detail Tab, you should know how to do this by now, but just to play safe, select one of the Containers in the list then click the expand button ![expand-sidebar.png](../images/expand-sidebar.png) to navigate to the Container Detail Tab.  

If you navigated straight to the Container Detail Tab by simply clicking on the Tab, try using the Container ID drop down to select a container, now you will see the benefit of 'clicking through' to get to the desired Container!

You can now see the details for the Selected Container, with the Container Properties pane offering lots of detail on its configuration.
