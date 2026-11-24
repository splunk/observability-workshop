---
title: 5. Related Sessions
weight: 5
---

A **Related Session** or **User Session** represents one person’s activity in the application during a particular visit. Each session has a unique Session ID and contains a chronological timeline of the events captured by RUM. 

The session view brings browser activity together in one place, including page visits, clicks, form submissions, custom workflows, JavaScript errors, network requests, and performance events. At the top of the page, the Session Timeline summarizes when these events occurred. The detailed list below shows their order, duration, and status.

This view helps you move from an application-wide performance problem to the experience of an individual user. You can see what the user did, where delays or errors occurred, and—when a network request is connected to an APM trace—continue the investigation into the backend services that processed it.

{{< notice >}}
The session page may also provide a **Session Replay** option, which visually recreates the user’s interaction with the application. Session Replay is not covered in this exercise. Here, you’ll focus on the event timeline and use it to follow a slow checkout request from RUM into APM. 
{{< /notice >}}

{{% exercise title="Investigate a Slow PlaceOrder Interaction" %}}

In the previous exercise you filtered RUM data to **PlaceOrder** and sorted **Related Sessions** by duration. Now open one of those slow sessions and follow the checkout from the browser into APM.

* In the **Related Sessions** table, select the **Session ID** with the longest **PlaceOrder** duration. Prefer a session longer than **6 seconds**. If none are that slow, pick the longest one in the list. Your times may differ from the screenshots.

The session page opens. The top of the page may show **Session Replay**, a video of the user’s visit. You do not need it for this exercise.

* Scroll down until you see the **Navigation** waterfall **(1)**. This timeline lists the pages, custom events, and network requests from that visit.

If the waterfall is long and hard to scan, keep only the events that matter for checkout:

* Open the **Category** filter **(2)**.
* Select **Custom** and **Network** **(3)**. Leave the other categories unchecked.

**Custom** includes workflows such as **PlaceOrder**. **Network** includes the HTTP requests the browser made, including checkout.

![RUM session flow](../images/rum-user-session-flow.webp)

* Locate the *PlaceOrder* custom section.
* Review its **duration**. The length of the bar shows how long the workflow took to complete. A long bar confirms that this user experienced a slow checkout interaction.
* Near the *PlaceOrder* Custom Event, locate the **Fetch (1)** event for the checkout request. Depending on the order of events in your session, it may appear immediately above or below *PlaceOrder*.  
It should start with:
  `POST https://<your-store>/api/checkout`.

![RUM Session](../images/rum-waterfall-place-order.webp)

* Check the request’s status code. An *HTTP status code* of **500** indicates that the backend encountered an error while processing the request.
* Select the blue **APM** link **(2)** and wait for the performance summary pane to appear. This summary connects the browser request to the backend trace that processed it.

![RUM Session](../images/rum-performance.webp)

* Review the services shown at the bottom of the summary. A red error indicator identifies a service containing one or more errors. In this example, errors are associated with services such as *checkout* or *payment* **(3)**. The exact services and order may differ in your session. 

* Select the **Business Operation** (also called a business workflow) by clicking the blue link **(4)**. The name may be `PlaceOrder`, `checkout:oteldemo.CheckoutService/PlaceOrder`, or another label used in your environment — click the blue text next to **Business Operation**. This opens the APM Service Map, where you will investigate the backend services and their dependencies.

{{% /exercise %}}
