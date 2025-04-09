---
title: Editing charts
linkTitle: 1.2 Editing charts
weight: 1.2
---
In this section, we’ll begin exploring how to edit charts by modifying an existing one. This is a great way to get familiar with the chart editor and understand how chart settings, data sources, and visual options work together.

## 1. Editing a chart

To get started, make sure you have the **SAMPLE CHARTS** dashboard open.

Find the **Latency histogram** chart, then click on the **three dots** (...) in the upper-right corner of the chart. From the menu, select **Open**. You can also simply click on the chart title (**Latency histogram**) to open it directly.

![Sample Charts](../../images/latency-histogram-open.png)

---
Once the chart editor opens, you’ll see the configuration for the **Latency histogram** chart. This includes the **Plot Options**, the currently selected **Plot Type**, and the associated **Signal** (or metric) being visualized.

The chart editor allows you to modify how the data is displayed — such as changing the chart type, adjusting time settings, or applying functions to the signal. This is where you can customize the look and behavior of the chart to better suit your needs.

![Latency Histogram](../../images/latency-histogram.png)

In the **Plot Editor (1)** tab under **Signal (2)** you see the metric **`demo.trans.latency` (3)** we are currently plotting.

![Plot Editor](../../images/plot-editor.png)

You will see a number of **Line** plots. The number **`18 ts` (4)** indicates that we are plotting 18 metric time series in the chart.

Click on the different chart type icons to explore each of the visualizations. Notice their name while you swipe over them. For example, click on the Heat Map icon:

![Chart Types](../../images/chartbartypes.png)

See how the chart changes to a heat map.

![Change to Heatmap](../../images/change-to-heatmap.png)

{{% notice title="Note" style="info" %}}
You can use different charts to visualize your metrics - you choose which chart type fits best for the visualization you want to have.

For more info on the different chart types see [Choosing a chart type.](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types)
{{% /notice %}}

Click on the **Line** chart type and you will see the line plot.

![Line Chart](../../images/change-to-line.png)

## 2. Changing the time window

You can also increase the time window of the chart by selecting from the **Time (1)**  and changing the time to **Past 15 minutes (2)** by selecting it from the dropdown.

![Line Chart](../../images/time_window.png)

## 3. Viewing the Data Table

Click on the **Data Table (1)** tab.

![Data Table](../../images/data-table.png)

You now see 18 rows, each representing a metric time series with a number of columns. These columns represent the dimensions of the metric. The dimensions for `demo.trans.latency` are:

- `demo_datacenter` **(2)**
- `demo_customer`   **(3)**
- `demo_host`       **(4)**

In the **`demo_datacenter`** column you see that there are two data centers, **Paris (5)**  and **Tokyo (6)**, for which we are getting multiple metrics.

If you move your cursor over the lines in the chart horizontally you will see the data table update accordingly. If you click on one of the lines in the chart you will see a pinned value **(7)** appear in the data table.

---

Now click on **Plot editor (8)** again to close the Data Table and let's save this chart into a dashboard for later use!
