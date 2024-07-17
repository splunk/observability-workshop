---
title: Use Tags with Dashboards
linkTitle: 1. ...with Dashboards
weight: 1
time: 5 minutes
---

### Dashboards

Navigate to **Metric Finder**, then type in the name of the tag, which is `credit_score_category` (remember that the dots in the tag name were replaced by underscores when the Monitoring MetricSet was created).  You'll see that multiple metrics include this tag as a dimension:

![Metric Finder](../../images/metric_finder.png)

By default, **Splunk Observability Cloud** calculates several metrics using the trace data it receives.  See [Learn about MetricSets in APM](https://docs.splunk.com/observability/en/apm/span-tags/metricsets.html) for more details.

By creating an MMS, `credit_score_category` was added as a dimension to these metrics, which means that this dimension can now be used for alerting and dashboards.

To see how, let's click on the metric named `service.request.duration.ns.p99`, which brings up the following chart:

![Service Request Duration](../../images/service_request_duration_chart.png)

Add filters for `sf_environment`, `sf_service`, and `sf_dimensionalized`.  Then set the **Extrapolation policy** to `Last value` and the **Display units** to `Nanosecond`:

![Chart with Seconds](../../images/chart_settings.png)

With these settings, the chart allows us to visualize the service request duration by credit score category:

![Duration by Credit Score](../../images/duration_by_credit_score.png)

Now we can see the duration by credit score category. In my example, the red line represents the `exceptional` category, and we can see that the duration for these requests sometimes goes all the way up to 5 seconds.

The orange represents the `very good` category, and has very fast response times.

The green line represents the `poor` category, and has response times between 2-3 seconds.

It may be useful to save this chart on a dashboard for future reference. To do this, click on the **Save as...** button and provide a name for the chart:

![Save Chart As](../../images/save_chart_as.png)

When asked which dashboard to save the chart to, let's create a **new** one named `Credit Check Service - Your Name` (substituting your actual name):

![Save Chart As](../../images/create_dashboard.png)

Now we can see the chart on our dashboard, and can add more charts as needed to monitor our credit check service:

![Credit Check Service Dashboard](../../images/credit_check_service_dashboard.png)


