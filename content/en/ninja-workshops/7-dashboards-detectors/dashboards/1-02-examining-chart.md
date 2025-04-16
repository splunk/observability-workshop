---
title: Exploring Charts
linkTitle: 1.02. Exploring Charts
weight: 1.02
---
In this section, we’ll start by exploring how charts are built and displayed in Splunk Observability. By examining and interacting with an existing chart, you’ll get a feel for how the chart editor works—how data sources are selected, how visual options are configured, and how different settings shape what you see.

## 1. Select a chart

To get started, make sure you have the **SAMPLE CHARTS** dashboard open.

Find the **Latency histogram** chart, then click on the **three dots** (...) in the upper-right corner of the chart. From the menu, select **Open**. You can also simply click on the chart title (**Latency histogram**) to open it directly.

![Sample Charts](../../images/latency-histogram-open.png)

---
Once the chart editor opens, you’ll see the configuration settings for the Latency histogram chart.

The chart editor is where you can control how your data is visualized. You can change the chart type, apply transformation functions, adjust time settings, and customize other visual and data-related options to match your specific needs.

![Latency Histogram](../../images/latency-histogram.png)

---

In the **Plot Editor (1)** tab, under the **Signal (2)** section, you’ll find the metric currently being used: `demo.trans.latency` **(3)**. This signal represents the latency data that the chart is plotting. You can use this area to edit or add additional signals to compare or enrich the visualization.

You’ll notice several **Line** plots displayed in the chart. The label `18 ts` **(4)** indicates that the chart is currently plotting **18 individual metric time series**.
![Plot Editor](../../images/plot-editor.png)

To explore different visualization styles, try clicking on the various chart type icons in the editor. As you hover over each icon, its name will appear—helping you understand what each type represents.

![Chart Types](../../images/chartbartypes.png)

For example, click on the **Heat Map** icon to see how the same data is represented in a different format.

![Change to Heatmap](../../images/change-to-heatmap.png)

{{% notice title="Note" style="info" %}}
You can visualize your metrics using a variety of chart types—choose the one that best represents the insights you want to highlight.

For a detailed overview of available chart types and when to use them, check out [Choosing a chart type.](https://docs.splunk.com/Observability/data-visualization/charts/chart-types.html#chart-types)
{{% /notice %}}
