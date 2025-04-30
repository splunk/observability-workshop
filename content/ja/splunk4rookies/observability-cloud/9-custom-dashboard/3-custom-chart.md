---
title: Adding a Custom Chart
linkTitle: 2. Adding a Custom Chart
weight: 3
---

In this part of the workshop we are going to create a chart that we will add to our dashboard, we will also link it to the detector we previously built. This will allow us to see the behavior of our test and get alerted if one or more of our test runs breach its SLA.

{{% notice title="Exercise" style="green" icon="running" %}}

* At the top of the dashboard click on the **+** and select **Chart**.
  ![new chart screen](../images/new-chart.png)
* First, use the {{% button style="grey" %}}Untitled chart{{% /button %}} input field and name the chart **Overall Test Duration**.
* For this exercise we want a bar or column chart, so click on the 3rd icon {{% icon icon="chart-bar" %}} in the chart option box.
* In the **Plot editor** enter `synthetics.run.duration.time.ms` (this is runtime in duration for our test) in the **Signal** box and hit enter.
* Right now we see different colored bars, a different color for each region the test runs from. As this is not needed we can change that behavior by adding some analytics.
* Click the {{% button style="blue" %}}Add analytics{{% /button %}} button.
* From the drop-down choose the **Mean** option, then pick `mean:aggregation` and click outside the dialog box. Notice how the chart changes to a single color as the metrics are now aggregated.
* The x-axis does not currently represent time to change this click on the settings {{% icon icon="cog" %}} icon at the end of the plot line. The following following dialog will open:
  ![signal setup](../images/signal-setup.png)
* Change the **Display units** (**2**) in the drop-down box from **None** to **Time (autoscaling)/Milliseconds(ms)**. The drop-down changes to **Millisecond** and the x-axis of the chart now represents the test duration time.
* Close the dialog, either by clicking on the settings {{% icon icon="cog" %}} icon or the {{% button style="gray" %}}close{{% /button %}} button.
* Add our detector by clicking the {{% button style="blue" %}}Link Detector{{% /button %}} button and start typing the name of the detector you created earlier.
* Click on the detector name to select it.
* Notice that a colored border appears around the chart, indicating the status of the alert, along with a bell icon at the top of the dashboard as shown below:
  ![detector added](../images/detector-added.png)
* Click the {{% button style="blue" %}}Save and close{{% /button %}} button.
* In the dashboard, move the charts so they look like the screenshot below:
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* For the final task, click three dots **...** at the top of the page (next to **Event Overlay**) and click on **View fullscreen**. This will be the view you would use on the TV monitor on the wall (press Esc to go back).

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

In your spare time have a try at adding another custom chart to the dashboard using RUM metrics. You could copy a chart from the out-of-the-box **RUM applications** dashboard group. Or you could use the RUM metric `rum.client_error.count` to create a chart that shows the number of client errors in the application.

{{% /notice %}}

 Finally, we will run through a workshop wrap-up.
