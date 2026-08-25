---
title: 5. User Sessions
weight: 5
---

A **User Session** represents one person’s activity in the application during a particular visit. Each session has a unique Session ID and contains a chronological timeline of the events captured by RUM. 

The session view brings browser activity together in one place, including page visits, clicks, form submissions, custom workflows, JavaScript errors, network requests, and performance events. At the top of the page, the Session Timeline summarizes when these events occurred. The detailed list below shows their order, duration, and status.

This view helps you move from an application-wide performance problem to the experience of an individual user. You can see what the user did, where delays or errors occurred, and—when a network request is connected to an APM trace—continue the investigation into the backend services that processed it.

{{< notice >}}
The session page may also provide a **Session Replay** option, which visually recreates the user’s interaction with the application. Session Replay is not covered in this exercise. Here, you’ll focus on the event timeline and use it to follow a slow checkout request from RUM into APM. 
{{< /notice >}}

{{% exercise title="Investigate a Slow PlaceOrder Interaction" %}}

You previously filtered the data to **PlaceOrder** and sorted the results by duration. You’ll now inspect one of the slowest interactions and follow its checkout request from RUM into APM.
* In the **User Sessions** table, select the **Session ID** associated with the longest *PlaceOrder* duration. Preferably select a duration longer than **6 seconds**. If none are available, select the longest duration shown. Your values may differ from the screenshots.
* The RUM session view opens. Locate the *PlaceOrder* span in the session timeline.

![RUM Session](../images/rum-waterfall-place-order.png)

* Review its **duration**. The length of the bar shows how long the workflow took to complete. A long bar confirms that this user experienced a slow checkout interaction.
* Near the *PlaceOrder* span, locate the **Fetch (1)** event for the checkout request. Depending on the order of events in your session, it may appear immediately above or below *PlaceOrder*.  
It should start with:
  `POST https://<your-store>/cart/checkout`.
* Check the request’s status code. An *HTTP status code* of **500** indicates that the backend encountered an error while processing the request.
* Select the blue **APM** link **(2)** and wait for the performance summary to appear. This summary connects the browser request to the backend trace that processed it.

![RUM Session](../images/rum-waterfall.png)

* Review the services shown at the bottom of the summary. A red error indicator identifies a service containing one or more errors. In this example, errors are associated with services such as *checkout* or *payment* **(3)**. The exact services and order may differ in your session. 
* Under **Business Operation**,  select `PlaceOrder`(4) to open the APM Service Map for this business operation. There, you’ll investigate the backend services and their dependencies to identify the root cause of the slow or failed checkout request.

{{% /exercise %}}
