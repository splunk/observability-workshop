# Using Filters

## 1. Filtering and Analytics

Let's now select the **Paris** datacenter to do some analytics - for that we will use a filter.

Let's go back to the **Plot Editor** tab and click on **Add Filter**{: .label-button .sfx-ui-button-blue}, wait until it automatically populates, choose **`demo_datacenter`**, and then **`Paris`**.

![Filter](../images/dashboards/M1-l1-13.png){: .zoom}

In the **F(x)** column, add the analytic function **`Percentile:Aggregation`**, and leave the value to **`95`** (click outside to confirm).

![Analytics](../images/dashboards/M1-l1-14.png){: .zoom}

For info on the **Percentile** function and the other functions see [Analytics reference](https://docs.signalfx.com/en/latest/reference/analytics-docs/analytics-reference.html){: target=_blank}.

---

## 2. Using Timeshift analytical function

Let's now compare with older metrics. Click on **`...`** and then on **Clone** in the dropdown to clone Signal **A**.

![Clone Signal](../images/dashboards/M1-l1-15.png){: .zoom}

You will see a new row identical to **A**, called **B**, both visible and plotted.

![Plot Editor](../images/dashboards/M1-l1-16.png){: .zoom}

For Signal **B**, in the **F(x)** column add the analytic function **Timeshift** and enter **`7d`** (7 days = 1 week), and click outside to confirm.

![Timeshift](../images/dashboards/M1-l1-17.png){: .zoom}

Click on the cog on the far right, and choose a **Plot Color** e.g. pink, to change color for the plot of **B**.

![Change Plot Colour](../images/dashboards/M1-l1-18.png){: .zoom}

Click on **Close**.

Next, click into the field next to **Time** on the Override bar and choose **`Past Day`** from the dropdown.

![Timeframe](../images/dashboards/M1-l1-19.png)

We now see plots for Signal **A** (the last day) as a blue plot, and 7 days ago in pink.

![Chart](../images/dashboards/M1-l1-20.png)

In order to make this clearer we can click on the **Area chart** icon to change the visualization.

![Area Chart](../images/dashboards/M1-l1-21.png){: .zoom}

We now have a better view of our two plots!
