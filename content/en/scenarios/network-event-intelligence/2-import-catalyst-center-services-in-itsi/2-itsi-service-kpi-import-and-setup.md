---
title: ITSI Service and KPI Validation
linkTitle: 2.2 ITSI Service and KPI Validation
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

With ITSI 4.21 manual import processes are replaced by a guided workflow and pre-built data integrations. The content pack includes service import modules that discover and build the service hierarchy for Meraki and Catalyst Center automatically.

{{% notice title="Exercise: Import Services and Configure Alerts" style="primary" icon="running" %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
To get back to the Import Services page for Catalyst Center, navigate to **Configuration** > **Data Integrations** > **Content Library** > **Cisco Enterprise Networks**.
{{% / notice %}}

**1.** Under **Service Import Modules**, select **Cisco Catalyst Center**.

{{% notice style="Info"  %}}
Automatic service hierarchy imports are supported for both <strong>Catalyst Center</strong> and <strong>Meraki</strong>

![Service Import Modules](../../images/service-import-modules.png?width=40vw)
{{% / notice %}}

**2.** Select the Catalyst Center Host and all available services. Click **Next**.

{{% notice style="Info" %}}
Select the Catalyst Center host and all available sites to import as ITSI services

![Select Services](../../images/select-services.png?width=40vw)
{{% / notice %}}

**3.** Select **Default Service Sandbox**. Click **Next**.

{{% notice style="Info" %}}
Services are imported into a sandbox for review before being published to production ITSI

![Default Service Sandbox](../../images/default-service-sandbox.png?width=40vw)
{{% / notice %}}

**4.** Review the Services that will be imported. Click **Import**.

{{% notice style="Info" %}}
Review the complete list of Catalyst Center site services that will be created before clicking Import

![Review Services](../../images/review-services.png?width=40vw)
{{% / notice %}}

**5.** Review the Service Sandbox. Click **Publish**. After the precheck completes, click **Next**.

{{% notice style="Info" %}}
Review the service hierarchy in the sandbox, then publish to make the services active in ITSI

![Service Sandbox](../../images/service-sandbox-publish.png?width=40vw)
{{% / notice %}}

**6.** Navigate to **Configuration** > **Service Monitoring** > **Service and KPI Management**. 

**7.** Use the **Select All** check box to select all of your services 

**8.** With all services selected click **Bulk Action** > **Enable**.

{{% notice style="Info" %}}
Use Bulk Action to enable all imported services at once from the Service and KPI Management page

![Service and KPI Management](../../images/service-kpi-management.png?width=40vw)
{{% / notice %}}

**9.** Click **Enable**. After a few minutes the KPIs will populate.

{{% notice style="Info" %}}
Confirm the enable action. KPIs will begin calculating within a few minutes

![Enable KPIs](../../images/enable-kpis.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="Nice Job!" %}} 
You just imported all of the Catalyst Center services without having to create any CSVs, lookups, write any SPL, or manually configure the service dependencies. Pretty neat, huh?

Continue to the next section to validate your configuration is working correctly.
{{% / notice %}}

{{% /notice %}}
