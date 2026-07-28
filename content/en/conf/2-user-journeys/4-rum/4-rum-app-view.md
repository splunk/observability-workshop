---
title: RUM Application Overview
linkTitle: 2. App Overview
weight: 2
time: 3 minutes
---

At the top of the session page, click the breadcrumb link to the workshop app.

{{% exercise title="Find critical workflows" %}}

* You will now see a dashboard breaking down RUM metrics by **User Experience**, **Front-end Health**, **Back-end Health**, **Custom Workflows**, **Pages**, **Network Requests**, and a **Map View**. Current metrics are compared to historic metrics (1 hour by default).

![RUM Dashboard](../images/rum-metric-map-charts.png)

* Click through each of the tabs and examine the data.

{{< tabs >}}
{{% tab title="Questions" %}}

1. If you examine the charts in the **Custom Workflows** tab, what chart shows the **latency** for `PlaceOrder`?
2. In the **Map View** tab, where is the largest request volume coming from?

{{% /tab %}}
{{% tab title="Answers" %}}

1. **Custom Event Latency P75**
2. **US**

{{% /tab %}}
{{< /tabs >}}

* Make sure you are on the **Custom Workflows** tab.
* To identify problematic user sessions, we will use the latency spikes in the **Custom Event Latency** chart.
* In the **Custom Workflow Latency** chart click on the **see all** link under the chart title.

![RUM See All Custom Workflows](../images/rum-see-all.png)

{{% /exercise %}}
