---
title: RUM Overview
linkTitle: 1. RUM Overview
weight: 1
time: 5 minutes
---

In this exercise, you'll open the RUM Overview dashboard. The data you'll see here was generated and also includes data from all the attendee's including yourself — it captures the browsing and shopping everyone did in the Astronomy Shop earlier, now surfaced as real user metrics like page views, errors, and load performance. This is your chance to see your own session through the lens of Real User Monitoring.

{{% exercise title="Filter to your store" %}}

* In Splunk Observability Cloud, from the main menu, hover over **Digital Experience**, then click on **Overview** **(1)** from the **Real User Monitoring** section as shown below.

![RUM](../images/rum-de.png)

* This will open up the **Application Summary Dashboard**. This section shows a quick overview of **all** the applications being monitored.

* The Real User Monitoring (RUM) Overview dashboard in Splunk Observability Cloud provides visibility into how real users experience your web applications. It captures browser-side performance metrics, JavaScript errors, and network request failures as they occur in actual user sessions. The dashboard surfaces Core Web Vitals (LCP, INP, CLS) to measure page load performance, displays error trends over time, and shows recent alerts, giving frontend teams the insights needed to identify and resolve issues affecting end-user experience.
* To make sure you're looking at the right data, filter down to your own store so the rest of the module focuses on your environment.
* Please set the filter to the following: **(2)**:
  * The **Time frame** is set to **-15m**.
  * The **Environment** selected is **[NAME OF WORKSHOP]-workshop**.
  * The **App** selected is **[NAME OF WORKSHOP]-store**.
  * The **Source** is set to **Browser**.
* Next, click on the **[NAME OF WORKSHOP]-store** **(3)** above the **Page Views / JavaScript Errors** chart.

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
