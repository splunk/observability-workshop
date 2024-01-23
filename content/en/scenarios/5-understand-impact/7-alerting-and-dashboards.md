---
title: Use Tags with Alerting and Dashboards
linkTitle: 5.7 Use Tags with Alerting and Dashboards
weight: 7
---

Earlier, we created a **Troubleshooting Metric Set** on the **credit.score.category** tag, which allowed us to use Tag Spotlight with that tag and identify a pattern to explain why some users received a poor experience. 

In this section of the workshop, we'll explore a related concept:  **Monitoring Metric Set**

Monitoring Metric Sets go beyond troubleshooting and allow us to use tags for alerts, dashboards, and more.  

Let's navigate to Settings -> APM MetricSets, and click the edit button (i.e. the little pencil) beside the MetricSet for **credit.score.category**. 

Check the box beside "Also create Monitoring MetricSet" then click **Start Analysis**. 

![Monitoring MetricSet](../images/monitoring_metricset.png)

The **credit.score.category** tag appears again as a Pending MetricSet. After a few moments, a green checkmark should appear.  Click this green checkmark to enable the Pending MetricSet. 

Next, let's explore how we can use this Monitoring MetricSet, or MMS.  Navigate to **Metric Finder**, then type in the name of the tag, which is **credit_score_category** (note that the dots were replaced by underscores when the MMS was created).  You'll see that multiple metrics exist that include this tag as a dimension: 

![Metric Finder](../images/metric_finder.png)

Let's take a moment to explain where these metrics come from. By default, Splunk Observability Cloud calculates several metrics using the trace data it receives.  <expand here> 

By creating an MMS, credit_score_category was added as a dimension to these metrics, which means that this dimension can now be used for alerting and dashboards. 

To see how, let's click on the metric named **service.request.duration.ns.p99**, which brings up the following chart: 

![Service Request Duration](../images/service_request_duration_chart.png)

This metric tracks the p99 response time of service requests, broken down by various attributes.  Let's break down the chart by credit score category. 

Click on the **Add analytics** button, select **Mean**, then **Mean:Aggregation**, then Group By the **credit_score_category** dimension: 

![Duration by Credit Score](../images/duration_by_credit_score.png)

Now we can see the duration by credit score category. In my example, the green line represents the "exceptional" category, and we can see that the duration for these requests sometimes goes all the way up to 5 seconds. 

The yellow line represents the "very good" category, and has very fast response times. 

The magenta line represents the "poor" category, and has response times between 2-3 seconds. 

It may be useful to save this chart on a dashboard for future reference. To do this, click on the "Save as..." button and provide a name for the chart:

![Save Chart As](../images/save_chart_as.png)

When asked which dashboard to save the chart to, let's create a new one named "Credit Check Service": 

![Save Chart As](../images/create_dashboard.png)

Now we can see the chart on our dashboard, and can add more charts as needed to monitor our credit check service: 

![Credit Check Service Dashboard](../images/credit_check_service_dashboard.png)

That's great that we have a dashboard to monitor the response times of the credit check service by credit score, but we don't want to stare at the dashboard all day. 

Let's create an alert so we can be notified proactively if some users of the credit check service are experiencing poor performance. 

To create an alert, click on the little bell on the top right-hand corner of the chart, then select "New detector from chart": 

![CNew Detector From Chart](../images/new_detector_from_chart.png)

Let's call the detector "Latency by Credit Score Category".  Add a filter to apply it to the "creditcheckservice" only, and set the environment to your environment name (i.e. tagging-workshop-yourname).   
