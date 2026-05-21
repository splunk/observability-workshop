---
title: ITSI Service and KPI Review
linkTitle: 5.2 ITSI Service and KPI Review
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

In this section you will review the services and episodes created by the content packs and alert integrations configured in the previous steps, confirming the full end-to-end pipeline is working correctly.

{{% notice title="Exercise: Review Services and Episodes" style="primary" icon="running" %}}

{{% notice style="info" %}}
Service Insights in IT Service Intelligence (ITSI) represents the mapping and monitoring of business and technical services within your organization. Within ITSI, a service is a set of interconnected applications and hosts configured to offer a specific service to the organization. ITSI Service Insights helps you map these service dependencies based on a connection between devices and applications, so you can immediately see the impact of a problematic object on the rest of the service operation.
{{% /notice %}}

**1.** Navigate to the **ITSI Service Analyzer** > **Default Service Analyzer**. You should see the services you imported

**2.** Edit the Analyzer name to `Network Health by Location`

{{% notice style="Info" %}}
The Tree view shows the full service hierarchy with each Catalyst Center site and its underlying KPI health

![Service Analyzer Tree View](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}

**3.** Click **Tree** on the right side

**4.** Add **United States** to **Filter Services**

**5.** Set the timeframe to **Last 1 hour** and **Auto Refresh** to **1 minute**

{{% notice style="Info" %}}
Filtering by United States and setting Auto Refresh gives you a live view of site health across all locations

![Episode Review](../../images/service-kpis.png?width=40vw)
{{% / notice %}}

**6.** Click **Save**. The view should be identical to the graphic below

**7.** Click **Alerts and Episodes**

**8.** Select the most recently created episode

**9.** In the **Episode details** confirm that the **Aggregation Policy** used was the NEAP you created in the previous step

{{% notice style="Info" %}}
Episodes created by the custom NEAP group Catalyst Center and SolarWinds alerts together under a single site-named episode

![Alerts and Episodes](../../images/episode-review.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="Nice Job!" %}}
The full pipeline is confirmed. Services and their dependencies are configured, KPIs are calculating, and the custom NEAP is grouping cross-vendor alerts by site.

Continue to the next section to walkthrough this scenario.
{{% / notice %}}

{{% /notice %}}
