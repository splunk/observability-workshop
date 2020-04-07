### Lab Summary

*  How to keep track of the usage of SignalFx in your organization.
*  Learn how to keep track of spend by exploring the Billing and Usage interface.

---

### 1. Understanding SignalFx engagement

To fully understand SignalFx adoption inside your organization, click on the **Settings** icon on the top right of the SignalFx UI,
![Settings Icon](../images/module5/M5-l1-1.png)

It may also look like this ![gray user icon](../images/M1-l7-2.jpg).
From the drop down, select the **Organizations Settings → Organization Overview** menu item, this will provide 
you with the following dashboard that shows you how your SignalFx organization is being used:

![Organization overview](../images/M1-l7-3.jpg)

On the left, you will see a list of registered users (blurred for privacy in the above screenshot), and the various charts that show you the number of registered users, chart's and dashboards created and growth trends.

The screenshot is taken from an actual organization, the workshop organization  your are looking at,
may have less data to work with.
Take a minute to explore the various charts in the Organization over view of the workshop instance.

---

### 2. Usage and Billing
If you want to see what your spend is against your contract you can either select the  **Settings** icon on the top right of the SignalFx UI again,
![Settings Icon](../images/M1-l7-1.jpg)
but this time select the **Organizations Settings → Usage and Billing** tab, or the faster way, select the **Usage and Billing** tab from the left pane!

![Left pane](../images/M1-l7-4.jpg)

This screen will take a few seconds to load whilst it calculates the usage.

---

### 3. Understanding usage
You should see a screen similar like the one below  that will give you an overview of the current usage, 
the average usage  and your entitlement per category : Nodes, Containers, Customer Metrics and 
High Resolution Metrics.  

For more information on what these are please read [ Billing and Usage information](https://docs.signalfx.com/en/latest/admin-guide/usage.html#viewing-billing-and-usage-information)
 
![Billing and Usage](../images/M1-l7-6.jpg)

You can find the category count inside the 4 red boxes below the graphs and your entitlement 
per category is shown in red above each graph. 
The graph will also show you how much you are consuming at this point in time.

In the bottom chart, you can see the usage per category for the current period (shown in the 
drop-down box on the top right of the chart.) 
The blue line marked _Average usage_ indicates what SignalFx will use to calculate your average usage 
for the current period. 

!!! info

    As you can see from the screenshot, SignalFx does not use High water mark or p95% for cost calculation but the actual average usage, allowing you do performance testing or Blue/Green style deployments etc. without risk of overage charges.

The Red box on the right  shows you information about your organizations and contract end date.

You can change the category type by the drop down on the top left of the chart.
Please take a minute to explore the different time periods & categories and their usage.
