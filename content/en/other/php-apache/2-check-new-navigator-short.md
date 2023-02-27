---
title: Tour of the Kubernetes Navigator v2
linkTitle: 2. Kubernetes Navigator v2
weight: 2
--- 

## 1. Cluster vs Workload View

The Kubernetes Navigator offers you two separate use cases to view your Kubernetes data.

* The **K8s workloads** is focusing on providing information in regards to workloads a.k.a. *your deployments*.
* The **K8s nodes** is focusing on providing insight into the performance of clusters, Nodes, Pods & Containers.

You initially select either view depending on your need (you can switch between the view on the fly if required). The most common one we will use in this workshop is the  workload view and we will focus on that specifically.

### 1.1 Finding your K8s Cluster name

Your first task is to identify and find your own cluster. The cluster will be named after your EC2 instance name.

To confirm your EC2 instance name, look at the prompt of your EC2 instance. For example, if you are assigned the 7th EC2 instance, the prompt will show:

``` bash
ubuntu@emea-ws-7 ~ $
```

This means your cluster is named: `emea-ws-7-k3s-cluster`. Please make a note of your cluster name as you will need this later in the workshop for filtering.

## 2. Workloads & Workload Details Pane

Go to the **Infrastructure** menu item in the Observability UI and select **Kubernetes**. Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will offer you a set of Kubernetes services, one of them being the **K8s workloads** pane.

The pane will show a tiny graph giving you a bird's eye view of the load being handled across those Workloads. Also, if there are any alerts for one of the workloads, you will see a small alert indicator as shown in the image above.

![k8sWorkloads](../images/K8s-Workloads.png)

Click on the **K8s workloads** pane and you will be taken to the workload view.

Initially, you will see all the workloads that are reported by your clusters into your Observability Cloud Org. If an alert has fired for any of the workloads, it will be highlighted on the top right *as marked with a red stripe* in the image below. You can go directly to the alert by clicking it to expand it.

![Workloads](../images/k8s-workload-screen.png)

Now, let's find your own cluster by filtering on the field `k8s.cluster.name` in the filter toolbar, *as marked with a blue stripe*. Note: you can enter a partial name into the search box, such as 'emea-ws-7*', to quickly find your Cluster. Also it's a very good idea to switch the default time from the default **-3h** back to last 15 minutes (**-15m**).

You should now just see information for your own cluster.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How many workloads are running & how many namespaces are in your Cluster?
{{% /notice %}}

### 2.1 Using the Navigator Selection chart

The **K8s workloads** table is a common feature used across most of the Navigator's and will offer you a list view of the data you are viewing. In our case, it shows a list of `Pods Failed` grouped by `k8s.namespace.name`.

You will find this pane used in various Navigators in this workshop (ex: Workloads & Apache Servers). The way the selection pane works is similar across the Navigators in that the information shown will match the selection criteria in your filters.

![k8s-workload-list](../images/workload-selection.png)

Now let's change the list view to a heat map view by selecting either the Heat map icon or List icon in the upper-right corner of the screen *(as marked with a purple line)*.

Changing this option will result in the following representation, which is one we will use most of the time in this workshop:

![k8s-Heat-map](../images/heatmap.png)

In this view, you will note that each workload is now a colored rectangle. These rectangles change color according to the **Color by** option you selected, *as marked by a green line* above. The colors give a visual indication of health and/or usage. You can check the meaning by hovering over the **legend** exclamation icon {{% icon icon="exclamation-circle" %}}
 bottom right of the heatmaps.

Another valuable option in this screen is **Find Outliers** which provides historical analytics of your clusters based on what is selected in the **Color by** dropdown.

Now, let's select the **File system usage (bytes)** from the **Color by** drop down box, *as marked with a green line* then click on the **Find outliers** drop down *as marked by a yellow stripe* in the above image and make sure you change the Strategy in the dialog  to **Deviation from Median** as below:

![k8s-Heat-map](../images/set-find-outliers.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What happened to the Heatmap?
{{% /notice %}}

The **Find outliers** view is very useful when you need to view a selection of your workloads (or any service depending on the Navigator used) and quickly need to figure out if something has changed.

It will give you fast insight into items (workloads in our case) that are performing differently (both increased or decreased) which helps to make it easier to spot problems.

Now switch the **Find Outliers** option back to off.

### 2.2 The Workload Overview pane

The workload overview gives you a quick insight of the status of your deployment. You can see at once if the pods of your deployments are Pending, Running, Failed, Succeeded or in an unknown state.  

![k8s-workload-overview](../images/k8s-workload-overview.png)

* *Running:* Pods are deployed and in a running state
* *Pending:* Waiting to be deployed
* *Succeeded:* Pod has been deployed and completed its job and is finished
* *Failed:* Containers in the pod have run and returned some kind of error
* *Unknown:* Kubernetes isn't reporting any of the known states. (This may be during start or stopping of pods, for example).

You can expand the Workload name by hovering your mouse on it, in case the name is longer than the chart allows.

![k8s-workload-hoover](../images/k8s-workload-hoover.png)

To filter to a specific workload, you can click on three dots `...` next to the workload name in the **k8s.workload.name** column and choose **Filter** from the dropdown box.

![workload-add-filter](../images/workload-add-filter.png)

This will add the selected workload to your filters. Try this for the **splunk-otel-collector-k8s-cluster-receiver** workload. It should give you a single  rectangle in the `splunk` namespace.

Confirm that you have the right filter by hovering over the rectangle, and if it is indeed the **splunk-otel-collector-k8s-cluster-receiver** workload, by double-clicking on it. This brings you to a more detailed view of your workload.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What are the CPU request  & CPU limit units for the otel-collector?
{{% /notice %}}

At this point you can drill into the information of the pods, but that is outside the scope of this workshop, for now reset your view by removing the filter for the **splunk-otel-collector-k8s-cluster-receiver** workload and setting the **Color by** option to **Pods Running**.

## 3. Pivot Sidebar

Later in the workshop, you will deploy an Apache server into your cluster which will create a new icon in the **Pivot Sidebar**.

As soon as any metric that is used by a Navigator, is flowing into your Observability org, the system will add that service to the Pivot Sidebar.

The Pivot Sidebar will expand and a link to the discovered service will be added as seen in the image below:

![pivotbar](../images/pivotbar.png)

This will allow for easy switching between Navigators. The same applies for your Apache server instance, it will have a Pivot Sidebar allowing you to quickly jump back to the Kubernetes navigator.
