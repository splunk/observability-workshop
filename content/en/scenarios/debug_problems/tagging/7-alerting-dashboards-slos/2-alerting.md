---
title: Use Tags with Alerting
linkTitle: 2. ...with Alerting
weight: 2
time: 3 minutes
---

### Alerts

It's great that we have a dashboard to monitor the response times of the credit check service by credit score, but we don't want to stare at a dashboard all day.

Let's create an alert so we can be notified proactively if customers with `exceptional` credit scores encounter slow requests.

To create this alert, click on the little bell on the top right-hand corner of the chart, then select **New detector from chart**:

![New Detector From Chart](../../images/new_detector_from_chart.png)

Let's call the detector `Latency by Credit Score Category`.  Set the environment to your environment name (i.e. `tagging-workshop-yourname`) then select `creditcheckservice` as the service. Since we only want to look at performance for customers with `exceptional` credit scores, add a filter using the `credit_score_category` dimension and select `exceptional`:

![Create New Detector](../../images/create_new_detector.png)

As an alert condition instead of "**Static threshold**" we want to select "**Sudden Change**" to make the example more vivid.

![Alert Condition: Sudden Change](../../images/alert_condition_suddenchange.png)

We can then set the remainder of the alert details as we normally would. The key thing to remember here is that without capturing a tag with the credit score category and indexing it, we wouldn't be able to alert at this granular level, but would instead be forced to bucket all customers together, regardless of their importance to the business.

Unless you want to get notified, we do not need to finish this wizard. You can just close the wizard by clicking the **X** on the top right corner of the wizard pop-up.
