---
title: Adding charts to dashboards
linkTitle: 1.09. Adding more charts
weight: 1.09
---

## 1. Saving to an Existing Dashboard

Before saving your chart, check the top-left corner to confirm that **YOUR_NAME-Dashboard: YOUR_NAME-Dashboard (1)** is selected. This ensures that your chart will be saved to the correct dashboard.

Next, give your chart a name. Enter **Latency History** **(2)**, and if you’d like, add a brief description in the **Chart Description (3)** if you wish like in our example.
![Save Chart 1](../../images/morecharts-1.png)

---
When you’re ready, click the {{% button style=blue %}}Save And Close{{% /button %}} button **(4)**. You’ll be returned to your dashboard, which now contains two charts.
![Save Chart 2](../../images/morecharts-2.png)

---

## 2. Copy and Paste a chart

Now let’s quickly add another chart by duplicating the one we just created.

In your dashboard, locate the **Latency History** chart and click the three dots **`...`** **(1)** in the upper-right corner of the chart. From the menu, select **Copy (2)**.

After copying, you’ll notice a small white **1** appear in front of the **+** icon **(3)** at the top of the page. This indicates that one chart is ready to be pasted.
![Copy chart](../../images/morecharts-3.png)

---
Click the **+** icon **()1** at the top of the page, and in the dropdown menu, select **(2)**.  
You should also see a **1** at the end of that line, confirming that the copied chart is ready to be added.
![Past charts](../../images/morecharts-4.png)

This will place a copy of the previous chart in your dashboard.
![Three Dashboard](../../images/morecharts-5.png)

---

## 3. Edit the pasted chart

 To edit the duplicated chart, click the three dots **`...`** on one of the **Latency History** charts in your dashboard and then select **Open**.    Alternatively, you can click directly on the chart’s title, **Latency History**, to open it in the editor.

This will bring you to the editor environment again.

Start by adjusting the time range in the top-right corner of the chart. Set it to **Past 1 Hour (1)** to give you a broader view of recent data.

Next, let’s customize the chart to make it unique. Click the eye icon next to **Signal A (2)** to make it visible again.  
Then hide **Signal C (3)** by clicking its eye icon.

Update the chart title from *Latency history* to **Latency vs Load (4)**, and optionally add or edit the chart description to reflect the updated focus **(5)**.
![Set Visibility](../../images/morecharts-6.png)

---
Click on the {{% button style=blue %}}Add Metric Or Event{{% /button %}} button to create a new signal. In the input field that appears, type and select `demo.trans.count` **(1)** to add it as **Signal D**.
![Dashboard Info](../../images/M-MoreCharts-8.png)

---
This adds a new signal, **Signal D**, to your chart. It represents the number of active requests being processed.

To focus on the **Paris data center**, add a filter for **demo_datacenter: Paris**. Then, click the Configure Plot button to adjust how the data is displayed. Change the **rollup** type from **Auto (Delta)** to **Rate/sec** to show the rate of incoming requests per second.

Finally, rename the signal from `demo.trans.count` to `Latency vs Load` to reflect its role in the chart more clearly.

![rollup change](../../images/M-MoreCharts-9.png)

Finally press the {{% button %}}Save And Close{{% /button %}} button. This returns you to your dashboard that now has three different charts!

![three charts](../../images/M-MoreCharts-10.png)

Let's add an "instruction" note and arrange the charts!
