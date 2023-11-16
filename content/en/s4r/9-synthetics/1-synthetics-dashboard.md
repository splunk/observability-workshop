---
title: 1. Synthetics Dashboard
weight: 1
---
1. Go to Synthetics
2. Your instructor will highlight which Synthetic test to use
3. Click on the test
4. Note: be aware of screenshot for this step
5. Change to last hour

In Splunk Observability Cloud from the main menu, click on *Synthetics*. Click on All or Browser test to see the list of active tests:

This view has already been covered in the short introduction earlier. To continue, select the ***Workshop Browser Test for [NAME OF WORKSHOP]*** from the Test Pane.

During our investigation  in the RUM section, we found there was an issue with the *Place Order* Transaction, Lets see if we can confirm this from the Synthetics tests as well.
{{% notice title="Exercise" style="green" icon="running" %}}

* Make sure the page you are looking at is the result page for the **Workshop Browser Test for [NAME OF WORKSHOP]**
* Change the following options in the Performance KPI header:
  * Set Time to -1h.
  * Segment by  *Synthetic transactions* (default is Location).

Looking at the dots, what do you recommend your developer, if your goal is to improve performance?

* To dive deeper:
  * Reduce Time to -15m.
  * Filter to just *Place Order*. (Remove all other transactions from the dialog box)
* Hover in the white space of the chart - you should get a black vertical line.
* Move your Mouse pointer horizontally across the chart. (the line should move along).

What can you conclude of the relation of the Dots and the red X's at the bottom?

* Change the filter to just *Keep Browsing*, the dots should change both pattern and color.
{{% /notice %}}

![Duration - Place Order](../images/duration-place-order.png)

Select a successful test dot. (One that has no red X beneath it). If there are multiple tests in that time range you will be presented with a list of tests. Pick one that is around 20 seconds long and resulted in ✅ Success.

![Results](../images/select-result.png)

This will take you to the Synthetic Test Details or Waterfall.

If the new page has a Red Banner like this on top:

![error](../images/run-result-error.png)

You accidentally picked an test that had an error, it timed out. (This can happen as new tests are added and the UI just refreshed). In that case, Go back in the browser and try again.  
