---
title: 1. Real User Monitoring 
weight: 1
---

In Splunk Observability Cloud from the main menu, click on **Digital Experience**, followed by selecting **overview** (**1**) from the Real user Monitoring  section as show below. 

![RUM](../images/rum-de.png?width=920px)

This will open up the *Real User Monitoring Overview* and you should see your shop, **labobs-1037-store** (**3**) in the *Application summary dashboard*. This section is showing a quick overview of all RUM apps you are monitoring.

![main page](../images/rum-dashboard.png?width=920px)

{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure you select the *Cisco Live EMEA Walk-in Lab* Store data by ensuring the drop-downs are set/selected in the red underlined section (**2**) above as follows:
  * The **Time frame** is set to **-15m**.
  * The **Environment** selected is **labobs-1037**.
  * The **App** selected is **labobs-1037-store**.
  * The **Source** is set to **Browser**.
* Next, click on the **labobs-1037-store** (**3**) above the **Page Views / JavaScript Errors** chart.
* This will bring up a new dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events** and comparing them to historic metrics (1 hour by default).

{{% /notice %}}

![RUM Dashboard](../images/rum-metric-map-charts.png?width=920px)

* **UX Metrics:** Page Views, Page Load and Web Vitals metrics.
* **Front-end Health:** Breakdown of Javascript Errors and Long Task duration and count.
* **Back-end Health:** Network Errors and Requests and Time to First Byte.
* **Custom Events:** RED metrics (Rate, Error & Duration) for custom events.
* **Network Requests:** Sortable lists of all Network Requests
* **Pages:** Sortable lists of all Pages visited
* **Map View** Show where request where made from in the world

{{% notice title="Exercise" style="green" icon="running" %}}

* Click through each of the tabs (**UX Metrics**, **Front-end Health**, **Back-end Health**, **Custom Events**, **Network Requests:**, **Pages:** and **Map View**) and examine the data.

{{< tabs >}}
{{% tab title="Questions" %}}
* **If you examine the charts in the *Custom Events* Tab, **what chart **shows** clearly the** latency Spikes?**
* **Check the Map view, where is the largest  REquest volume coming from?**
{{% /tab %}}
{{% tab title="Answers" %}}
* **It is the *Custom Event Latency* chart**
* **It is *Ireland***
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
