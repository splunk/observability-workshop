# Using Overlays

Let's overlay metrics and events to our initial plot to see if there is any correlation with high latency.

To discover and add new metrics to the chart from the ones that are being sent to SignalFx already, click on **Browse** as highlighted in the screenshot below.

In the **METRICS** sidebar on the right, enter **`demo`** and click on the search icon to search.

Observe that the **Find Metrics** option is pre-selected.

![Find metrics](../images/dashboards/M1-l1-25.png){: .zoom}

The metrics search is showing 3 metrics with **`demo`** in the name.

Select **`demo.trans.count`** and click on the **Add Plot**{: .label-button .sfx-ui-button-blue} button.

![Add Plot](../images/dashboards/M1-l1-26.png)

Click on the blue eye icon next to **C** to hide that Signal, and on the greyed eye icon for Signal **A** to show it.

On plot **D**, apply the **Percentile:Aggregation** function and set to **`95`**. Click on **Delta Rollup** and from the **Rollup** dropdown select **Rate/Sec**.

Enter **`-1h`** in the **Time** frame for the entire chart.

![Aggregation](../images/dashboards/M1-l1-27.png){: .zoom}

We see that there is a correlation between latency and number of transactions.

!!! note
    Likewise we could check **Find Events** and find events like deployment events etc. to correlate with.

Click on the the greater than sign icon to collapse the **METRICS** sidebar.

![Collapse Sidebar](../images/dashboards/M1-l1-28.png)
