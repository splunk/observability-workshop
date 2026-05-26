---
title: 4. User Sessions
weight: 4
---
{{% exercise title="Find the APM jump-off point" %}}

* Close the RUM Session Replay by clicking on the **X** in the top right corner.
* Note the length of the span, this is the time it took to complete the order, not good!
* Scroll down the page and you will see the **Tags** metadata (which is used in Tag Spotlight). After the tags, we come to the waterfall which shows the page objects that have been loaded (HTML, CSS, images, JavaScript etc.)
* Keep scrolling down the page until you come to a blue **APM** link (the one with `/cart/checkout` at the end of the URL) and hover over it.

{{% /exercise %}}

![RUM Session](../images/rum-waterfall.png)

This brings up the APM Performance Summary. Having this end-to-end (RUM to APM) view is very useful when troubleshooting issues.

{{% exercise title="Jump from RUM to APM" %}}

* You will see **paymentservice** and **checkoutservice** are in an error state as per the screenshot above.
* Under **Workflow Name** click on `front-end:/cart/checkout`, this will bring up the **APM Service Map**.

{{% /exercise %}}

![RUM to APM](../images/rum-to-apm.png)
