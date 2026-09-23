---
title: 3. Application View
weight: 3
time: 8 minutes
---

{{% exercise title="Explore the RUM dashboard" %}}

You are now viewing the detailed RUM dashboard for your Astronomy Shop. The filters at the top show the application, environment, data source, and time range currently being analyzed.

By default, the dashboard may compare the selected time range with an earlier period (1 day by default). This helps you recognize changes or unusual patterns in application usage, performance, and errors.

![RUM Dashboard](../images/rum-metric-map-charts.png)

The dashboard is organized into several tabs:

* **UX Metrics** — Review page views, page-load performance, route changes, and Core Web Vitals.
* **Front-end Health** — Investigate JavaScript errors and long-running browser tasks that can make the application feel slow or unresponsive.
* **Back-end Health** — Examine network requests, request errors, and Time to First Byte (TTFB), which measures how quickly the browser begins receiving a response.
* **Custom Workflows** — Review important user journeys, such as completing a purchase. The charts show request rate, errors, and duration.
* Pages — Compare traffic, performance, and Web Vitals for individual pages or groups of URLs.
* **Network Requests** — Examine the application’s network calls and their key performance and error metrics.
* **Map View** — See the geographical locations from which application activity was recorded.

Select each tab and take a moment to examine its charts. You do not need to understand every metric yet. Focus on the chart titles, their units, and any visible spikes or unusual patterns.

{{< tabs >}}
{{% tab title="Questions" %}}

1. In **Custom Workflows**, in the C**ustom Workflow Duration P75** chart, which workflow has the highest P75 duration and what evidence in the chart supports your answer?
2. In the **Map View** tab, which location shows the largest request volume??

{{% /tab %}}
{{% tab title="Answers" %}}

1. **PlaceOrder** is considerably slower. Its **P75 duration** is approximately **7.46 seconds**, with repeated spikes approaching 10 seconds, while the other workflows complete in milliseconds or microseconds. (you data may be different, but the pattern should be the same )
2. **Ireland**

{{% /tab %}}
{{< /tabs >}}

* Make sure you are on the **Custom Workflows** tab **(1)**.
* To identify problematic user sessions, we will use the latency spikes in the **Custom Workflow Duration P75** chart.
* In the **Custom Workflows Duration** chart click on the **see all** **(2)** link under the chart title.

![RUM See All](../images/rum-see-all.png)

{{< notice tip >}}
What does P75 mean?
P75 is the 75th percentile. A P75 duration of 500 milliseconds means that 75% of the recorded interactions completed in 500 milliseconds or less, while 25% took longer.
{{< /notice >}}

{{% /exercise %}}
