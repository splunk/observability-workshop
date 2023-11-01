---
title: Real User Monitoring Home Page
linkTitle: 3. RUM Home Page
weight: 30
---
 
{{% button icon="clock" %}}5 minutes{{% /button %}}

If you have not done so already, please select


### WIP WIP WIP WIP WIP WIP WIP



---


 ![RUM](../images/apm-icon.png?classes=inline&height=25px) from the Main menu. This will bring you to the APM Home page. We will not go into all the sections for apm in this tour as we will do a deep dive later.

This Page has 4 distinct sections that provide information or allows you to navigate the APM UI.

![apm page](../images/apm-main.png?width=30vw)

1. Instruction Pane, Here you will find video's and references to document pages of interest for APM  
(Can be closed by the **X** on the right, if space is at a premium.)
2. APM Overview Pane, This pane shows you dashboards of consolidated and unsampled trace information for  a real-time snapshot of your services behaviour.
3. Function Pane, this pane allows for quick movement between the different functions that make up Splunk APM.

{{% notice title=" About Environments" style="info" %}}
Usually you will have multiple teams or applications send Trace data to Splunk APM. To differentiate between these teams or application, Splunk uses environments. And users can work with one or more environment at the same time. However, in this workshop everything is contained in one single environment.  
This naming convention for your environment is *[NAME OF WORKSHOP]-workshop*. Your instruction can provide the correct name.

{{% /notice %}}

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First,verify that time window we are working with is set to the last 15 minutes.  If this is not the case, change it by using the drop down in APM Overview Pane ![time-window](../../images/time-window.png?classes=inline) at the top of the page and set it to *the last 15 minutes*.
* Change the environment to the workshop one by selecting its name from the drop down box and make sure that is the only one with a ![blue tick](../../images/blue-tick.png?classes=inline) in front of it.
* Now, lets have a look at our service Map.  This map will show you how your components/services interact together in the selected time frame based on the Trace  information send to the Splunk Observability Suite.
* Click on the Explore Tile in the Function Pane. This will bring use to the automatically generated map of our service interaction.

![APM Map](../images/apm-map.png?width=30vw)

{{% /notice %}}

We will investigate APM in more detail later, so lets have a look at  how Real User Monitoring works in the next page.
