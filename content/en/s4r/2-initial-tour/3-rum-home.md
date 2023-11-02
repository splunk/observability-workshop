---
title: Real User Monitoring Home Page
linkTitle: 3. RUM Home Page
weight: 30
---
 
{{% button icon="clock" %}}5 minutes{{% /button %}}

Again, as this is the quick tour and we will be visiting the Real User Monitoring UI in more detail later, this will just highlight the main options.

{{% notice title=" Rum Environments & Apps" style="info" %}}
As with APM, Real User Monitoring works with environments to separate RUM information/traces information, this allows you to separate RUM trace information from different teams/applications. It also adds an extra option for Apps (short for applications). This allows you to distinguish between separate browser applications in the same environment.

Splunk RUM offers RUM for both Browser & Mobile applications.  You will see that as the source type in the Ui. In this workshop we will just focus on browser based  RUM.
{{% /notice %}}

If you have not done so already, please select ![RUM](../images/rum-icon.png?classes=inline&height=25px) from the Main menu. This will bring you to the RUM Home page.

This Page has 3 distinct sections that provide information or allows you to navigate the RUM UI.

![RUM Page](../images/rum-main-page.png?width=30vw)

1. Onboarding Pane. Here you will find video's and references to document pages of interest for RUM  
(Can be closed by the **X** on the right, if space is at a premium.)
2. Filter Pane. This pane allows you to filter on Environment, Application and source type.
3. Application Summary Pane. This pane shows you a health summary of all your  applications that send RUM trace info. Note, that the summaries have a compact and a more detailed view (as show in the Image above.)

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First,

{{% /notice %}}

We will investigate RUM in more detail later, so lets have a look at how Splunk Log Observer works with Log data in the next page.
