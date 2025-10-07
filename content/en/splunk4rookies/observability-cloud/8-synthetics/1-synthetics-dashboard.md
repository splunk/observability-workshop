---
title: 1. Synthetics Dashboard
weight: 1
---

In Splunk Observability Cloud from the main menu, click on **Synthetics**. Click on **All** or **Browser tests** to see the list of active tests.

During our investigation in the RUM section, we found there was an issue with the **Place Order** Transaction. Let's see if we can confirm this from the Synthetics test as well. We will be using the metric **First byte time** for the 4th page of the test, which is the **Place Order** step.

{{% notice title="Exercise" style="green" icon="running" %}}
* In the **Search** box enter **[WORKSHOP NAME]** and select the test for your workshop (your instructor will advise as to which one to select).
* Under **Performance KPIs** set the Time Picker to **Last 1 hour** and hit enter.
* Click on **Location** and from the drop-down select **Page**. The next filter will be populated with the pages that are part of the test.
* Click on **Duration**, deselect **Duration** and select **First byte time**.
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* Look at the legend and note the color of **First byte time - Page 4**.
* Select the highest data point for **First byte time - Page 4**. You will now be taken to the **Run results** for this particular test run.
{{% /notice %}}
