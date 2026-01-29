---
title: 3. Synthetics to APM
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

* In the waterfall find an entry that starts with **POST checkout**.

![Place Order](../images/run-results-place-order.png)

* Click on the **>** to open the metadata section. Observe the metadata that is collected, and note the **Server-Timing** header. This header is what allows us to correlate the test run to a back-end trace.
* Click on the blue {{% icon icon="link" %}} **APM** link on the **POST checkout** line in the waterfall.

![APM trace](../images/apm-trace.png)

* Validate you see one or more errors for the **paymentservice**.
* To validate that it's the same error, click on the related content for **Logs**.
* Repeat the earlier exercise to filter down to the errors only.
* View the error log to validate the failed payment due to an invalid token.

{{% /notice %}}
