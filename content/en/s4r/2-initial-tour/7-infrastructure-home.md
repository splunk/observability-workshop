---
title: 7. Infrastructure Home Page
description: This section of the workshop will equip you with the basic understanding of the Kubernetes and Database Navigators in the infrastructure section.
weight: 70
---

{{% button icon="clock" %}}15 minutes{{% /button %}}

This section is split in two and is going to be a little longer, the first section is a quick intro to the main page, followed by a section to dive deeper into some of the special features of the Splunk Observability suite, before we start to use our application and validate performance.

Please select Splunk Infrastructure from the menu bar on the right by selecting the ![Infra-monitoring](../images/inframon-icon.png?classes=inline&height=25px). This will bring us to the Infrastructure Home Page. It has 4 distinct sections that provide either useful information you pick or create a Synthetic Test.

![Infra main](../images/infrastructure-main.png?width=40vw)

* 1. Onboarding Pane, Here you will find video's and information related to Splunk Infrastructure. (Can be closed by pressing the X, if space is a premium)
* 2. Time & Filter Pane, This pane is used to modify the time window, and will expand in the next section to allow you to filter you views.
* 3. Integration Pane, This pane allows you to select a specific technology set  to focus on when looking at your infrastructure components.
* 4. Tile Pane, The Tiles in this  pane show in one view both the features available for a specific technology, and a quick  health status of your systems with a chart and alert count.

In the main page, we can select the infrastructure/technology we are interested in, let's do that now.

 {{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Under the **Containers** section in the Integration Pane, select Kubernetesas the technology you wish to examine.
* This should show you two Tiles, one for *K8s Nodes* and one for *K8s Workloads*
![Tiles](../images/kubernetes-tiles.png?width=20vw)
* Note in the Image above, the purple chart (3) for CPU% on both tiles, as well as notifications for alerts (2) that fired for these kubernetes cluster(s).
* Click on the K8s Nodes page to look in more detail at the load on the Kubernetes nodes.

{{% /notice %}}
Let's move on  the next page and run a more detailed exercise based on Kubernetes and the Datastores
