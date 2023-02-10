---
title: The New Kubernetes Navigator
linkTitle: Kubernetes Navigator v2
weight: 2
--- 
## 1. Cluster vs Workload View

The Kubernetes Navigator offers you two separate use cases to view your Kubernetes data.

* The `K8s nodes` or Admin view is focusing on providing insight into the performance of Clusters, Nodes, Pods & Containers.
* The `K8s workloads` or Developer view is focusing on  providing information in regards to workloads a.k.a. *your deployments*.

You initially select either view depending on your need. (You can switch between the view on the fly if required)

## 2 The K8s nodes & cluster Pane

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will offer you a set of Kubernetes services. For this exercise, pick the `K8s nodes` pane.

![k8s-cluster-pane](../images/k8s-nodes.png)

The first thing you notice is that the pane indicates how many kubernetes nodes are being monitored for you. The pane also shows a tiny graph giving you a bird's eye view of the load being handled across those Nodes. Also, if there are any alerts for one of the nodes, you will see a small alert indicator as shown in the image above.

Click on the K8s Nodes pane and you will be taken to the `Infrastructure/Kubernetes/K8s nodes` overview pane. Here you will find a map representation of all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform.

### 2.1 Finding your K8s cluster name

Your first task is to identify and find your own cluster. The cluster will be named after your EC2 instance name: `ws-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name, look at the prompt of your EC2 instance. For example, if you are assigned the 7th EC2 instance, the prompt will show:

``` bash
ubuntu@ws-5-7 ~ $
```

This means your cluster is named: `ws-5-7-k3s-cluster`. Please make a note of your cluster name as you will need this later in the workshop for filtering.

### 2.2 The K8s Cluster Map

Initially, the cluster detail map will show you all the clusters reporting into your Observability Cloud Org. If an alert has fired for any of the clusters, it will be highlighted on the top right, *as marked with a red stripe in the image below*. You can go directly to the alert by clicking on it to expand it.

Beneath the filters, you will find the Breadcrumbs feature, *as marked with a yellow arrow in the image below*. When you drill down deeper into your cluster, the breadcrumbs will show drop downs for all levels and you can use it to navigate up and down the cluster tree. (More on this later!)

![k8s-cluster-map](../images/nodeswithclusters.png)

In a production environment, you can expect to see different sizes of Clusters with different number of nodes. Each node in a cluster will be shown as an individual pale blue square. When you drill down into a node, you will see green squares which represent pods as seen in the image below:

![k8s-cluster-map](../images/cluster-node.png)

In our workshop environment, however, you each have a single node within your cluster, represented by a large, single, blue square.

Let's find your own Cluster using the filter feature. First, let's switch the time filter in the upper-left corner from the default of 3 hours to the past 15 minutes. Then, click the *Add Filters* button and begin typing `k8s.cluster.name` in the filter toolbar (the type-ahead feature will help you!) For the cluster name, you can enter a partial name into the search box, such as 'ws-5-7*', to quickly find your cluster.

As soon as you find your cluster and it's highlighted, the charts below it show information on all the nodes in your cluster.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How much memory and how many CPU cores does our one node have?
{{% /notice %}}

You can switch to the Cluster View by selecting the *K8s cluster* tab just beneath the map view. Here you will see charts with details of your cluster(s).

### 2.3. The Nodes & Cluster views

Now, drill down into your single Node by hovering over the pale blue background, then clicking on either the magnifying glass that appears in the top left corner, or double clicking on the pale blue background. This will take you to the Node level view. Note that the `Breadcrumbs` has grown one level.

You should now be able to see all the Pods and Containers running on your single Node Cluster.

![cluster-detail](../images/cluster-detail.png)

As soon as you select your node in your cluster, you can see the overall performance of that node in the charts beneath the selected node.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How many pods are running on your node at this point?
{{% /notice %}}

### 2.4. Using the Breadcrumbs

As you selected your Node, you may notice that the `Breadcrumbs` above the Map view is changing and showing more options.

With the node selected, hunt in your node map for the *splunk-otel-collector-agent* pod, and once found, select the *otel-collector* container from that pod.

Your Breadcrumbs above your Map view should look somewhat like this:

![Breadcrumbs](../images/crumbtrail.png)

Note, you can walk back-up in the stack by clicking on the Pod, Node, Cluster & Service links.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Which of the levels in the `Breadcrumbs` provides `Related Content` for logs?

**Tip:** You may need to refresh the screen a few time to refresh the log search data in the background.
{{% /notice %}}

## 3. Workloads & Workload Details Pane

You can switch to the `K8s Workloads` view in two ways:

1) Go to the **Infrastructure** menu item in the Observability UI and select **Kubernetes** again, then pick the `K8s workloads` pane
OR
2) Simply change the value in the `Service` drop down box in the `Breadcrumbs` from *K8s nodes* to *K8s workloads*

![k8sNode](../images/K8s-Workloads.png) ![k8sToggle](../images/service-toggle.png)

Initially, the workload view will show you all the workloads that are reported by your clusters into your Observability Cloud Org. If an alert has fired for any of the workloads, it will be highlighted on the top right, *as marked with a red stripe in the image below*. You can go directly to the alert by clicking it to expand it.

We can also use the Breadcrumbs feature that we have learned about earlier. As a reminder, you will see the Breadcrumbs toward the top of the screen, *as marked with a yellow arrow in the image below*. When you drill down deeper into your workload, it will show drop downs for all levels and you can use it to navigate up and down the workload tree.

![Workloads](../images/k8s-workload-screen.png)

Now, let's find your own cluster by filtering on the field `k8s.cluster.name` in the filter toolbar, *as marked with a blue stripe in the image below*. Note: you can enter a partial name into the search box, such as 'ws-5-7*', to quickly find your Cluster. Remember, it's is a good idea to switch the default time from the default 3 hours back to 15 minutes.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How many workloads are running on your Cluster?
{{% /notice %}}

### 3.1 Using the Navigator Selection chart

The K8s.Namespace.Name Table is a common feature used across most of the Navigator's and will offer you a list view of the data you are viewing. In our case, it shows a list of `Pods Failed` grouped by `k8s.namespace.name`. You will find this pane used in various navigators in this workshop (ex: Workloads & Apache Servers). The way the selection pane works is similar across the navigators in that in that the information shown will match the selection criteria in your filters..

![k8s-workload-list](../images/workload-selection.png)

First, let's select the `File system usage (bytes)` from the **Color by** drop down box, *as marked with a green line in the image above*. Now,expand the Splunk Workload by clicking on the black triangle to the left of `Splunk` (*as marked by a black arrow in the image above*).

Once you expand a workload, you will note that each workload row has a colored rectangle at the end of it row. These bars change color according to the `color by` option you selected, *as marked by a green line in the image above*. These bars use colors to give a visual indication of health and/or usage.

If there are many workloads, you can change the `Result per page box` *as marked by an orange line in the image above*, to increase the list size. (It will also offer pagination if required).

Next, you can change the the list view to a heat map view by selecting either the Heat map icon or List icon in the upper-right corner of the screen: [heat-map-toggle](../images/heatmaptoggle.png) *(as marked with a purple line in the above image).*

Changing this option will result in the following representation:

![k8s-Heat-map](../images/heatmap.png)

This might be a useful view if you have many clusters as they can be grouped together using the `Group by` option *as marked by the green line in the above image*. The colors of each node will follow the `Color by` choice similar to the list view.

The last option, is `Find Outliers` which provides historical analytics of your clusters based on what is selected in the `Color by` box.

Now, click on the `Find outliers` drop down *as marked by a yellow stripe in the above image* and make sure the dialog is set as below:

![k8s-Heat-map](../images/set-find-outliers.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What happened to the Heatmap?
{{% /notice %}}

The `Find outliers` view is very useful when you need to view all or a selection of your workloads (or any service depending on the navigator used) and need to figure out if something has changed. It will give you a quick insight in items (workloads in our case) that are performing differently (both increase or decreased) which helps to make it easier to spot problems.

### 3.2 The Workload Overview pane

The workload overview gives you a quick insight of the status of your deployment. You can see at once if the pods of your deployments are Pending, Running, Failed, Succeeded or in an unknown state.  

![k8s-workload-overview](../images/k8s-workload-overview.png)

* *Running* Means your pods are deployed and in a running state
* *Pending* means waiting to be deployed
* *Succeeded* means the pod has been deployed and completed its job and is finished
* *Failed* means the containers in the pod have run and returned some kind of error
* *Unknown* means Kubernetes isn't reporting any of the known states. (This may be during start or stopping pods, for example).

To filter to a specific Workload, simply click on three dots `...` next to the workload name in the *k8s.workload.name* column and choose `filter` from the drop down box.

![workload-add-filter](../images/workload-add-filter.png)

This will add the selected workload to your filters.

### 3.3 Replicaset overview

The last chart will give you a bird's eye view on how many pods are deployed by Kubernetes for your deployment. In a replicaset, you can indicate the min, max and desired number of pods you wish to run as part the deployment.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What is the desired number of pods for the `splunk-otel-collector-k8s-cluster-reciever` replicaset?
{{% /notice %}}

### 3.4. Drilling down into your Workload

To bring up details of a workload in the Kubernetes Navigator, you either need to expand a namespace in the list mode or click on a workload square in the heatmap view.

In the heatmap mode, double click on the square for the `splunk-otel-collector-agent` workload in the *splunk* namespace.

![workload-expand](../images/workload-expand.png)

In the list view, you can click on the link that appears when expanding a namespace.

This will bring you to the `Workload detail` page where you get more details about the health and performance of your workload & pods.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What are the names of the container(s) in the **CPU resources (cpu units)** chart for the `splunk-otel-collector-agent`?
{{% /notice %}}

## 4. Pivot Sidebar

Later in the workshop, you will deploy an Apache server into your cluster which= will cause a pivot bar to appear.
As soon as any metric that is displayed in a Navigator is flowing into your observability org, the system will add that service to the pivot bar.

The pivot bar will expand and a link to the discovered service will be added as seen in the image below:

![pivotbar](../images/pivotbar.png)

This will allow for easy switching between navigators. The same applies for your Apache server instance -- it will have a pivot bar allowing you to quickly jump back to the Kubernetes navigator.
