---
title: The New Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator v2
weight: 2
--- 
## 1. Cluster vs Workload View

The Kubernetes Navigator offers you two separate use cases to view your Kubernetes data.

* The `K8s nodes` or Admin view is focusing on providing insight into the performance of Clusters, Nodes, Pods & Containers.
* The `K8s workloads` or Developer view is focusing on  providing information in regards to workloads a.k.a. *your deployments*.

You initially select either view depending on your need (You can switch between the view on the fly if required)

## 2 The K8s nodes & cluster Pane

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will offer you a set of Kubernetes services. For this exercise pick the `K8s nodes` pane.

![k8s-cluster-pane](../images/k8s-nodes.png)

The first thing you notice is that the pane indicates how many kubernetes nodes are being monitored for you. The pane also shows a tiny graph for a birds eye view of the load being handled across those Nodes.  Lastly, if there is a alert for one of the Nodes it will be highlighted here too as is shown above.

Click or select on the pane and you will be taken to the `Infrastructure/Kubernetes/K8s nodes` overview pane. Here you will find a  map representation of all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform.

### 2.1 Finding your K8s cluster name

Your first task is to identify and find your own cluster. The cluster will be named after your EC2 instance name: `ws-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of your EC2 instance, assuming you are assigned the 7th EC2 instance the prompt will show

``` bash
ubuntu@ws-5-7 ~ $
```

This means your cluster is named: `ws-5-7-k3s-cluster` make a note as you will need this later in the workshop as a filter.

### 2.2 The K8s Cluster Map

Initially, the cluster detail map will show you all the clusters reporting into your Observability Cloud Org. If an alert has fired for any of the clusters it will be highlighted on the top right, *Marked with a red Stripe*. You can go directly to the alert  by clicking on it and expanding it.

There is also the Breadcrumbs, *Marked with a yellow Arrow*. When you drill down deeper into your cluster, it will show drop down for all levels and you can use it to navigate up and down the cluster tree. (More on this later)

![k8s-cluster-map](../images/nodeswithclusters.png)

In a production environment, you can expect to see different sizes of Clusters with different number of nodes. Each node in a cluster will be shown as individual pale blue square, when you drill down in a node you will see green squares which represent pods as represented below.

![k8s-cluster-map](../images/cluster-node.png)

However in our workshop environment you each have a single node within your Cluster, represented by the large single blue square.

Now, you can find your own Cluster by finding it by name or by filtering by using the field `k8s.cluster.name` in the filter toolbar, *(marked with a blue stripe)*.
You can enter a partial name into the search box such as 'ws-5-7*', to quickly find your Cluster. Also, its is a good idea to switch the default time from the default 3 hours back to 15 minutes.

As soon as you found your cluster and its highlighted, and you are on the highest level you are in the nodes view view, the charts below show information on all the nodes in your cluster.

{{% alert title="Workshop Question" color="success" %}}
How much memory and how many CPU cores does our one node have?
{{% /alert %}}

You can switch to the Cluster View by selecting the *K8s cluster* menu beneath the map view.
Here you can see the charts with the details of your Cluster(s).

### 2.3. The Nodes & Cluster views

Now drill down into your single Node by hovering over the pale blue background, then clicking on either the magnifying glass that appears in the top left corner, or double clicking on the pale blue background, this will take you to the Node level view. Note that the `Breadcrumbs` has grown one level.

You should now be able to see all the Pods and Containers running on your single Node Cluster.

![cluster-detail](../images/cluster-detail.png)

As soon as you select your node in your cluster, you can see the overall performance of that node in the charts below.

{{% alert title="Workshop Question" color="success" %}}
How much pods are running on our node at this point?
{{% /alert %}}

### 2.4. Using the Breadcrumbs

As you selected your Node you may notice that the `Breadcrumbs` above the Map view is changing and showing more options.

With the node selected, hunt in your node map for the pod for the *splunk-otel-collector-agent* pod, and once found, select the *otel-collector* container from that pod.

Your Breadcrumbs above your Map view should look somewhat like this:

![Breadcrumbs](../images/crumbtrail.png)

Note, you can walk back-up in the stack by clicking on the Pod, Node, Cluster & Service links to the level you want to be.

{{% alert title="Workshop Question" color="success" %}}
Which of the levels in the `Breadcrumbs` provides `Related Content` for logs?

**Tip:** You may need to refresh the screen a few time to refresh the log search data in the background.
{{% /alert %}}

## 3. Workloads & Workload Details Pane

You can switch to the `K8s Workloads` view in two ways.

Either go to the **Infrastructure** menu item in the Observability UI and select **Kubernetes** again,and pick the `K8s workloads` pane or simply change the value in the `Service` drop down box in the `Breadcrumbs` from *K8s nodes* to *K8s workloads*

![k8sNode](../images/K8s-Workloads.png) ![k8sToggle](../images/service-toggle.png)

Initially, the workload  view will show you all the workloads that are reported by your clusters into your Observability Cloud Org. If an alert has fired for any of the workloads it will be highlighted on the top right, *Marked with a red Stripe*. You can go directly to the alert  by clicking on it and expanding it.

There is also the Breadcrumbs, *Marked with a yellow Arrow*. When you drill down deeper into your workload, it will show drop down for all levels and you can use it to navigate up and down the workload  tree.

![Workloads](../images/k8s-workload-screen.png)

Now find your own Cluster by filtering  by using the field `k8s.cluster.name` in the filter toolbar, *(marked with a blue stripe)*.
You can enter a partial name into the search box such as 'ws-5-7*', to quickly find your Cluster. Remember, its is a good idea to switch the default time from the default 3 hours back to 15 minutes.

{{% alert title="Workshop Question" color="success" %}}
How many workloads are running on your Cluster?
{{% /alert %}}

### 3.1 Using the Navigator Selection chart

The K8s Selection chart is a common charts used across most of the Navigator's and will offer you a list view of the Services you are looking at. In this case it shows a list of Failed pods grouped by  `k8s.namespace.name`
You will find that this pane is used in various navigators used in this workshop (Workloads & Apache Servers). The way the selection pane works is similar across the navigators. Just the information and selection criteria will match the chosen service.

![k8s-workload-list](../images/workload-selection.png)

First, Select the `File system usage (bytes)` from the **Color by** drop down box *Marked with a green line*,  and Expand the Splunk Workload by clicking on the black triangle before the name splunk *Marked by a black Arrow*  as shown in the example above.

Once you expand a workload, you will note that each workload row has a colored mark at the end of it row. These bars  will change  color according the `color by` option, *Marked by a green line*, these bars use colors to give a visual indication of health and/or usage.

If there are many workloads, you can change the Result per page box *Marked by an orange line*, to increase the list size. (It will also offer pagination if required)

Next, you can change the the list view to a heat map view by selecting either the Heat map or List icon ![heat-map-toggle](../images/heatmaptoggle.png) *(Marked by a purple line).*

This will result in the follow representation:

![k8s-Heat-map](../images/heatmap.png)

This might be a useful view if you have many cluster as they can be grouped together using the group by option *Marked by the green line*. The colors of each node will follow the color by  choice similar to the list view.

The last option, is the Find Outliers based on historical analytics of your clusters based on what is selected in the `color by` box.

Now click on the `Find outliers` box *Marked by a yellow Stripe* and make sure the dialog is set like below:

![k8s-Heat-map](../images/set-find-outliers.png)

{{% alert title="Workshop Question" color="success" %}}
What happened to the Heatmap?
{{% /alert %}}

The `Find outliers` view is very useful when you need to view all or a selection of your workloads (or any service depending on the navigator used) and need  o figure out if something has changed. It will give you a quick insight in items (workloads in our case) that are performing different (both increase or decreased) then usually making it easy to spot a problem.

### 3.2 The Workload Overview pane

The workload over view view give you a quick insight of the status of your deployment, you can see at once if the pods of your deployments are Pending, Running, Failed, Succeeded or in an unknown state.  

![k8s-workload-overview](../images/k8s-workload-overview.png)

* *Running* Means your pods are deployed and in a running state
* *Pending* means waiting to be deployed
* *Succeeded* means the pod has been deployed and completed its job and is finished
* *Failed* means the containers in the pod have run and returned some kind of error
* *Unknown* means Kubernetes doesn't report any of the know states</br>
  (this may be during start or stopping pods for example)

To get filter to a specific Workload, simply click on three dots `...` next to the workload name in the *k8s.workload.name* column  and choose filter from the drop down box. This will add the workload as a filter.

### 3.3 Replicaset overview

The last chart will give you a birds eye view  on how many pods are deployed by Kubernetes for your deployment. In a replicaset you can indicate the min, max and desired number of pods you wish to run as part the deployment.

{{% alert title="Workshop Question" color="success" %}}
What is the desired number of pods for the `splunk-otel-collector-k8s-cluster-reciever` replicaset?
{{% /alert %}}

### 3.4. Drilling down into your Workload

To bring up details of a workload in the Kubernetes Navigator you either need to expand  a namespace  in the list mode or clicking on a  workload square in the  heatmap view.

In the heatmap mode, double click on the square for the `splunk-otel-collector-agent` workload in the *splunk* namespace.

![workload-expand](../images/workload-expand.png)

In the list view you can click on the link that appears when expanding a namespace.

This will bring you to the workload detail page where you get more detail about the health and performance of your workload & Pods Detail.

{{% alert title="Workshop Question" color="success" %}}
What are the names of the container(s) in the **CPU resources (cpu units)** chart for the `splunk-otel-collector-agent`?
{{% /alert %}}

## 4. Pivot Sidebar

Later in the workshop you will deploy a Apache server into you cluster and this will cause the pivot bar to appear.
As soon as any metric that is displayed in a Navigator is flowing into your observability org  the system will add that service to the pivot bar.

The pivot bar will expand and a link to the discovered service will be added.

![pivotbar](../images/pivotbar.png)

This will allow for easy switching between navigators, teh same applies for your apache server instance it will have a pivot bar to get back to Kubernetes.
