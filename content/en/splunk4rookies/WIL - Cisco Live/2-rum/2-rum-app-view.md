---
title: 2. Application View
weight: 2
---

You should now see a dashboard view breaking down the metrics by **UX Metrics**, **Front-end Health**, **Back-end Health** and **Custom Events**, comparing them to historic metrics (1 hour by default).

![RUM Dashboard](../images/rum-metric-map-charts.png?width=920px)

The tabs available on this page include:

* **UX Metrics:** Page Views, Page Load and Web Vitals metrics.
* **Front-end Health:** Breakdown of Javascript Errors and Long Task duration and count.
* **Back-end Health:** Network Errors and Requests and Time to First Byte.
* **Custom Events:** RED metrics (Rate, Error & Duration) for custom events.
* **Network Requests:** Sortable lists of all Network Requests
* **Pages:** Sortable lists of all Pages visited
* **Map View:** Shows where requests were made from in the world

{{% notice title="Exercise" style="green" icon="running" %}}

* Click through each of the tabs (**UX Metrics**, **Front-end Health**, **Back-end Health**, **Custom Events**, **Network Requests:**, **Pages:** and **Map View**) and examine the data.

{{< tabs >}}
{{% tab title="Questions" %}}

* **If you examine the charts in the *Custom Events* Tab, what chart shows clearly the latency spikes?**
* **Check the Map view, where is the largest request volume coming from?**

{{% /tab %}}
{{% tab title="Answers" %}}

* **It is the *Custom Event Latency* chart**
* **It is *Ireland***

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
