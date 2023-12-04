---
title: 4. User Sessions
weight: 4
---
{{% notice title="Exercise" style="green" icon="running" %}}

* Close the RUM Session Replay by clicking on the **X** in the top right corner. We had set a filter on **PlaceOrder** in the previous exercise. It should be selected here as well, as shown in the screenshot below (**1**).
* Note the length of the span, this is the time it took to complete the order, not good!
* Scroll down the page and you will see the **Tags** metadata (which is used in Tag Spotlight). After the tags, we come to the waterfall which shows the page objects that have been loaded (HTML, CSS, images, JavaScript etc.)
* Keep scrolling down the page until you come to a blue **APM** link (the one with `/cart/checkout` at the end of the URL) and hover over it.

{{% /notice %}}

![RUM Session](../images/rum-waterfall.png)

This brings up the APM Performance Summary. Having this end-to-end (RUM to APM) view is very useful when troubleshooting issues.

{{% notice title="Exercise" style="green" icon="running" %}}

* You will see **paymentservice** (**2**) and **checkoutservice** (**3**) are in an error state as per the screenshot above.
* Under **Workflow Name** click on `front-end:/cart/checkout`, this will bring up the **APM Service Map**.

{{% /notice %}}

![RUM to APM](../images/rum-to-apm.png)
