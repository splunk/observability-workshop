---
title: Create Custom Chart & add to Dashboard
linkTitle: 3. Add Custom Chart
weight: 3
---

In this part of the workshop we are going to create a chart that we will add to our dashboard, we will also link it to the detector we previously build. This will allow us to see the behaviour of our test and get alerted if one or more of our test runs breaches its SLA.

{{% notice title="Exercise" style="green" icon="running" %}}

* At the top of the dashboard click on the **+** and select *chart*. This will bring us to the new chart screen.

![new chart screen](../images/new-chart.png)

* First use the {{% button style="gray" %}}Untitled chart{{% /button %}} input field and name the chart **Overall Test Duration**. Next, you can set the Description to **Showing the Synthetic Test for the complete application**.
* For this exercise we want a bar or column chart, so click on the 3d icon ![column chart](../images/barchart-icon.png?classes=inline&height=25px)in the chart option box.
* We need to provide a signal or metric that we are going to display. In this case we want *synthetics.run.duration.time.ms* (This is runtime in duration for our test)
* Click the {{% button style="blue" %}}Add filter{{% /button %}} button.
* Set the filter to successful ones by selecting *success:true*, the button now should contain that.
* Right now we see different colored bars, a different color for each region the test runs from. We change that behaviour by adding some analytics.
* Click the {{% button style="blue" %}}Add analytics{{% /button %}} button.
* From the drop down choose the *Mean* option, then pick **mean**:*aggregation* and click outside the dialog. the button should now say **Mean*, and the bars should now have the same color.
* We now looking at the aggregated results of the tests instead of showing each region separately.
* Click on the settings *⚙️* icon at the end of the plot line. It will open the following dialog.
![signal setup](../images/signal-setup.png)
* Change the *Display units* in the drop down box from *None* to *Time (autoscaling)/Milliseconds(ms)*. The dropdown changes to *Millisecond* and the label in front of the chart should now represent Time.
* Close the dialog, either clicking on the settings *⚙️* icon or the {{% button style="gray" %}}close{{% /button %}} button.
* Add our detector by clicking {{% button style="blue" %}}Link Detector{{% /button %}} and typing the name of the detector. (Start with you initials, assuming you used the recommended naming method.) the detector name should appear. A colored bar appears around your chart, indicating the status of the alert, (Green OK, Red Alert), as well as a bell signal at the top of the page as shown below.

![detector added](../images/detector-added.png)

* Click the {{% button style="blue" %}}Save and close{{% /button %}} button.

* In our dashboard, size the *Log view* chart to be last 50% of the page width  and drag the new *Overall Test Duration* chart in front of it.

The result should be like this:
![Service Health Dashboard](../images/service-health-dashboard.png)

As the last task, find the the thee dots **...** at the top of the page (next to *Event Overlay*) and click on *View fullscreen*. This will be the view you would use on the TV monitor on the wall.
(press Esc to go back) For TV monitors, setting the background color to black seems to work best.

{{% /notice %}}
 Now lets go and wrap up.
