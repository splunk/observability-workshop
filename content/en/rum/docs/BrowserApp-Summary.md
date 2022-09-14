---
title: Check Browser Applications health at a glance
weight: 2
---

* Get familiar with the UI and options available from this landing page
* Identify Page Views/Errors and Request/Errors and Java Script Errors in a single view </br>
  Check the Web Vitals metrics and any Detector that has fired for in relation to your Browser Application

---

## 1. Browser Application Summary Dashboard Overview

### 1.1. Header Pane

As seen in the previous section the RUM Application Summary Dashboard consists of 5 major sections.</br>
The first section is the selection header, where you can collapse the Pane via the ![RUM-browser](../../images/browser.png) Browser icon or the **>** in front of the application name. which is *jmcj-rum-app* in the example below. 
It also provides access to the Detailed Application Overview page if you click the link with your application name wich is *jmcj-rum-app* in the example below. 

Further, you can also visit/open the Application Overview Page and an App Health Dashboard via the hamburger ![trippleburger](../../images/trippleburger.png) menu on the right by selecting *View Dashboard*

![RUM-SummaryHeader](../../images/summaryHeader.png)

Please visit the Detailed Overview page for a moment, then use the back button of your browser to return the landing page, then open the Browser App Health Dashboard for a quick visit (note: this dashboard will open in a new page, find the tab with the RUM landing page (Entitled **RUM**) and select it again).

We will looking at the Detail Overview page and the Browser App Health Dashboard in detail in one of the next sections).

### 1.3. Chart Area
The second section of the RUM Application Summary Dashboard is focused on providing you in a single glance the relation between Pageviews and Errors & Network request and errors occurring in your application. This can be Javascript errors, or failed  network calls to back end services

![RUM-chart](../../images/Rum-chart.png)

In the example above you can see that there are no failed network calls in the bottom chart, but in the PageView chart you can see that a number of page chart do experienced some errors. These are often not visible for regular users, but can seriously impact the performance of your web site. 

You can see the count of the Pageviews/network invocations and errors by clicking in the chart.

![RUM-chart-clicked](../../images/RumChart-clicked.png)

### 1.4. Java Script Errors
With the third section of the RUM Application Summary Dashboard we are showing you an overview of the Javascript errors occurring in your application as wel of a count of each error. In the example below you can see that there are three error locations 

![RUM-javascript](../../images/RUM-Javascripterrors.png)

In the example above you can see there are three Java script errors, one that appears 29 times in the selected time slot, andd the two other appear 12 times each.
If you click on one of the errors a new page opens that will show a chart showing you the count over time, and  the stack trace of the javascript error, giving you and indication where the problem happened. ( We will see this in more detail in one of the next sections.)

![RUM-javascript-chart](../../images/expandedRUmJAVAscript-error.png)

### 1.5. Web Vitals
The forth section of the RUM Application Summary Dashboard is showing you the crucial (google) Web Vitals, three metrics, that are used by Google in its ranking system, and give a very good indication of the speed  of your site for your end users. 

![WEB-vitals](../../images/RUM-QuickWebVitals.png)

As you can see our site is wel behaved and scores *Good* for all three Metrics. If it would be different, these metrics can be used to identify the effect changes to you application have, and help you improve the performance of your site. 

If you click on any of the Metrics show in the webVitals pane you will be taken to the corresponding Tag Spot light Dashboard.  If you click on the Large Contentful Paint (LCP) metric, you will be taken to a dashboard similar to the screen shot below, that give you an insight and trend view fof how this metric varied, allowing you to identify trends where the problem may originate from like a region, OS version or browser version for example.

![WEB-vitals-tag](../../images/RUM-WVTAG.png)

### 1.6. Most Recent Detectors
The last section of the RUM Application Summary Dashboard is focused on providing you  an overview of any detector that has triggered for you application.
We have created a detector for this screen shot  and very likely your pane will be empty now  but we will add some detectors to you site and make sure they are triggered in one of the next sections 

![detectors](../../images/rum-detector.png)

In the screen shot you can see we have a critical alert for the *RUM Aggregated View Detector*,  and a Count, how often this alert has triggered in the selected time window. If you click on the  name of the Alert (that is shown as a blue link)  you will be taken to the Alert over view page and show the details of the alert (Note: this will move you away from the current page, Please use the **Back** option of your browser to return to the overview page) 

![alert](../../images/click-alert.png)
---
Please take a few minutes to experiment with the RUM Application Summary Dashboard  and the underlying chart and dashboards before going on to the next section.