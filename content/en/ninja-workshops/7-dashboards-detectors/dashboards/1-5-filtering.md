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

Now let’s narrow down our data to focus on the **Paris** data center, which will allow us to apply more targeted analytics. We’ll do this by using a **Filter**.

Start by returning to the **Plot Editor** tab. Click the {{% button style=“blue” %}}Add Filter{{% /button %}} button **(2)** as shown in the screenshot above.

Wait a moment for the available dimensions to populate. Then:

* Select **demo_datacenter (1)** as the filter dimension.
* Choose **Paris (2)** as the value to filter on.

This filter will limit the chart to show only the time series coming from the Paris data center, making your analysis more focused and meaningful.

![Filter](../../images/select-filter.png)

In the **F(x) (1)** column of the chart editor, click the {{% button style="blue" %}}Add Analytics{{% /button %}} button o apply an analytic function.
From the dropdown list, select **`Percentile` (2)**, and then choose the **`Percentile:Aggregation` (3)** option.
In the follow-up panel, leave the percentile value set to 90, which tells the chart to display the 90th percentile of the selected time series.

In this context, the 90th percentile represents the value below which 90% of the latency measurements fall, in other words, only **the highest 10%** of values exceed this point. This is a useful way to understand “worst-case normal” performance—filtering out occasional spikes while still showing when latency is approaching unacceptable levels.

To apply the function, simply click anywhere outside the panel to confirm your selection **(4)**.

![Analytics](../../images/prepare_filter.png)

For info on the **Percentile** function and the other functions see [Chart Analytics](https://docs.splunk.com/Observability/data-visualization/charts/gain-insights-through-chart-analytics.html#gain-insights-through-chart-analytics).

---

### 3. Using Timeshift analytical function

Start by cloning **Signal A** by clicking the **`...`** menu **(1)** next to it, then selecting **Clone (2)** from the dropdown.

Cloning a signal creates a second, identical version with the same metric, filters, and settings. This allows you to apply different analytics—such as comparing current data to historical trends—without changing the original.

![Clone Signal](../../images/timeshift-filter.png)

After cloning, you’ll see a new signal labeled **Signal B (1)**. Since it’s an exact copy of **Signal A**, both signals display the same data over the same time range. As a result, they appear to **overlap completely** on the chart, making it look like there’s only one line.

To make the comparison meaningful, we’ll apply a **Timeshift** to **Signal B**, shifting its data one week into the past. This allows us to see how current latency trends compare to those from the same time last week.

In the **F(x)** column next to Signal B, click the {{% button style="blue" %}} **+** {{% /button %}} **(2)**, then choose the **Timeshift (3)** function from the list.

![Plot Editor](../../images/ab-plot-full.png)

When prompted, enter **1w** (or **7d** for 7 days) **(4)** as the time shift value. Click anywhere outside the panel **(5)** to confirm the change.

This will shift **Signal B**’s data one week into the past, allowing you to visually compare current latency trends with those from the same time last week.  

![Timeshift](../../images/b-shifted.png)

To change the color of **Signal B**, click the ⚙️ settings icon **(1)** on the far right of its row to open the settings menu. Then, select a **Plot Color**, such as pink **(2)**, to visually distinguish **Signal B** from the original signal on the chart.
When you are done, click on the{{% button style="gray" %}} Close {{% /button %}} **(3)**

![Change Plot Color](../../images/b-pink.png)

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
