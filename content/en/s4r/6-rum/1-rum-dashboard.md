---
title: 1. RUM Dashboard
weight: 1
tags: RUM
---

In Splunk Observability Cloud from the main menu, click on **RUM**. From the drop-downs ensure the following is set/selected:

* Timeframe is set to **-15m**.
* Environment selected is **[NAME OF WORKSHOP]-workshop**.
* App selected is **[NAME OF WORKSHOP]-shop**.
* Source is set to **All**.

This view has already been covered in the short introduction earlier. Next, click on the **[NAME OF WORKSHOP]-workshop** above the **Page Views / JavaScript Errors** chart.

This will bring up a dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events**. For more detailed information on the metrics collected by Splunk RUM see [**here**](https://docs.splunk.com/observability/en/gdi/get-data-in/rum/browser/rum-browser-data-model.html#rum-browser-data).

![RUM Dashboard](../images/rum-dashboard.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Click through each of the tabs (**UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events**)
* Identify the charts that clearly show there is an issue with the application.

{{% /notice %}}
