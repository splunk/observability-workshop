---
title: Dashboard Components
time: 2 minutes
weight: 5
description: In this exercise,you will work with some of the dashboard components that can be used to build compelling dashboards.
---
The ability to build dashboards is a vital component of the AppDynamics capabilities and value. In this exercise,you will work with some of the dashboard components that can be used to build compelling dashboards.

## Create a new dashboard

1. Select the **Dashboard & Reports** tab.
2. Click **Create Dashboard**.
3. Enter a dashboard name such as **SuperCar-Dashboard-YOURINITIALS**.
4. Select **Absolute Layout** as the **Canvas Type**.
5. Click **OK**.

![NewDashboard](images/05-biq-create-dashboard.png)

Now open the newly created empty dashboard. You will now add various widget types.

## Dashboard components custom widget builder

The custom widget builder is a highly flexible tool that can generate representations of data, including numeric vews, time series, pie charts, and more. It is based on the AppDynamics AD Query Language.

To create a widget, follow these steps:

1. Toggle the **Edit Mode** at the upper left corner of the dashboard.
2. Click **Add Widget**.
3. Select the **Analytics** tab on the left.
4. Click **Custom Widget Builder**.

![NewCustomWidgetBuilder](images/05-biq-widget-builder.png)

There are many chart types that you can create in the Customer Widget Builder. You can simply drag or drop information or create an AD Query in the Advanced pane..

![NewCustomWidgetBuilder](images/05-biq-add-widget.png)

For now, we will cover Numeric, Bar and Pie Charts.

### Numeric charts

**Exercise:** Quantifying the dollar amount impacted by errors enables you to show the impact of IT performance on the business revenue.

1. Select the **Numeric** chart type.
2. Add a Filter on the Application field and Select your application name: **Supercar-Trader-YOURINITIALS**
3. Add a filter on the **/Supercar-Trader/sell.do** business transactions.
4. Add a filter on the User Experience Field selecting only the **Error** to show the impact of errors.
5. Find the **CarPrice_MIDC** field on the left panel and drag and drop it into the Y-Axis. Notice that SUM is the Aggregation used to capture the total price per model.
6. Change the font color to red for better visibility.
7. Click **Save**.

![NumericChartWidget](images/05-biq-lost-revenue.png)

Note that you could do the same for the **$ Amount Transacted Successfully** criterion by changing the user experience filter to only include NORMAL, SLOW and VERY SLOW.

You could also baseline this metric by creating a custom metric in the Analytics module and defining a health rule that indicates if the **$ Amount Impacted** is equal to or higher than the baseline. You can also add a label for the currency.

![NumericChartSamples](images/06-numeric-chart-widget-samples-09.png)

### Bar charts

**Exercise:** You will now create a bar chart to visualize Top Impacted Car Models. The chart will show the car models of all of the **SellCar** transactions, categorized by the User Experience.

1. Create a New Widget by clicking **+ Add Widget**, **Analytics** and **Custom Widger Builder**
2. Select the **Column** chart type.
3. Add the following filters: Application = **Supercar-Trader-YOURINITIALS** and Business Transaction = **/Supercar-Trader/sell.do**.
4. Add **CarModel\_MIDC** and **User Experience** to the X-Axis.
5. Click **Save**.

![BarChartWidget](images/05-biq-bar-chart.png)

This chart type can be adjusted based on your need. For example, you could group the X-AXIS by Customer Type, Company, Organization, and more. Refer to the following example.

![BarChartSamples](images/06-bar-chart-widget-samples-05.png)

### Pie charts

You will now create a pie chart that shows all the car models reported by the `sellCar` transaction and the sum of prices per model. This will show the most highly-demanded model in the application.

1. Create a new Widget
2. Select the **Pie** chart type.
3. Add the following filters: Application = **Supercar-Trader-YOURINITIALS** and Business Transaction = **/Supercar-Trader/sell.do**.
4. Add **CarModel\_MIDC** in the X-Axis
5. Add **CarPrice\_MIDC** in the Y-Axis. Note that **SUM** is the aggregation used to capture the total price per model.
6. Add a Title **Sold by Car Model**
7. Click **Save**.

![PieChartWidget](images/05-biq-pie-chart.png)

Refer to the following example for more uses of the pie chart widget.

![PieChartSamples](images/06-pie-chart-widget-samples-07.png)

## Dashboard components: Conversion funnels

Conversion funnels help visualize the flow of users or events through a multi-step process. This enables you to better understand which steps can be optimized for more successful convergence. You can also use conversion funnels to examine the IT perfomance of every step, to understand how they impact the user experience and identify the cause of user drop-offs.

Note that the funnel is filtered according to the users who executed this path in that specific order, not the total visits per step.

The first step of funnel creation is to select a unique identifier of the transaction that can represent each user navigation through the funnel. Usually, the Session ID is the best choice, since it persists through each step in the funnel.

A Session ID can be captured from the transactions. You’ll need a **SessionId** data collector to use it as a counter for the Funnel transactions.

For Java applications, AppDynamics has the capability to Session IDs in the default HTTP data collector. You’ll ensure that it is enabled and apply it to all business transactions to capture the Session ID for every transaction.

1. Select the **Applications** tab.
2. Select **Supercar-Trader-YOURINITIALS** Application.
3. Select the **Configuration** Left tab.
4. Click **Instrumentation**.
5. Select the **Data Collectors** tab.
6. Edit the **Default HTTP Request Request Data Collectors**.
7. Select **Transaction Analytics**.
8. Verify that **SessionID** is selected.
9. Click **Save**.

![EnableSessionId](images/05-biq-session-id.png)

Now apply some load by navigating multiple times from the **/Supercar-Trader/home.do** page. Then, directly navigate to **/Supercar-Trader/sell.do** page on the application.

Now Return to your Dashboard to create the funnel widget.  

1. Toggle the **Edit** slider.
2. Click **Add Widget**.
3. Select the **Analytics** tab.
4. Click **Funnel Analysis**.
5. Select **Transactions** from the drop-down list.
6. Under **Count Distinct of**, select **uniqueSessionId** from the drop-down list.
7. Click **Add Step**. Name it **Home Page**.
8. Click on **Add Criteria**. Add the following criteria: **Application**: Supercar-Trader-YOURINITIALS & **Business Transactions**: **/Supercar-Trader/home.do**.
9. Click **Add Step**. Name it **SellCar Page**.
10. Click on **Add Criteria**. Add the following criteria: **Application:** Supercar-Trader-YOURINITIALS &  **Business Transactions:** /Supercar-Trader/sell.do.
11. Select the **Show Health** Checkbox on the right panel to visualize the transaction health in the flow map.
12. Click **Save**

![FunnelWidget](images/05-biq-funnel-chart.png)
