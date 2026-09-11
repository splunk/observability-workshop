---
title: 2. Log Filtering
weight: 2
---

{{% exercise title="Filter to Error Logs" %}}

The selected trace contains log records with different severity levels. You’ll first group them by severity, then filter the results to focus on errors.
* Keep the existing trace ID search filter and time range unchanged.
* Open **Group by (1)**, search for *severity*, and select it.
* Select {{% button style="blue" %}}Apply{{% /button %}}. The chart now separates the log records by **severity**, such as *info*, *debug*, and **error**. The values shown depend on your selected trace.

Grouping helps you compare the different **severity** levels, but it does not remove records from the results. To display only error logs:

![legend](../images/severity-logs.png)

* Select **ERROR (2)** in the legend, then select **Add to filter**. Click <img src="../images/search.png" alt="Run search" style="display:inline-block; width:24px; height:auto; vertical-align:middle; margin:0 4px;"> **(3)** at the right end of the search bar.
* Confirm that the filters now include both the original *trace ID* and *severity = error*. The log table should show only error records associated with your selected trace.


{{% notice %}}
The number of matching records may differ from the screenshots. Use the severity value displayed in your environment; capitalization may vary.
{{% /notice %}}

![Error Logs](../images/log-observer-errors.png)
{{% /exercise %}}

Next, you’ll open an error record and examine its details to understand why the payment request failed.
