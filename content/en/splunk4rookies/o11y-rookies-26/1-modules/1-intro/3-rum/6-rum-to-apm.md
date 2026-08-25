---
title: 6. RUM to APM
weight: 6
---

{{% exercise title="Locate the failing service" %}}

* Examine the service circles in the APM Service Map. Their color indicates service health and helps identify where an error originated. A red circle marks the service identified as the source of the errors, while the red path shows how the failed requests travelled through the service dependencies.

* In this example, the **payment** service is shown as a full **red** circle, indicating that the *checkout* errors originated there. Your map may look slightly different, but the service responsible for the errors should be highlighted in the same way.

![RUM to APM](../images/rum-to-apm.png)

{{% /exercise %}}

We have now successfully navigated from **RUM** into **APM**, providing an end-to-end view of the user experience. This integration allows us to trace performance issues from the front-end all the way through to the back-end services, enabling more effective troubleshooting and optimization.

The RUM metrics initially pointed to the Checkout Service as the source of the problem. Without **APM**, teams could waste valuable time investigating this service unnecessarily. However, with **APM** we can quickly identify that the root cause actually lies in the `payment` service, saving valuable time and significantly reducing MTTx.

Let's ask our friends in back-end development to continue the investigation.
