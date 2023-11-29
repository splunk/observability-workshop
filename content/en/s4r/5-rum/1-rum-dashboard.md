---
title: 1. RUM Dashboard
weight: 1
---

In Splunk Observability Cloud from the main menu, click on **RUM**. you arrive at the RUM Home page, this view has already been covered in the short introduction earlier.

![multiple apps](../images/multiple-apps.png)

Make sure you select your workshop by ensuring the drop-downs are set/selected as follows:

* The **Timeframe** is set to **-15m**.
* The **Environment** selected is **[NAME OF WORKSHOP]-workshop**.
* The **App** selected is **[NAME OF WORKSHOP]-store**.
* The **Source** is set to **All**.

Next, click on the **[NAME OF WORKSHOP]-workshop** above the **Page Views / JavaScript Errors** chart.

This will bring up a dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events** and compares them to  the same metrics historically (1 hour by default). <!-- For more detailed information on the metrics collected by Splunk RUM see [**here**](https://docs.splunk.com/observability/en/gdi/get-data-in/rum/browser/rum-browser-data-model.html#rum-browser-data). -->

![RUM Dashboard](../images/rum-dashboard.png)

* **UX Metrics**, This tab groups the *Web vitals* an other user interface metrics together.  
* **Front-end Health**, This tab shows metrics regarding how the website behaved in the browsers.  
* **Back-end Health**, In this tab you can find thh metric related to overall network behavior.
* **Custom Events**, In this tab we find metrics related to Custom Events added to the website by the developer to track behaviour.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click through each of the tabs (**UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events**)
* Find the chart that clearly show there is an issue with the application. (Hint, its a Custom Event)

{{% /notice %}}
