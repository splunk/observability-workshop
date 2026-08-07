---
title: RUM Application Overview
linkTitle: 2. App Overview
weight: 2
time: 3 minutes
---

At the top of the session page, click the breadcrumb link to the workshop app. Alternatively, you can hover over the "Digital Experience" menu item on the left, click into the `Overview` for Real User Monitoring, and click the name of the workshop app on that page.

{{% exercise title="Find critical workflows" %}}

You will now see a dashboard breaking down RUM metrics by **User Experience**, **Front-end Health**, **Back-end Health**, **Custom Workflows**, **Pages**, **Network Requests**, and a **Map View**. Current metrics are compared to historic metrics (1 hour by default).

![RUM Dashboard](../images/rum-metric-map-charts.png)

Click through each of the tabs and examine the data.

{{< tabs >}}
{{% tab title="Questions" %}}

1. If you examine the charts in the **Custom Workflows** tab, what chart shows the **latency** for `PlaceOrder`?
2. Geographically, where is user traffic coming from?

{{% /tab %}}
{{% tab title="Answers" %}}

1. Custom Workflow Duration
2. US, UK, France, and Germany (see the `Map View` tab)

{{% /tab %}}
{{< /tabs >}}

Make sure you are on the **Custom Workflows** tab:
* To identify problematic user sessions, we will use the latency spikes in the **Custom Workflow Latency** chart.
* In the **Custom Workflow Duration** chart click on the **see all (1)** link under the chart title.

![RUM See All Custom Workflows](../images/rum-workflows-see-all.png)

{{% /exercise %}}
