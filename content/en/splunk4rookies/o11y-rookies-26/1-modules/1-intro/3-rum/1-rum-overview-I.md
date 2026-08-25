---
title: "Open the RUM  Overview"
linkTitle: 1. Open RUM Overview
weight: 1
time: 5 minutes
---

In this exercise, you'll open the RUM Overview dashboard. The data you'll see here was generated and also includes data from all the attendee's including yourself — it captures the browsing and shopping everyone did in the Astronomy Shop earlier, now surfaced as real user metrics like page views, errors, and load performance. This is your chance to see your own session through the lens of Real User Monitoring.

{{% exercise title="Open the RUM Overview" %}}

* In Splunk Observability Cloud, from the main menu, hover over **Digital Experience**, then click on **Overview** **(1)** from the **Real User Monitoring** section as shown below.

![RUM](../images/rum-dea.png)

* This opens the Real User Monitoring (RUM) Overview, where the Application Summary Dashboard provides a quick overview of all monitored web applications.

* The dashboard shows how real users experience the Astronomy Shop. It captures browser activity such as page views, frontend performance, JavaScript errors, and failed network requests. It also displays Core Web Vitals—Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS)—together with error trends and recent alerts.

* The activity you generated earlier by browsing the catalog and completing purchases contributes to the RUM data summarized on this dashboard. If the shop was accessed from different browsers, mobile phones, or tablets, those interactions also contribute RUM data and can be explored in more detail later in the workshop.

{{% /exercise %}}
