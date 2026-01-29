---
title: 1. Real User Monitoring 
weight: 1
hidden: true
---

In Splunk Observability Cloud from the main menu, click on **Digital Experience**, followed by selecting **overview** (**1**) from the Real user Monitoring  section as show below. 

![RUM](../images/rum-de.png)

This will open up the Real User Monitoring Overview:

![main page](../images/rum-dashboard.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure you select your workshop by ensuring the drop-downs are set/selected as follows:
  * The **Time frame** is set to **-15m**.
  * The **Environment** selected is **[NAME OF WORKSHOP]-workshop**.
  * The **App** selected is **[NAME OF WORKSHOP]-store**.
  * The **Source** is set to **All**.
* Next, click on the **[NAME OF WORKSHOP]-store** above the **Page Views / JavaScript Errors** chart.
* This will bring up a new dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events** and comparing them to historic metrics (1 hour by default).

{{% /notice %}}

![RUM Dashboard](../images/rum-metrics-dashboard.png)

* **UX Metrics:** Page Views, Page Load and Web Vitals metrics.
* **Front-end Health:** Breakdown of Javascript Errors and Long Task duration and count.
* **Back-end Health:** Network Errors and Requests and Time to First Byte.
* **Custom Events:** RED metrics (Rate, Error & Duration) for custom events.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click through each of the tabs (**UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events**) and examine the data.

{{< tabs >}}
{{% tab title="Question" %}}
**If you examine the charts in the *Custom Events* Tab, **what chart **shows** clearly the** latency Spikes?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It is the *Custom Event Latency* chart**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
