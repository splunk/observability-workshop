---
title:  Mobile Applications (Introduction)
weight: 9
---

* Short introduction to Mobile RUm
* See an overview of the performance of your Mobile Application(s)<br>
  in the Application Summary Dashboard 

---

## 1. Visit your RUM Application Summary Dashboard

Visit and login into your Splunk IMT/APM/RUM Website. From the left side menu bar select **RUM** ![RUM-ico](../../images/RUM_ico.png). This will bring you to your RUM Application Summary Page.

The goal of this page is to give you in a single pane/dashboard, a clear indication of the  health, performance and potential errors found in your application(s) and allow you dive deeper into  the information about your User Session ran against your web site.  
You will have a pane for each of your active RUM applications. (The view below is the default  expanded view)

![RUM-App-sum](../../images/Applicationsummarydashboard.png)

If you have multiple applications, the pane view may be automatically reduced by collapsing the panes as shown below:

![RUM-App-sum-collapsed](../../images/multiple_apps_collapsed.png)

You can expanded a condensed RUM Application Summary View to the full dashboard by clicking on the small browser ![RUM-browser](../../images/browser.png) or Mobile ![RUM-mobile](../../images/mobile.png)icon. (Depending on the type of application: *Mobile* or *Browser* based) on the left in front of the applications name, highlighted by the red arrow.

## 2. RUM Mobile Overview

Splunk RUM supports Native Mobile RUM, for Apple iPhone and Android Phones. You can use this to see the End-user experience of your native Smartphone app.

![RUM-Header](../../images/RUM-Mobile.png)

The above screen is to show you the various metrics and data Splunk Mobile RUM can track. For example:

* **Custom events**, similar to the Browser version.
* **App Errors** , with *App Errors* & *Crashes* per minute.
* **App Lifecycle Performance**, with *Cold Startup Time*, *Hot Startup Time* per OS.
* **Request/Response**, similar to the Browser version.

At this point we will not go deeper into Mobile RUM, due to the need to run either a native app on a phone, or run an emulation. We can provide more information in a deep dive demo if needed.
