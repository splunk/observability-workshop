---
title:  Infrastructure Navigators
linkTitle: 6.1 Infrastructure Navigators
weight: 2
---

Click on **Infrastructure** in the main menu, the Infrastructure Home Page is made up of 4 distinct sections.

![Infra main](../images/infrastructure-main.png)

1. **Onboarding Pane:** Training videos and links to documentation to get you started with Splunk Infrastructure Monitoring.
2. **Time & Filter Pane:** Time window (not configurable at the top level)
3. **Integrations Pane:** List of all the technologies that are sending metrics to Splunk Observability Cloud.
4. **Tile Pane:** Total number of services being monitored broken down by integration.

Using the Infrastructure pane, we can select the infrastructure/technology we are interested in, let's do that now.

{{% notice title="Exercise" style="green" icon="running" %}}

* Under the **Containers** section in the Integrations Pane (**3**), select **Kubernetes** as the technology you wish to examine.
* This should show you two tiles, **K8s Nodes** and **K8s Workloads**.
* The bottom part of each tile will have a history graph and the top part will show notifications for alerts that fired. Across all tiles, this additional information on each of the tiles will give you a good overview of the health of your infrastructure.
* Click on the **K8s Nodes** tile to look in more detail at the load on the Kubernetes nodes.
* You will see one or more representations of a Kubernetes Cluster.
* Even if there is only one visible, still filter & select the Workshop Cluster, by clicking on the {{% button style="gray" %}}Add filters{{% /button %}} button. Type `k8s.cluster.name` and search for the workshop name. This time the naming convention is **[NAME OF WORKSHOP]-k3s-cluster**. Click on {{% button style="blue" %}}Apply Filters{{% /button %}} when selected.

![cluster](../images/k8s-cluster.png)

 A- steps fro after lunch

* explain the red and green boxes, 
* note the two detected services on this cluster, Mysql and REdis introduce related content.
* clikc on redis
* find the REdis running on your ncluster  (naming convention). See metrics for you data storee
* note therelated  Kubneteres link,  click to go back to you cluster 
* click on  cluster in the tree.. back to start.
{{% /notice %}}
<!-- 
Either move to the next page and run an *optional* but more detailed exercise based on Kubernetes and the data stores used in the *Online Boutique* application or just go shopping! -->

This completes the tour of Splunk Observability Cloud.  Here, have some some virtual 💶 and let's go and look at our e-commerce site, the 'Online Boutique' and do some shopping.
