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
* You will be presented with one or more representations of a Kubernetes Cluster.
* Click on the {{% button %}}Add filters{{% /button %}} button. Type in `k8s.cluster.name` and click on the search result.
* From the list, select **[NAME OF WORKSHOP]-k3s-cluster** then click on the {{% button style="blue" %}}Apply Filter{{% /button %}} button.

  ![cluster](../images/k8s-cluster.png)

* The Kubernetes Navigator uses color to indicate health. As you can see there are two pods or services that are unhealthy and in a Failed state (**1**). The rest are healthy and running. This is not uncommon in shared Kubernetes environments, so we replicated that for the workshop.
* Note the tiles to the side, under **Nodes dependencies** (**2**), specifically the MySQL and Redis tiles. These are the two databases used by our e-commerce application.
{{% /notice %}}

{{% notice title="Related Content" style="info" %}}

The Splunk Observability User Interface will attempt to show you additional information that is related and relevant to what you're actively looking at.
A good example of this is the Kubernetes Navigator showing you **Related Content** tiles in the information Pane for services discovered running on this node.

{{% /notice %}}

{{% notice title=" Related Content Exercise" style="green" icon="running" %}}

* Find and click on the **Redis** tile. This will take you to the list of the *Redis* Datastore services. Select the one running on your cluster, the naming convention is **redis-[NAME OF WORKSHOP]**.

  ![redis](../images/redis-2.png)

* This will bring you to the Redis Datastore Navigator. This navigator will show charts with metric data from the active *Redis* cluster from our e-commerce site.
{{< tabs >}}
{{% tab title="Question" %}}
**Are there Related Content Tiles? (Check the answer for more info.)**
{{% /tab %}}
{{% tab title="Answer" color="green"%}}
**Yes, there is one for Kubernetes.**
* Click the tile, it will bring us back into the Kubernetes Navigator, this time at the Pod level showing the Pod that runs the Redis Service.
* To return to the Cluster level, simply click on the link *Cluster* (1) at the top of the screen.

 ![node](../images/node-link.png)

{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}
<!-- 
Either move to the next page and run an *optional* but more detailed exercise based on Kubernetes and the data stores used in the *Online Boutique* application or just go shopping! -->

This completes the tour of Splunk Infrastructure and Splunk Observability Cloud.  

Here, have some virtual 💶 and let's go and look at our e-commerce site, the 'Online Boutique' and do some shopping.
