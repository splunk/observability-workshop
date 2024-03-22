---
title: Use Tags with Alerting and Dashboards
linkTitle: 5.7 Use Tags with Alerting and Dashboards
weight: 7
time: 10 minutes
---

Earlier, we created a **Troubleshooting Metric Set** on the `credit.score.category` tag, which allowed us to use **Tag Spotlight** with that tag and identify a pattern to explain why some users received a poor experience.

In this section of the workshop, we'll explore a related concept:  **Monitoring MetricSets**.

## What are Monitoring MetricSets?

**Monitoring MetricSets** go beyond troubleshooting and allow us to use tags for alerting and dashboards.

## Create a Monitoring MetricSet

Let's navigate to **Settings** -> **APM MetricSets**, and click the edit button (i.e. the little pencil) beside the MetricSet for `credit.score.category`.

Check the box beside **Also create Monitoring MetricSet** then click **Start Analysis** (**note**: your workshop instructor will do this for you)

![Monitoring MetricSet](../images/monitoring_metricset.png)

The `credit.score.category` tag appears again as a **Pending MetricSet**. After a few moments, a checkmark should appear.  Click this checkmark to enable the **Pending MetricSet**.

## Using Monitoring MetricSets

Next, let's explore how we can use this **Monitoring MetricSet**.

### Dashboards

Navigate to **Metric Finder**, then type in the name of the tag, which is `credit_score_category` (note that the dots in the tag name were replaced by underscores when the MMS was created).  You'll see that multiple metrics include this tag as a dimension:

![Metric Finder](../images/metric_finder.png)

By default, **Splunk Observability Cloud** calculates several metrics using the trace data it receives.  See [Learn about MetricSets in APM](https://docs.splunk.com/observability/en/apm/span-tags/metricsets.html) for more details.

By creating an MMS, `credit_score_category` was added as a dimension to these metrics, which means that this dimension can now be used for alerting and dashboards.

To see how, let's click on the metric named `service.request.duration.ns.p99`, which brings up the following chart:

![Service Request Duration](../images/service_request_duration_chart.png)

This metric tracks the p99 response time of service requests in nanoseconds, broken down by various attributes. Nanoseconds are bit too granular for our needs, so let's click **Enter formula** and convert this to seconds by entering `A / 1000000000`.  Then we can hide `A` and show only `B`:

![Chart with Seconds](../images/chart_with_seconds.png)

Next, let's break down the chart by credit score category. Click on the **Add analytics** button on the first row, select **Mean**, then **Mean:Aggregation**, then Group By the `credit_score_category` dimension:

![Duration by Credit Score](../images/duration_by_credit_score.png)

Now we can see the duration by credit score category. In my example, the green line represents the `exceptional` category, and we can see that the duration for these requests sometimes goes all the way up to 5 seconds.

The yellow line represents the `very good` category, and has very fast response times.

The magenta line represents the `poor` category, and has response times between 2-3 seconds.

It may be useful to save this chart on a dashboard for future reference. To do this, click on the **Save as...** button and provide a name for the chart:

![Save Chart As](../images/save_chart_as.png)

When asked which dashboard to save the chart to, let's create a new one named `Credit Check Service`:

![Save Chart As](../images/create_dashboard.png)

Now we can see the chart on our dashboard, and can add more charts as needed to monitor our credit check service:

![Credit Check Service Dashboard](../images/credit_check_service_dashboard.png)

### Alerts

It's great that we have a dashboard to monitor the response times of the credit check service by credit score, but we don't want to stare at a dashboard all day.

Let's create an alert so we can be notified proactively if customers with `exceptional` credit scores encounter slow requests.

To create this alert, click on the little bell on the top right-hand corner of the chart, then select **New detector from chart**:

![New Detector From Chart](../images/new_detector_from_chart.png)

Let's call the detector `Latency by Credit Score Category`.  Set the environment to your environment name (i.e. `tagging-workshop-yourname`) then select `creditcheckservice` as the service. Since we only want to look at performance for customers with `exceptional` credit scores, add a filter using the `credit_score_category` dimension and select `exceptional`:

![Create New Detector](../images/create_new_detector.png)

We can then set the remainder of the alert details as we normally would. The key thing to remember here is that without capturing a tag with the credit score category and indexing it, we wouldn't be able to alert at this granular level, but would instead be forced to bucket all customers together, regardless of their importance to the business.
