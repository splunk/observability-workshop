---
title: 7. Infrastructure Home Page
description: This section of the workshop will equip you with the basic understanding of the Kubernetes and Database Navigators in the infrastructure section.
weight: 70
---

{{% button icon="clock" %}}5 minutes{{% /button %}}

This section is split in multiple sections and is going to be a little longer, the first section is a quick intro to the main page, followed by a few sections to dive deeper into some of the special features of the Splunk Observability suite, before we start to use our application and validate performance.

Please select Splunk Infrastructure from the menu bar on the right by selecting the ![Infra-monitoring](../images/inframon-icon.png?classes=inline&height=25px). This will bring us to the Infrastructure Home Page. It has 4 distinct sections that provide information on all technology that is sending metrics to the Splunk observability Suite.

![Infra main](../images/infrastructure-main.png?width=40vw)

* 1. Onboarding Pane, Here you will find video's and information related to Splunk Infrastructure. (Can be closed by pressing the X, if space is a premium)
* 2. Time & Filter Pane, This pane is used to modify the time window, and will expand in the next section to allow you to filter you views.
* 3. Integrations Pane, This pane allows you to select a specific technology set your focus on when looking at your infrastructure components.
* 4. Tile Pane, The tiles in this pane show, the all the features available for a specific technology, and a quick health status of that feature  with a history chart and alert count.  
     This allows you to see the status of all your technologies as you scroll along the page.

Using the Infrastructure pane, we can select the infrastructure/technology we are interested in, let's do that now.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Under the **Containers** section in the Integration Pane, select Kubernetes as the technology you wish to examine.
* This should show you two Tiles, one for *K8s Nodes* and one for *K8s Workloads* as shown below.
* Depending on how the workshop was set up you may see a lot of nodes or just one. This will not impact the workshop.

![Tiles](../images/kubernetes-tiles.png?width=20vw)

* Note that the bottom part of each tile will have a history graph and  the top part will show notifications for alerts that fired for the technology represented by the tile (kubernetes nodes and workloads in this case).  
  Across all tiles, this additional information on each of the tiles will give you a good over-view of the health of your infrastructure.
* Click on the *K8s Nodes* tile to look in more detail at the load on the Kubernetes nodes.

{{% /notice %}}
Let's move on  the next page and run a more detailed exercise based on Kubernetes and the Datastores
