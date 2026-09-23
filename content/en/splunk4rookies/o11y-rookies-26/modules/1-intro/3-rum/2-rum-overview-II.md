---
title: Explore your Store data
linkTitle: 2. Explore your Store
weight: 2
time: 5 minutes
---

{{< notice tip >}}
The rum application  we used in the screenshots below is named **workshop**, so **workshop-store** is used as the example application name.  
Replace [NAME OF WORKSHOP] with the workshop name assigned to you by your instructor.
{{< /notice >}}

{{% exercise title="Filter to your store" %}}

* To display the data for your own Astronomy Shop, configure the filters marked (2) as follows:
  * Set the **Time frame** to **-15m**.
  * Set **Environment** to **[NAME OF WORKSHOP]-workshop**.
  * Set **App** to **[NAME OF WORKSHOP]-store**.
  * Set **Source** to **Browser**.

* Take a moment to review the resulting dashboard. You should see information including:
  * Page Views and JavaScript Errors, showing application activity and browser-side errors over time.
  * Network Requests and Errors, showing requests made by the application and any failures.
  * JavaScript Errors, including how frequently each error occurred and when it was last detected.
  * Web Vitals, indicating the application’s loading performance, responsiveness, and visual stability.
  * Most Recent Alerts, showing any active alerts associated with the application.  

* Next, click on the **[NAME OF WORKSHOP]-store** **(3)** above the **Page Views / JavaScript Errors** chart to dive into the the data.

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
