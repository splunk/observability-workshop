---
title: 3. Synthetics to APM
weight: 3
---

We now should have a view similar to the one below.

![Place Order](../images/run-results-place-order.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* In the waterfall find an entry that starts with **POST checkout**.
* Click on the **>** button in front of it to drop open the metadata section. Observe the metadata that is collected, and note the **Server-Timing** header. This header is what allows us to correlate the test run to a back-end trace.
* Click on the blue {{% icon icon="link" %}} **APM** link on the **POST checkout** line in the waterfall.
{{% /notice %}}

![APM trace](../images/apm-trace.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Validate you see one or more errors for the **paymentservice** (**1**).
* To validate that it's the same error, click on the related content for **Logs** (**2**).
* Repeat the earlier exercise to filter down to the errors only.
* View the error log to validate the failed payment due to an invalid token.

{{% /notice %}}
