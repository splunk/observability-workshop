---
title: The new Kubernetes Navigator
linkTitle: Touring the Kubernetes Navigator v2
weight: 22
---

## 0. Switching to the new Navigator UI

As we are in the process of switched to the new generation of the Kubernetes Navigator please check if you are already on the new Kubernetes navigator.

When you select `Kubernetes` as you focus, you should see a number of services panes for Kubernetes, similar like the ones below:

![k8s-navi-v-2](../images/k8s-nav2.png)

If you taken straight to the Kubernetes Navigator v1 after selecting `Kubernetes` in the right hand menu,  you need to set the feature flag for the new Navigator yourself.

To do this, please change the Url in your browser to match the following:</br>
https://app.[REALM].signalfx.com/#/Superpowers </br>
Were [REALM] needs to match the Realm we are running this workshop in.

Scroll down the list of feature and find the option: `newKubernetesNavigators` and set it like below

![Set-New-NAvi](../images/set_new_k8s_navi.png)

Once its set, you can refresh you page, and reselect kubernetes form the option in the infrastructure navigator menu.

## 1 The k8s cluster & cluster detail Pane

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this will offer you a number of kubernetes services. For this exercise pick the `K8s cluster` pane.

![k8s-cluster-pane](../images/k8sclusters.png)

The first thing you notice is that the pane indicates how many clusters are being monitored for you. The pane also shows a tiny graph of the load being handled across those clusters for a birds eye view.  Lastly, if there is a alert for one of the clusters it will be highlighted here too.

Click or select on the pane  and you will be taken to the `Infrastructure/Kubernetes/ K8s clusters` overview pane. Here you will find  a list  off all the Kubernetes clusters that are sending data to the Splunk Observability Cloud platform. Y

### 1.1 Finding your K8s cluster name

Your first task is to identify and find your own cluster.

The cluster will be named after your EC2 instance name: `ws-5-X-k3s-cluster` where `X` is the number of the EC2 instance assigned to you.

To find your node name look at the prompt of your EC2 instance, assuming you are assigned the 7th ec2 instance the prompt will show

``` bash
ubuntu@ws-5-7 ~ $
```

This means your cluster is named: `ws-5-7-k3s-cluster`  make a note as you will need this later in the workshop as a filter.

### 1.2 Using the K8s cluster Selection Pane

The k8s cluster Selection Pane by default, will offer a list view of your clusters like shown below.

![k8s-cluster-list](../images/k8sclusterselection.png)

You can scroll down the k8s cluster list or by using the filter on the top toolbar, *(marked with a blue stripe)*, with  the field `k8s.cluster.name`, to find your Cluster. </br>
You can enter a partial name into the search box such as 'ws-5-7', to find quickly find your Cluster.

Also its is a good idea to switch the default time from  the default 3 hours back to 15 minutes.

If there are many clusters, you can change the Result per page box *Marked by an orange line*,  to increase the list size.

You will note that each cluster row has a colored mark at the end of each row. These will change according the `color by` option, *Marked by a green line*, you have selected as to indicate its range. 

These are the possible options at this time:</br>
![k8s-colorby-list](../images/Infk8sColorBy.png)

Next, you can change the the list view to a heat map view by selecting either the Heatmap or List icon ![heatmap-toggle](../images/heatmaptoggle.png) *(Marked by a purple line).*

This will result in the follow representation:</br>
![k8s-heatmap](../images/heatmapview.png)

This might be a useful view if you have many cluster as they can be grouped together using the group by option *Marked by the green line* . The colors of each node will follow the color by  choice similar to the list view.

The last option, is the Find Outliers based on historical analytics of your clusters based on what is selected in the `colored by` box.  

This view is better used when you view all or a selection of you cluster. It will give you a quick insight which of your clusters are behaving differently than  they do normally and may need further investigation.
You may not see relevant info, The clusters in this workshop are short lived and  have not send enough meaningful data for the historical analytics to detect deviations.

### 1.3 The K8s cluster detail Pane

Initially,the cluster detail pane will show you the overall performance across all the servers as show below.
![k8s-allclusters](../images/k8s-allclusters.png)

As soon as you select your own cluster, you can see the overall performance of your luster, in this view you also can see if your cluster is affected by an alert:

![k8s-cluster-alert](../images/single-cluster-alert.png)

You may note that a `single alert` has fired  for this example Cluster

## 3. The Nodes & Node Details Pane

Go to the **Infrastructure** page in the Observability UI and select **Kubernetes**, this again will offer you a number of kubernetes services. For this exercise pick the `K8s Nodes` pane.

![k8sNode](../images/k8sNodes.png)

When Selected it may show a cluster that you have select4d previously, 



In a production environment you would expect to see multiple Nodes within a Cluster which would now all be visible and shown as individual pale blue squares, each containing green squares which represent pods, however in our workshop environment you each have a single node within your Cluster, represented by the large single blue square.

Drill down into the single Node by hovering over the pale blue background, then clicking on either the magnifying glass that appears in the top left corner, or double clicking on the pale blue background, this will take you to the Node level view.


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

You can now see the details for the Selected Container, with the Container Properties pane offering lots of detail on its configuration