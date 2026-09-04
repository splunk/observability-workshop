---
title: 4. Synthetics to APM
weight: 4
---
The synthetic run shows that checkout failed, but its waterfall also provides a connection to the corresponding back-end trace. You’ll use this connection to verify whether the synthetic failure is associated with the same payment problem found earlier.

{{% exercise title="Follow the failed test into APM" %}}

* In the waterfall, locate the request beginning with `POST checkout`. You may need to scroll down to find it. If it is not present, return to the test results and open another failed run.

![Place Order](../images/run-results-place-order.png)

* Select the blue **APM** (2) link on the `POST checkout` request. The corresponding distributed trace opens in **APM**. 
* In the **Trace Flow**, locate the **payment** service **(3)** and confirm that it is marked as having errors. You may need to pan the map to locate the service.
* In the **Trace Waterfall**, locate the `checkout` branch and its **error marker (4)**. This identifies where the back-end request failed.
* At the bottom of the waterfall, select *Logs*, which may display a count of available related logs. Then select the **Logs for trace… (5)** link from the **Related Logs** pop-up.
* As in the earlier **Logs** exercise, filter the correlated records to display only errors, then open a payment error record.

![APM trace](../images/apm-trace.png)

{{< tabs >}}
{{% tab title="Question" %}}
* **Does the log record show that this synthetic failure was caused by the same payment error found earlier?** 
{{% /tab %}}
{{% tab title="Answers" %}}
**Yes. The correlated payment log reports that the payment failed because the request contained an invalid API token, confirming that the synthetic test detected the same underlying problem.**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
