---
title: 2. Synthetics Browser Test
weight: 2
---



The browser test page summarizes how a synthetic user journey has performed over time and across its configured locations.

At the top, you can review *duration* trends and overall *uptime*. The *Availability* chart shows when runs succeeded or failed at each location, while *Recent* run results lists individual runs with their location, duration, and result.

{{% exercise title="Confirm the Synthetic Test Detected the Failure" %}}
* Review **Uptime Trends (1)** in the upper-right corner. The results show that approximately half of the test runs failed during the displayed periods.
* Examine the **Availability** chart **(2)**. Frequent drops to 0% and red failure markers confirm that the problem occurred repeatedly and was not limited to a single run or location.
* Compare the **uptime percentages (3)** for the different locations. The exact values may vary, but each location should show a significant number of failures.

![waterfall](../images/synthetic-browser-test.png)

#### Open a failed run
* Scroll to **Recent** run results at the bottom of the page.
* Find a row whose **Result** is **Failed (4)**, then select the **blue** timestamp for that failed run to open its detailed results.

{{% notice %}}
Test results change as new scheduled runs complete, so the percentages, locations, and timestamps may differ from the screenshot.
{{% /notice %}}

{{% /exercise %}}

Next, you’ll inspect the failed run’s screenshots, video, and individual test steps to see what the synthetic user experienced.