---
title: Install the Cisco Enterprise Networks Content Pack
linkTitle: 2.1 Install the Cisco Enterprise Networks Content Pack
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

In this section you will install the Cisco Enterprise Networks Content Pack which provides pre-built services, KPIs, and data integrations for Cisco network infrastructure.

{{% notice title="Exercise: Install the Cisco Enterprise Networks Content Pack" style="primary" icon="running" %}}
**1.** In ITSI Navigate to **Configuration -> Data Integrations**

**2.** Select **Content Library** in the tabs under Data Integrations

{{% notice style="Info" %}}
Here you can see all of the available Out of the box Integrations that are available in the Splunk App for Content Packs

![Data Integrations](../../images/content-library.png?width=40vw)
{{% / notice %}}

**3.** Select the **Content Pack for Cisco Enterprise Networks**, and click **Proceed**

{{% notice style="Info" %}}
This page gives you an overview of what's available in the content pack

![Content Pack for Cisco Enterprise Networks](../../images/content-pack-overview.png?width=40vw)
{{% / notice %}}

**5.** Make sure **Add all 14 objects** is enabled

**6.** Enable the **Import As Enabled** toggle

**IMPORTANT: Do not enter a prefix in the Add a prefix to your new objects section**

**7.** Click **Install Selected**

{{% notice style="Info" %}}
Make sure Add all 14 objects and Import As Enabled are both toggled on before clicking Install Selected

![Install Selected](../../images/install-selected.png?width=40vw)
{{% / notice %}}

**8.** Click **Install**.

{{% notice style="Info" %}}
In production environments it's a best practice to take a backup before any major changes

![Install](../../images/install-confirm.png?width=40vw)
{{% / notice %}}

**9.** Confirm the installation is complete.

{{% notice style="Info" %}}
The summary confirms all objects were successfully installed

![Installation Complete](../../images/installation-complete.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="Nice Job!" %}}
The Cisco Enterprise Networks Content Pack is now installed!

In the next section you see how the content pack can be used to automatically import Catalyst Center Sites as services in ITSI.

Click **Configure Services** and continue to the next section of the workshop.
{{% / notice %}}

{{% / notice %}}
