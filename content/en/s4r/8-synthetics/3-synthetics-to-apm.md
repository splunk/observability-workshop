---
title: 3. Synthetics to APM
weight: 3
---

We now should have a view similar to the one below.  

![Place Order](../images/run-results-place-order.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* In the waterfall find the second call out to **POST checkout**.
* Click on the **>** button on front of it to drop open the MetaData section.
* Verify that the credit card information is passed to the service.
* Close the Meta Data view and confirm you havre the same view as above.
* Click on the blue **🔗APM** link behind the **checkout** line in the waterfall
{{% /notice %}}

![apm trace](../images/apm-trace.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure you are in an APM trace view
* Validate you see errors, where we got the failure in the *payment* service
* To verify, its the same error er sre seeing, click on related content log link
* Repeat the exercise to filter down to errors only
* View the error log to validate the failed payment due to invalid Token.

{{% /notice %}}
