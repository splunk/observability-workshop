---
title: Adding a Custom Chart
linkTitle: 2. Adding a Custom Chart
weight: 3
---

In this part of the workshop we are going to create a chart that we will add to our dashboard, we will also link it to the detector we previously built. This will allow us to see the behavior of our test and get alerted if one or more of our test runs breach its SLA.

{{% notice title="Exercise" style="green" icon="running" %}}

* At the top of the dashboard click on the **+** and select **Chart**.
  ![new chart screen](../images/new-chart.png)
* First, use the {{% button style="grey" %}}Untitled chart{{% /button %}} input field and name the chart **Requests by version & error**.
* For this exercise we want a bar or column chart, so click on the 3rd icon {{% icon icon="chart-bar" %}} in the chart option box.
* In the **Plot editor** enter `spans.count` (this is runtime in duration for our test) in the **Signal** box and hit enter.
* Click {{% button style="blue" %}}Add filter{{% /button %}} and choose `sf_service:wire-transfer-service`
* Right now we see different colored bars, a different color for each region the test runs from. As this is not needed we can change that behavior by adding some analytics.
* Click the {{% button style="blue" %}}Add analytics{{% /button %}} button.
* From the drop-down choose the **Sum** option, then pick `sum:aggregation` and click `version` and then click `sf_error` to group by both of these dimensions. Notice how the chart changes as the metrics are now aggregated.
![new chart screen](../images/spans-sum-version-error.png)
* Click the {{% button style="blue" %}}Save and close{{% /button %}} button.
* In the dashboard, move the charts so they look like the screenshot below:
  ![Service Health Dashboard](../images/service-health-dashboard.png)
* For the final task, click three dots **...** at the top of the page (next to **Event Overlay**) and click on **View fullscreen**. This will be the view you would use on the TV monitor on the wall (press Esc to go back).

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

In your spare time have a try at adding another custom chart to the dashboard using APM or Infrastructure metrics. You could copy a chart from the out-of-the-box **Kubernetes** dashboard group. Or you could use the APM metric `traces.count` to create a chart that shows the number of errors on a specific endpoint.

{{% /notice %}}

 Finally, we will run through a workshop wrap-up.
