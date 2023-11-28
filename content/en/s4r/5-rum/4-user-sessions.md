---
title: 4. User Sessions
weight: 4
---

Close the RUM Session Replay by clicking on the **X** in the top right corner. Here, we can see the custom event **PlaceOrder**. (If it is not immediately visible, type `PlaceOrder` in the search bar below thh Session replay section. Use the **⌵** & **⌃**  to find the longest one.) Notice the length of the span. This is the time it took to complete the order, not good!

{{% notice title="Exercise" style="green" icon="running" %}}

* Scroll down the page and you will see the **Tags** metadata (which is used in Tag Spotlight). After the tags, we come to the waterfall which shows the page objects loading (CSS, images, JavaScript etc.)
* Scroll back up to the top of the metrics section and hover over the blue **APM** link (the one next to `Doc Fetch` with `/cart/checkout` at the end of the URL).

{{% /notice %}}

![RUM Session](../images/rum-waterfall.png)

This brings up the APM Performance Summary. Having this end-to-end (RUM to APM) view is very useful when troubleshooting issues.

{{% notice title="Exercise" style="green" icon="running" %}}

* You will see **paymentservice** and **checkoutservice** are in an error state as per the screenshot above.
* Under **Workflow Name** click on `front-end:/cart/checkout`, this will bring up the **APM Service Map**.

{{% /notice %}}

![RUM to APM](../images/rum-to-apm.png)
