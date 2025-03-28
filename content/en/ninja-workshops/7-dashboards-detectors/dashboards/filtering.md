---
title: Using Filters & Formulas
weight: 3
---

## 1 Creating a new chart

Let's now create a new chart and save it in our dashboard!

Select the plus icon **(1)** (top right of the UI) and from the drop down, choose the option **Chart (2)**.
Or click on the {{< button style="blue">}}+ New Chart{{< /button >}} Button **(3)** to create a new chart.

![Create new chart](../../images/new-chart.png)

You will now see a chart template like the following.

![Empty Chart](../../images/empty-new-chart.png)

Let's enter a metric to plot. We are still going to use the metric **`demo.trans.latency`**.

In the **Plot Editor (1)** tab under **Signal (2)** enter **`demo.trans.latency`(3)**.

![Signal](../../images/plot-editor.png)

You should now have a familiar line chart with 18 Timeseries reporting **(4)**. Please switch the time to 15 mins by using the dropdown **(1)**.

![Signal](../../images/line-chart-15-mins.png)

## 2. Filtering and Analytics

Let's now select the **Paris** datacenter to do some analytics - for that we will use a filter.

Let's go back to the **Plot Editor** tab and click on {{% button style="blue" %}}Add Filter{{% /button %}}
button, **(2)** in the screen shot above, wait until it automatically populates , choose **`demo_datacenter` (1)**, and then add **`Paris` (2)**.

![Filter](../../images/select-filter.png)

In the **F(x) (1)** column, click on the {{% button style="blue" %}}Add Analytics{{% /button %}} button and add the analytic function **`Percentile` (2)** from the dropdown list, then pick the  **`Percentile:Aggregation` (3)** version, and leave the value of the desired percentile on **`90`** in the follow up screen. (Afterwards click outside the pane to confirm **(4)**).

![Analytics](../../images/prepare_filter.png)

For info on the **Percentile** function and the other functions see [Chart Analytics](https://docs.splunk.com/Observability/data-visualization/charts/gain-insights-through-chart-analytics.html#gain-insights-through-chart-analytics).

---

## 3. Using Timeshift analytical function

Let's now compare with older metrics. Click on **`...`** and then on **Clone** in the dropdown to clone Signal **A**.

![Clone Signal](../../images/M-Filter-3.png)

You will see a new row identical to **A**, called **B**, both visible and plotted.

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

## 4. Using Formulas

Let's now plot the difference of all metric values for a day with 7 days in between.

Click on {{% button style="blue" %}}Enter Formula{{% /button %}}
 then enter **`A-B`** (A minus B) and hide (deselect) all Signals using the eye, except **C**.

![Formulas](../../images/M-Filter-11.png)

We now see only the difference of all metric values of **A** and **B** being plotted. We see that we have some negative values on the plot because a metric value of **B** has some times larger value than the metric value of **A** at that time.

Lets look at the Signalflow that drives our Charts and Detectors!
