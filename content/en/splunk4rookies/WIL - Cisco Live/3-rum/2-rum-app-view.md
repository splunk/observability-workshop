---
title: 2. Application View
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

* You will now see a dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health**, **Custom Events**, **Network Requests**, **Pages** and a **Map View** comparing them to historic metrics (1 hour by default).

![RUM Dashboard](../images/rum-metric-map-charts.png)

* The tabs available on this page include:
  * **UX Metrics** Page Views, Page Load and Web Vitals metrics
  * **Front-end Health** Breakdown of JavaScript Errors and Long Task duration and count
  * **Back-end Health** Network Errors and Requests and Time to First Byte
  * **Custom Events** RED metrics (Rate, Error & Duration) for custom events
  * **Network Requests** Network URL grouping and key metrics
  * **Pages** URL grouping and key metrics and web vitals
  * **Map View** Geographical requests by location

* Click through each of the tabs and examine the data.

{{< tabs >}}
{{% tab title="Questions" %}}

1. If you examine the charts in the **Custom Events** tab, what chart shows clearly the latency spikes?
2. In the **Map View** tab, where is the largest request volume coming from?

{{% /tab %}}
{{% tab title="Answers" %}}

1. **Custom Event Latency P75**
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* Make sure you are on the **Custom Events** tab.
* To identify problematic user sessions, we will use the latency spikes in the **Custom Event Latency P75** chart.
* In the **Custom Event Latency** chart click on the **see all** **(1)** link under the chart title.

![RUM See All](../images/rum-see-all.png)

{{% /notice %}}
