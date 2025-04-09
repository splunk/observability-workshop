---
title: Using Filters & Formulas
linkTitle: 1.5 Filters & Formulas
weight: 1.5
---

### 1 Creating a New Chart

Now let’s create a new chart and add it to the dashboard we’ve been working on!

To get started, click the plus icon **(1)** in the top-middle part of the interface. From the dropdown, select **Chart (2)**.
Alternatively, you can click the {{< button style="blue">}}+ New Chart{{< /button >}} Button **(3)** button to create a new chart directly.

![Create new chart](../../images/new-chart.png)

You’ll now see a blank chart template, ready for configuration:

![Empty Chart](../../images/empty-new-chart.png)

Let’s begin by adding a metric to visualize. For this example, we’ll continue working with **`demo.trans.latency`**, the same metric we used earlier.

In the **Plot Editor (1)**, go to the **Signal (2)** section, and enter **`demo.trans.latency`(3)** into the input field. This will load the latency time series data into the chart, so we can start building and customizing our visualization.

![Signal](../../images/plot-editor.png)

You should now see a familiar line chart displaying **18 time series (4)**. To view recent activity, change the time range to **Past 15 minutes** by selecting it from the **Time dropdown (1)**

![Signal](../../images/line-chart-15-mins.png)

### 2. Filtering and Analytics

Let's now select the **Paris** datacenter to do some analytics - for that we will use a filter.

Let's go back to the **Plot Editor** tab and click on {{% button style="blue" %}}Add Filter{{% /button %}}
button, **(2)** in the screen shot above, wait until it automatically populates , choose **`demo_datacenter` (1)**, and then add **`Paris` (2)**.

Now let’s narrow down our data to focus on the **Paris** data center, which will allow us to apply more targeted analytics. We’ll do this by using a **filter**.

Start by returning to the **Plot Editor** tab. Click the {{% button style=“blue” %}}Add Filter{{% /button %}} button **(2)** as shown in the screenshot above.

Wait a moment for the available dimensions to populate. Then:

* Select **demo_datacenter (1)** as the filter dimension.
* Choose **Paris (2)** as the value to filter on.

This filter will limit the chart to show only the time series coming from the Paris data center, making your analysis more focused and meaningful.

![Filter](../../images/select-filter.png)

In the **F(x) (1)** column of the chart editor, click the {{% button style="blue" %}}Add Analytics{{% /button %}} button o apply an analytic function.
From the dropdown list, select **`Percentile` (2)**, and then choose the **`Percentile:Aggregation` (3)** option.
In the follow-up panel, leave the percentile value set to **`90`**, which will display the 90th percentile of the selected time series.

To apply the function, simply click anywhere outside the panel to confirm your selection **(4)**.

![Analytics](../../images/prepare_filter.png)

For info on the **Percentile** function and the other functions see [Chart Analytics](https://docs.splunk.com/Observability/data-visualization/charts/gain-insights-through-chart-analytics.html#gain-insights-through-chart-analytics).

---

### 3. Using Timeshift analytical function

Let's now compare with older metrics. Click on **`...`** and then on **Clone** in the dropdown to clone Signal **A**.
Now let’s compare our current data to historical values using the **Timeshift** function.
Start by clicking the **`...`** menu next to **Signal A**, then select **Clone** from the dropdown.

![Clone Signal](../../images/M-Filter-3.png)

This creates a new row, **Signal B**, which is an identical copy of **A**. Both signals will now be visible and plotted on the chart, ready for further comparison.

![Plot Editor](../../images/M-Filter-4.png)

For Signal **B**, in the **F(x)** column add the analytic function **Timeshift** and enter **`1w`** (or 7d for 7 days), and click outside to confirm.

![Timeshift](../../images/M-Filter-5.png)

Click on the cog on the far right, and choose a **Plot Color** e.g. pink, to change color for the plot of **B**.

![Change Plot Colour](../../images/M-Filter-6.png)

Click on **Close**.

We now see plots for Signal **A** (the past 15 minutes) as a blue plot, and the plots from a week ago in pink.

In order to make this clearer we can click on the **Area chart** icon to change the visualization.

![Area Chart](../../images/M-Filter-8.png)

We now can see when last weeks latency was higher!

Next, click into the field next to **Time** on the Override bar and choose **`Past Hour`** from the dropdown.

![Timeframe](../../images/M-Filter-9.png)

---

### 4. Using Formulas

Let's now plot the difference of all metric values for a day with 7 days in between.

Click on {{% button style="blue" %}}Enter Formula{{% /button %}}
 then enter **`A-B`** (A minus B) and hide (deselect) all Signals using the eye, except **C**.

![Formulas](../../images/M-Filter-11.png)

We now see only the difference of all metric values of **A** and **B** being plotted. We see that we have some negative values on the plot because a metric value of **B** has some times larger value than the metric value of **A** at that time.

Lets look at the Signalflow that drives our Charts and Detectors!
