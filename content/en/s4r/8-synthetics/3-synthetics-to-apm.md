---
title: 3. Synthetics to APM
weight: 3
---

We now should have a view similar to the one below.

![Place Order](../images/run-results-place-order.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* In the waterfall find the second call out to **POST checkout**.
* Click on the **>** button in front of it to drop open the metadata section.
* Verify that the credit card information is passed to the service.
* Close the Meta Data view and confirm you have the same view as above.
* Click on the blue {{% icon icon="link" %}} **APM** link on the **POST checkout** line in the waterfall.
{{% /notice %}}

![APM trace](../images/apm-trace.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure you are in an APM trace view.
* Validate you see errors for the **paymentservice**.
* To validate that it's the same error, click on the **Related Content** log link.
* Repeat the earlier exercise to filter down to the errors only.
* View the error log to validate the failed payment due to an invalid token.

{{% /notice %}}