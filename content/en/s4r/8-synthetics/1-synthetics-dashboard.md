---
title: 1. Synthetics Dashboard
weight: 1
---

In Splunk Observability Cloud from the main menu, click on **Synthetics**. Click on **All** or **Browser tests** to see the list of active tests:

During our investigation in the RUM section, we found there was an issue with the **Place Order** Transaction. Let's see if we can confirm this from the Synthetics test as well.

In the **Search** box enter **Workshop Browser Test** and select the test for your workshop (your instructor will advise as to which one to select).

{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure the page you are looking at is the result page for the **Workshop Browser Test for [NAME OF WORKSHOP]**
* Under **Performance KPIs** set the Time Picker to **-1h** and hit enter.
* From the **Location** drop-down select **Synthetic transactions**.
* Looking at the dots, which transaction has a performance issue?
* Next, change the Time Picker to **-15m** and hit enter.
* Change the filtering so that only **Place Order** is visible by removing all other transactions from the drop-down.
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* As you move your mouse pointer horizontally across the chart a vertical line will appear showing the duration and the time of the test.
* What can you conclude about the relation of the dots and the red **X** at the bottom?
* Change the filter to just *Keep Browsing*, the dots will change both pattern and color.
* Select a successful test dot. (One that has no red X beneath it). If there are multiple tests in that time range you will be presented with a list of tests. Pick one that is 20 seconds or longer and results in ✅ Success.
  ![Duration - Place Order](../images/duration-place-order.png)
{{% /notice %}}

![Results](../images/select-result.png)

This will take you to the Synthetic Test Details or Waterfall. If the Waterfall has a Red Banner like this on top:

![error](../images/run-result-error.png?classes=left)

You accidentally picked a test that had an error, it timed out. (This can happen as new tests are added and the UI just refreshed). In that case, use the browser back button and try again.
