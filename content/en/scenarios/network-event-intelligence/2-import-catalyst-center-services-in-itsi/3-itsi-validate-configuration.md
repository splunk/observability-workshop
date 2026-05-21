---
title: Validate the Configuration
linkTitle: 2.3 Validate the Configuration
weight: 3
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

Confirm that the imported services and KPIs are calculating correctly, and that the alert pipeline from Catalyst Center is active before moving on.

{{% notice title="Exercise: Validate the Configuration" style="primary" icon="running" %}}

**1.** Navigate to the **Service Analyzer** > **Default Service Analyzer**.

You should see the services you imported and the KPIs that are part of the Catalyst Center Site Service Template.

It may take a few minutes for your services and KPIs to show a health status.

{{% notice style="Info" %}}
The Service Analyzer shows the imported Catalyst Center site services and their current health status

![ITSI Service Analyzer](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}

**2.** Click **Tree** to switch to the **Service Tree** view

**3.** Click one of the Store services in the service tree to view the KPIs associated with the Catalyst Center Site

{{% notice style="Info" %}}
Clicking a service reveals its individual KPIs and their current health scores per network layer

![Service KPIs](../../images/service-kpis.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="Congrats!" %}}
Your Catalyst Center services are live in ITSI!

In the next section you'll configure the **Inbound Notification Service** which will automatically create notable events in ITSI when a Catalyst Center Issue occurs indicating degraded network performance.
{{% / notice %}}

{{% / notice %}}
