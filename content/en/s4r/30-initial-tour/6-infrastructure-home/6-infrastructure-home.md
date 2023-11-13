---
title:  Infrastructure Navigators
linkTitle: 6. Infrastructure Navigators
description: This section of the workshop will equip you with a basic understanding of the Kubernetes and Database Navigators in the infrastructure section.
weight: 60
---

{{% button icon="clock" color="#ed0090" %}}2 minutes{{% /button %}}

Click on **Infrastructure** in the main menu, the Infrastructure Home Page is made up of 4 distinct sections.

![Infra main](../images/infrastructure-main.png)

1. **Onboarding Pane:** Training videos and links to documentation to get you started with Splunk Infrastructure Monitoring.
2. **Time & Filter Pane:** Time window (not configurable at the top level)
3. **Integrations Pane:** List of all the technologies that are sending metrics to Splunk Observability Cloud.
4. **Tile Pane:** Total number of services being monitored broken down by integration.

Using the Infrastructure pane, we can select the infrastructure/technology we are interested in, let's do that now.

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Under the **Containers** section in the Integrations Pane (**3**), select **Kubernetes** as the technology you wish to examine.
* This should show you two tiles, **K8s Nodes** and **K8s Workloads**.
* The bottom part of each tile will have a history graph and the top part will show notifications for alerts that fired. Across all tiles, this additional information on each of the tiles will give you a good overview of the health of your infrastructure.
* Click on the **K8s Nodes** tile to look in more detail at the load on the Kubernetes nodes.

{{% /notice %}}

Let's move to the next page and run a more detailed exercise based on Kubernetes and the data stores.
