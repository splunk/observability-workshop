---
title: Adding charts to the Service Health Dashboard 📋
linkTitle: 2. Add Charts
weight: 2
---

In this section, we are going to use the **Copy and Paste** functionality to extend our dashboard. Remember we copied some charts during the APM Service Dashboard section, we will now Add those chart to our dashboard.

{{% notice title="Exercise" style="green" icon="running" %}}

* Find your Service Health Dashboard.
* Select the **2+** at the top of the page and select **Paste charts**, this will create the charts in your custom dashboard.
* Add `sf_environment:[WORKSHOPNAME]` and `sf_service:payment_service` to the override filter box. ( This will make sure the charts only show data for your workshops payment service.)
* Click {{% button style="blue" %}}Save{{% /button %}}.
* As the new pasted charts appeared at the bottom of our dashboard, lets re-organize our dashboard gain.
* First drag the *Log view* chart to the second row, between the *Instructions* chart and the *Log Lines* chart, and expand it to fill the row.
* Then first resize the two new charts to be 1/3 of a row chart we just pasted, before moving them to the top row, so you have the *Instruction, Request Rate & Error Rate* chart taking up the top row.

![new dashboard look](../images/copyandpastedcharts.png)

* Click the {{% button style="blue" %}}Save{{% /button %}} button again to keep th lates changes.

Now we are going to create a custom chart based on our Synthetic test that is running.
{{% /notice %}}
