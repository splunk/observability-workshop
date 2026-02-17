---
title: 5. RUM to APM
weight: 5
---

{{% notice title="Exercise" style="green" icon="running" %}}

* In the **APM Service Map** you can clearly see there is an issue with the `paymentservice`.

![RUM to APM](../images/rum-to-apm.png)

{{% /notice %}}

We have now successfully navigated from **RUM** into **APM**, providing an end-to-end view of the user experience. This integration allows us to trace performance issues from the front-end all the way through to the back-end services, enabling more effective troubleshooting and optimization.

The RUM metrics initially pointed to the Checkout Service as the source of the problem. Without **APM**, teams could waste valuable time investigating this service unnecessarily. However, with **APM** we can quickly identify that the root cause actually lies in the `paymentservice`, saving valuable time and significantly reducing MTTx.

Let's ask our friends in back-end development to continue the investigation.
