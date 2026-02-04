---
title: 1. RUM Overview
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

* In Splunk Observability Cloud, from the main menu, hover over **Digital Experience**, then click on **Overview** **(1)** from the **Real User Monitoring** section as shown below.

![RUM](../images/rum-de.png)

* This will open up the **Application Summary Dashboard**. This section shows a quick overview of **all** the applications being monitored.

* The Real User Monitoring (RUM) Overview dashboard in Splunk Observability Cloud provides visibility into how real users experience your web applications. It captures browser-side performance metrics, JavaScript errors, and network request failures as they occur in actual user sessions. The dashboard surfaces Core Web Vitals (LCP, INP, CLS) to measure page load performance, displays error trends over time, and shows recent alerts, giving frontend teams the insights needed to identify and resolve issues affecting end-user experience.

* To ensure we are looking at the right data, please check the following settings **(2)**:
  * The **Time frame** is set to **-15m**.
  * The **Environment** selected is **labobs-1037**.
  * The **App** selected is **labobs-1037-store**.
  * The **Source** is set to **Browser**.
* Next, click on the **labobs-1037-store** **(3)** above the **Page Views / JavaScript Errors** chart.

![main page](../images/rum-dashboard.png)

{{% /notice %}}
