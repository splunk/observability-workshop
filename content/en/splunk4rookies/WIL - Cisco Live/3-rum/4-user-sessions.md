---
title: 4. User Sessions
weight: 4
---

A **User Session** in RUM represents a single user's complete interaction with your web application from the moment they arrive until they leave or become inactive. Each session captures a timeline of all page views, user interactions (clicks, scrolls, form submissions), network requests, errors, and performance metrics.

Sessions are identified by a unique Session ID and include metadata such as browser type, device, geographic location, and custom tags. This allows you to replay and analyze the exact experience a specific user had, making it invaluable for troubleshooting issues, understanding user behavior, and identifying performance bottlenecks.

{{% notice title="Exercise" style="green" icon="running" %}}

* In the **User Sessions** table, click on the **Session ID** with the longest **Duration** (over 20 seconds or longer). This will take you to the RUM Session view.
* Note the length of the span, this is the time it took to complete the order, not good!
* Scroll down the page and you will see the **Tags** metadata (which is used in Tag Spotlight). After the tags, we come to the waterfall which shows the page objects that have been loaded (HTML, CSS, images, JavaScript etc.)
* Keep scrolling down the page until you come to a blue **APM** link (the one with `/cart/checkout` at the end of the URL) and hover over it.

![RUM Session](../images/rum-waterfall.png)

{{% /notice %}}
