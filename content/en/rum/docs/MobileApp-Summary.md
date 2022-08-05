---
title:  Check Mobile Applications health at a glance
weight: 3
---

* See an overview of the performance of all your application(s)<br>
  in the Application Summary Dashboard (Both Mobile and Web based)

---

## 1. Visit your RUM Application Summary Dashboard

Visit and login into your Splunk IMT/APM/RUM Website. From the left side menu bar select **RUM** ![RUM-ico](../../images/RUM_ico.png). This will bring you to your RUM Application Summary Page.

The goal of this page is to give you in a single pane/dashboard, a clear indication of the  health, performance and potential errors found in your application(s) and allow you dive deeper into  the information about your User Session ran against your web site.  
You will have a pane for each of your active RUM applications. (The view below is the default  expanded view)

![RUM-App-sum](../../images/Applicationsummarydashboard.png)

If you have multiple applications, the pane view may be automatically reduced by collapsing the panes as shown below:

![RUM-App-sum-collapsed](../../images/multiple_apps_collapsed.png)

You can expanded a condensed RUM Application Summary View to the full dashboard by clicking on the small browser ![RUM-browser](../../images/browser.png) or Mobile ![RUM-mobile](../../images/mobile.png)icon. (Depending on the type of application: *Mobile* or *Browser* based) on the left in front of the applications name, highlighted by the red arrow.

## 2. RUM Application Summary Dashboard Overview

### 2.1. Header Section

The RUM Application Summary Dashboard consists of 6 major sections. The first is the selection header, where you can set/filter a number of options:

* A drop down for the time window you're reviewing (You are looking at the past 15 minutes by default)
* A drop down to select the Environment[^1] you want to look at.</br>
  (This allows you to focus on just the subset of application belonging to that environment).
* A drop down with the available Environments to view:  (Choose the one provided by the workshop host or *Select all* for the workshop)
* A drop down list with the various web apps being monitored (You    can use the one provided by the workshop host or use *Select all*)</br>
This will focus you on just 1 (One) application.</br>
For the workshop make sure you can use the one provided by the workshop host or or *Select all*.  
* A drop down to select the source type  *Browser* or *Mobile* applications to view</br> For the Workshop  select *All* as the source.
* A hamburger menu located at the right of the header allowing to configure some settings of your Splunk RUM application. (we will visit this in a later section).

![RUM-SummaryHeader](../../images/RUM_SummaryHeader.png)

### 2.2. Overview Pane

The next section is the overview pane:
This pane will give you a quick indication to the pages with highest increase in load times (75 percentile or higher)  
The **Highest P75 Page Load Times** window will show you in a quick view if the load time of your top pages has increased or has an error.

In the example here you can see that the first page has an error due to the red square, and you can see that the load time has drastically increased by more than 8 seconds.

![RUM-Top](../../images/RUM-TOP.png)

You also see an overview of the number of Front end Error and Backend Errors  per minute.

The last two panes show you the **Top Page Views** and the **Top Providers**.

### 2.3. Custom Event Pane

The Custom Event View is the location where you will find the metrics for any event you may have added yourself to the web pages you are monitoring.

As we have seen in the RUM enabled website, we have added the follwoing two lines:

```javascript
const Provider = SplunkRum.provider;
var tracer=Provider.getTracer('appModuleLoader');
```

These lines  will automatically create custom Events for every new Page, and you can also add these to pieces of custom code that are not part of a framework or an event you created so you can better understand the flow though your application.
We support **Event Request rate**, **Event Error Rates** and **Event Latency** metrics.

These will help better understand the flow of your website and allows you increase conversions.

![RUM-CustomMetrics](../../images/RUM-Custom-Events.png)

### 2.4. Key Metrics Pane

The Key Metrics View is the location where you will find the metrics for the number of
**Frontend Errors** per second, **Endpoint Errors** per second an the **Endpoint Latency**.
These Metrics are very useful to guide you to the location of an issue if you are experiencing problems with your site.

![RUM-KeyMetrics](../../images/RUM-Key-Metrics.png)

### 2.5. Web Vitals Pane

The Web Vitals view is the location where you go if you wish to get insight into the experience you are delivering to your End users based on Web Vitals metrics.
Web Vitals is an initiative by Google to provide unified guidance for quality signals that are essential to delivering a great user experience on the web and focuses on three key parameters:

* Largest Contentful Paint (LCP): measures loading performance. To provide a good user experience, LCP should occur within 2.5 seconds of when the page first starts loading.
* First Input Delay (FID): measures interactivity. To provide a good user experience, pages should have a FID of 100 milliseconds or less.
* Cumulative Layout Shift (CLS): measures visual stability. To provide a good user experience, pages should maintain a CLS of 0.1. or less.

![RUM-WebVitals](../../images/RUM-Web-Vitals.png)

### 2.6. Other Metrics Pane

The Other Metrics Pane is the location where you find an other set of performance metrics, with a focus on initial load time of you page or showing you task that are longer then others.

* **Time To First Byte (TTFB)**, Time to First Byte (TTFB) measures how long it takes for a client's browser to receive the first byte of the response from the server. The longer it takes for the server to process the request and send a response, the slower your visitors' browsers start displaying your page.
* **Long Task Length**, a performance metric that can be used help developers to understand the bad user experience on the website, or can be an indication of a problem.
* **Long Task Count**, A metric to indicate how often a long task occurs, again used for exploring user experiences or problem detection.

![RUM-Other](../../images/RUM-Other.png)

## 3. RUM Mobile Overview

Splunk RUM supports Native Mobile RUM, for Apple iPhone and Android Phones. You can use this to see the End-user experience of your native Smartphone app.

![RUM-Header](../../images/RUM-Mobile.png)

The above screen is to show you the various metrics and data Splunk Mobile RUM can track. For example:

* **Custom events**, similar to the Browser version.
* **App Errors** , with *App Errors* & *Crashes* per minute.
* **App Lifecycle Performance**, with *Cold Startup Time*, *Hot Startup Time* per OS.
* **Request/Response**, similar to the Browser version.

At this point we will not go deeper into Mobile RUM, due to the need to run either a native app on a phone, or run an emulation. We can provide more information in a deep dive demo if needed.
