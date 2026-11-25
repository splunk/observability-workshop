---
title: 3. Application View
weight: 3
time: 8 minutes
---

{{% exercise title="Explore the RUM dashboard" %}}

You are now viewing the detailed RUM dashboard for your Astronomy Shop. The filters at the top show the application, environment, data source, and time range currently being analyzed.

By default, the dashboard may compare the selected time range with an earlier period (1 day by default). This helps you recognize changes or unusual patterns in application usage, performance, and errors.

![RUM Dashboard](../images/rum-metric-map-charts.webp)

The dashboard is organized into several tabs:

* **UX Metrics** — Review page views, page-load performance, route changes, and Core Web Vitals.
* **Front-end Health** — Investigate JavaScript errors and long-running browser tasks that can make the application feel slow or unresponsive.
* **Back-end Health** — Examine network requests, request errors, and Time to First Byte (TTFB), which measures how quickly the browser begins receiving a response.
* **Custom Workflows** — Review important user journeys, such as completing a purchase. The charts show request rate, errors, and duration.
* **Pages** — Compare traffic, performance, and Web Vitals for individual pages or groups of URLs.
* **Network Requests** — Examine the application’s network calls and their key performance and error metrics.
* **Map View** — See the geographical locations from which application activity was recorded.

Select each tab and take a moment to examine its charts. You do not need to understand every metric yet. Focus on the chart titles, their units, and any visible spikes or unusual patterns.

{{< quiz question="In the Custom Workflow Duration P75 chart, which workflow has the highest P75 duration?" >}}
{{< quiz-option >}}AddToCart{{< /quiz-option >}}
{{< quiz-option correct=true >}}PlaceOrder{{< /quiz-option >}}
{{< quiz-option >}}CheckoutError{{< /quiz-option >}}
{{< quiz-option >}}OrderConfirmed{{< /quiz-option >}}
{{< quiz-feedback >}}
**PlaceOrder** is considerably slower than the other workflows. Its **P75 duration** is several seconds, with repeated spikes approaching 10 seconds, while the other workflows complete in milliseconds. Your values may differ, but the pattern should be the same.
{{< /quiz-feedback >}}
{{< /quiz >}}

Open the **Map View** tab and note which locations your application activity is coming from. Your results depend on where you and other attendees are browsing from.

* Make sure you are on the **Custom Workflows** tab **(1)**.
* To identify problematic user sessions, we will use the latency spikes in the **Custom Workflow Duration P75** chart.
* In the **Custom Workflows Duration** chart click on the **see all** **(2)** link under the chart title.

![RUM See All](../images/rum-see-all.webp)

{{< notice tip >}}
What does P75 mean?
P75 is the 75th percentile. A P75 duration of 500 milliseconds means that 75% of the recorded interactions completed in 500 milliseconds or less, while 25% took longer.
{{< /notice >}}

{{% /exercise %}}
