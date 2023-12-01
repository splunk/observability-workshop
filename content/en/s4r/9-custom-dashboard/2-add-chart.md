---
title: Adding charts to the Service Health Dashboard 📋
linkTitle: 2. Add Charts
weight: 2
---

In this section, we are going to use the **Copy and Paste** functionality to extend our dashboard. Remember we copied some charts during the APM Service Dashboard section, we will now add those charts to our dashboard.

{{% notice title="Exercise" style="green" icon="running" %}}

* Find your Service Health Dashboard.
* Select the **2+** at the top of the page and select **Paste charts**, this will create the charts in your custom dashboard.
<!--* Add `sf_environment:[WORKSHOPNAME]` and `sf_service:payment_service` to the override filter box. ( This will make sure the charts only show data for your workshop **paymentservice**).
-->
* The chart currently show data for all *Environments* & *Services*, so lets add a filter to our environment and the paymentservice.
* Click on the the 3 dots **...** at the  top right side of the **Request Rate** chart. This wil open the edit mode.
* In the new screen, click on the {{% button style="blue" %}}sf_environment{{% /button %}} button (1) in the middle of the screen, and pick the [WORKSHOPNAME] from the drop down. The button should change to **sf_environment:[WORKSHOPNAME]**
* Do the same with the {{% button style="blue" %}}sf_service.{{% /button %}} button (2), only this time change it to `paymentservice`.
![edit chart](../images/edit-chart.png)
* Click the {{% button style="blue" %}}Save and close {{% /button %}} button (3). 
* Click {{% button style="blue" %}}Save{{% /button %}}.
* As the new pasted charts appeared at the bottom of our dashboard, we need to re-organize our dashboard gain.
* First drag the *Log view* chart to the second row, between the *Instructions* chart and the *Log Lines* chart, and expand it to fill the row.
* Then first resize the two new charts to be 1/3 of a row chart we just pasted, before moving them to the top row, so you have the *Instruction, Request Rate & Error Rate* chart taking up the top row.

![new dashboard look](../images/copyandpastedcharts.png)

* Click the {{% button style="blue" %}}Save{{% /button %}} button again to keep th lates changes.

Now we are going to create a custom chart based on our Synthetic test that is running.

{{% /notice %}}
