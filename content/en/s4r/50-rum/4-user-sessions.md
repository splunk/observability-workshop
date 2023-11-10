---
title: 4. User Sessions
weight: 4
---

21. Click on the workflow ensuring it says **frontend:/cart/checkout**
22. Move on to APM

Close the RUM Session Replay by clicking on the **X** in the top right corner. Here, we can see the custom event **PlaceOrder**. Notice the length of the span. This is the time it took to complete the order, not good!

Next, scroll down the page and you will see the **Tags** metadata (which is used in Tag Spotlight). After the tags, we come to the waterfall which shows the page objects loading (CSS, images, JavaScript etc.)

Hover over the 1st blue **APM** link (the one next to `Doc Fetch` with `/cart/checkout` at the end of the URL).

![RUM Session](../images/rum-waterfall.png?width=40vw)

This brings up the APM Performance Summary. Having this end-to-end (RUM to APM) view is very useful when troubleshooting issues.

You should see **paymentservice** and **checkoutservice** are in an error state as per the screenshot above. Under **Workflow Name** click on **frontend:/cart/checkout**. This will bring up the APM Service Map.

![RUM to APM](../images/rum-to-apm.png?width=40vw)
