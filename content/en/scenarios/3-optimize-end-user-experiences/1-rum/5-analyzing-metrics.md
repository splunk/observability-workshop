---
title: 5. Analyzing RUM Metrics
weight: 5
---

* See RUM Metrics and Session information in the RUM UI
* See correlated APM traces in the RUM & APM UI

---

## 1. RUM Overview Pages

From your RUM Application Summary Dashboard you can see detailed information by opening the Application Overview Page via the tripple dot ![trippleburger](../images/trippleburger.png?classes=inline&height=25px) menu on the right by selecting *Open Application Overview* or by clicking the link with your application name which is *jmcj-rum-app* in the example below.

![RUM-SummaryHeader](../images/summaryHeader.png)

This will take you to the RUM Application Overview Page screen as shown below.

![RUM app overview with UX metrics](../images/rum-ux-metrics.png)

## 2. RUM Browser Overview

### 2.1. Header

The RUM UI consists of 6 major sections. The first is the selection header, where you can set/filter a number of options:

* A drop down for the time window you're reviewing (You are looking at the past 15 minutes in this case)
* A drop down to select the Comparison window (You are comparing current performance on a rolling window   - in this case compared to 1 hour ago)
* A drop down with the available Environments to view
* A drop down list with the Various Web apps
* ***Optionally*** a drop down to select Browser or Mobile metrics (*Might not be available in your workshop*)

![RUM-Header](../images/rum-header.png)

### 2.2. UX Metrics

By default, RUM prioritizes the metrics that most directly reflect the experience of the end user. 

{{% notice title="Additional Tags" style="info" %}}
All of the dashboard charts allow us to compare trends over time, create detectors, and click through to further diagnose issues.
{{% /notice %}}

First, we see page load and route change information, which can help us understand if something unexpected is impacting user traffic trends.

![Page load and route change charts](../images/page-load-route-change.png)

Google has defined Core Web Vitals to quantify the user experience as measured by loading, interactivity, and visual stability.

![Core Web Vitals charts](../images/core-web-vitals-overview.png)

* **Largest Contentful Paint (LCP)**, measures loading performance. How long does it take for the largest block of content in the viewport to load? To provide a good user experience, LCP should occur within 2.5 seconds of when the page first starts loading.
* **First Input Delay (FID)**, measures interactivity. How long does it take to be able to interact with the app? To provide a good user experience, pages should have a FID of 100 milliseconds or less.
* **Cumulative Layout Shift (CLS)**, measures visual stability. How much does the content move around after the initial load? To provide a good user experience, pages should maintain a CLS of 0.1. or less.

Google has some great resources if you want to learn more, for example [the business impact of Core Web Vitals](https://web.dev/case-studies/vitals-business-impact).

### 2.3. Front-end health

Common causes of frontend issues are javascript errors and long tasks, which can especially affect interactivity. Creating detectors on these indicators helps us investigate interactivity issues sooner than our users report it, allowing us to build workarounds or roll back related releases faster if needed. Learn more about [optimizing long tasks](https://web.dev/articles/optimize-long-tasks) for better end user experience!

![JS error charts](../images/rum-js-errors.png)
![Long task charts](../images/rum-long-tasks.png)


### 2.4. Back-end health

Common back-end issues affecting user experience are network issues and resource requests. In this example, we clearly see a spike in Time To First Byte that lines up with a resource request spike, so we already have a good starting place to investigate.

![Back-end health charts](../images/rum-be-health.png)

* **Time To First Byte (TTFB)**, measures how long it takes for a client's browser to receive the first byte of the response from the server. The longer it takes for the server to process the request and send a response, the slower your visitors' browser is at displaying your page.

### 2.6. Custom Events

The Custom Events tab is where you will find the metrics for any event you may have added yourself to the web pages you are monitoring. See the docs for an [example scenario instrumenting Custom Events for RUM](https://docs.splunk.com/observability/en/rum/rum-scenario-library/spa-custom-event.html#create-a-custom-event-to-measure-user-engagement-on-blog-posts).

As we have seen in the RUM enabled website, we have added the following two lines:

```javascript
const Provider = SplunkRum.provider;
var tracer=Provider.getTracer('appModuleLoader');
```
These lines  will automatically create custom Events for every new Page, and you can also add these to pieces of custom code that are not part of a framework or an event you created so you can better understand the flow though your application. We support **Custom Event Requests**, **Custom Event Error Rates** and **Custom Event Latency** metrics.

![RUM custom event charts](../images/rum-custom-events.png)
