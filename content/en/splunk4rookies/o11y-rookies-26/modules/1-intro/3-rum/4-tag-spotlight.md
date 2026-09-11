---
title: 4. Tag Spotlight
weight: 4
time: 5 minutes
---

**Tag Spotlight** helps you explore the tags attached to your RUM data. Tags are key-value pairs that describe each interaction, such as its workflow name, application, environment, browser, operating system, or location.
The panels show the most common values for each tag and their associated performance percentiles, including **P50**, **P75**, and *P99*. You can select a value and add it as a filter without writing a query. This makes it easier to narrow the data from an application-wide overview to a particular workflow or group of user sessions.

{{% exercise title="Find slow PlaceOrder sessions" %}}

In this exercise, you’ll use **Tag Spotlight** to focus on the **PlaceOrder** workflow. You’ll then open the matching user sessions and sort them to find the slowest interactions.

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* Change the timeframe to **Last 1 hour** **(1)**.

* Find the **Custom Workflow Name** chart, locate **PlaceOrder** in the list **(2)**, click on it and select **Add to filter** **(3)** in the popup window to apply the filter to the page.
* Confirm that the **PlaceOrder** filter appears at the end of the filter pane at the top of the page **(1)**.  
The charts and results now focus on interactions associated with this workflow.
* Select the **User Sessions** tab (4).
* Select the **Duration** column heading (5) until the longest durations appear at the top. A *downward arrow* indicates that the results are sorted from longest to shortest.

* You now have a list of **sessions** containing the **PlaceOrder** workflow, with the slowest interactions shown first. The results were narrowed using the PlaceOrder tag before you opened the User Sessions tab. We could apply more filters to further narrow down the data, e.g. *OS version*, *browser version*, etc.

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
