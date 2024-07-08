---
title: Service Bureau
linkTitle: 6. Service Bureau
weight: 6
time: 10 minutes
---

* How to keep track of the usage of Observability Cloud in your organization
* Learn how to keep track of spend by exploring the Subscription Usage interface
* Creating Teams
* Adding notification rules to Teams
* Controlling usage

---

## 1. Understanding engagement

To fully understand Observability Cloud engagement inside your organization, click on the **>>** bottom left and select the **Settings → Organization Overview**, this will provide you with the following dashboards that show you how your Observability Cloud organization is being used:

![Organization Overview](../images/engagement.png)

You will see various dashboards such as Throttling, System Limits, Entitlements & Engagement. The workshop organization you're using now may have less data to work with as this is cleared down after each workshop.

Take a minute to explore the various dashboards and charts in the Organization Overview of this workshop instance.

## 2. Subscription Usage

If you want to see what your usage is against your subscription you can select **Subscription Usage**.

![Left pane](../images/billing-and-usage-menu.png)

This screen may take a few seconds to load whilst it calculates and pulls in the usage.

## 3. Understanding usage

You will see a screen similar to the one below that will give you an overview of the current usage, the average usage and your entitlement per category: Hosts, Containers, Custom Metrics and High Resolution Metrics.  

For more information about these categories please refer to [Monitor Splunk Infrastructure Monitoring subscription usage](https://docs.splunk.com/Observability/admin/monitor-imm-billing-usage.html).

![Billing and Usage](../images/usage-charts.png)

---

## 4. Examine usage in detail

The top chart shows you the current subscription levels per category (shown by the red arrows at the top in the screenshot below).

Also, your current usage of the four categories is displayed (shown in the red lines at the bottom of the chart).

In this example, you can see that there are 25 Hosts, 0 Containers, 100 Custom Metrics and 0 High Resolution Metrics.

![Billing and Usage-top](../images/usage-detail.png)

In the bottom chart, you can see the usage per category for the current period (shown in the drop-down box on the top right of the chart).

The blue line marked **Average Usage** indicates what Observability Cloud will use to calculate your average usage for the current Subscription Usage Period.

![Billing and Usage-Bottom](../images/usage-trends.png)

{{% notice title="Info" style="info" %}}
As you can see from the screenshot, Observability Cloud does not use High Watermark or P95% for cost calculation but the actual average hourly usage, allowing you to do performance testing or Blue/Green style deployments etc. without the risk of overage charges.
{{% /notice %}}

To get a feel for the options you can change the metric displayed by selecting the different options from the **Usage Metric** drop-down on the left, or change the **Subscription Usage Period** with the drop-down on the right.

Please take a minute to explore the different time periods & categories and their views.

Finally, the pane on the right shows you information about your Subscription.

![Billing and Usage-Pane](../images/subscription.png)
