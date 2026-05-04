---
title: Install the Cisco Enterprise Networks Content Pack
linkTitle: 2.1 Install the Cisco Enterprise Networks Content Pack
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
In this section you will install the Cisco Enterprise Networks Content Pack which provides pre-built services, KPIs, and data integrations for Cisco network infrastructure.
</center>

{{% notice title="Exercise: Install the Cisco Enterprise Networks Content Pack" style="primary" icon="running" %}}
**1.** In ITSI Navigate to **Configuration -> Data Integrations**

**2.** Select **Content Library** in the tabs under Data Integrations

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}} 
<div style="text-align: center;">
Here you can see all of the available Out of the box Integrations that are available in the Splunk App for Content Packs
</div>

![Data Integrations](../../images/content-library.png?width=40vw)
{{% / notice %}}
</div>

**3.** Select the **Content Pack for Cisco Enterprise Networks**, and click **Proceed**

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}} 
<div style="text-align: center;">
This page gives you an overview of what's available in the content pack
</div>

![Content Pack for Cisco Enterprise Networks](../../images/content-pack-overview.png?width=40vw)
{{% / notice %}}
</div>

**5.** Make sure **Add all 14 objects** is enabled

**6.** Enable the **Import As Enabled** toggle

**IMPORTANT: Do not enter a prefix in the Add a prefix to your new objects section**

**7.** Click **Install Selected**

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}} 
<div style="text-align: center;">
Make sure Add all 14 objects and Import As Enabled are both toggled on before clicking Install Selected
</div>

![Install Selected](../../images/install-selected.png?width=40vw)
{{% / notice %}}
</div>

**8.** Click **Install**.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}} 
<div style="text-align: center;">
In production environments it's a best practice to take a backup before any major changes
</div>

![Install](../../images/install-confirm.png?width=40vw)
{{% / notice %}}
</div>

**9.** Confirm the installation is complete.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}} 
<div style="text-align: center;">
The summary confirms all objects were successfully installed
</div>

![Installation Complete](../../images/installation-complete.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="Nice Job!" %}} 
<div style="text-align: center;">
The Cisco Enterprise Networks Content Pack is now installed! 

In the next section you see how the content pack can be used to automatically import Catalyst Center Sites as services in ITSI.

Click **Configure Services** and continue to the next section of the workshop.
</div>
{{% / notice %}}

{{% / notice %}}
</div>