---
title: Adding Context With Tags
linkTitle: 2.2 Adding Context With Tags
weight: 3
authors: ["Tim Hard"]
time: 3 minutes
draft: false
---

When you [deployed the OpenTelemetry Demo Application](../getting_started/2-deploy-application/) in the [Getting Started](../getting_started/) section of this workshop, you were asked to enter your favorite city. For this workshop, we'll be using that to show the value of custom tags.

For this workshop, the OpenTelemetry collector is pre-configured to use the city you provided as a custom tag called `store.location` which will be used to emulate Kubernetes Clusters running in different geographic locations. We'll use this tag as a filter to show how you can use Out-of-the-Box integration dashboards to quickly create views for specific teams, applications, or other attributes about your environment. Efficiently enabling content to be reused across teams without increasing technical debt.

Here is the OpenTelemetry Collector configuration used to add the `store.location` tag to all of the data sent to this collector. This means any metrics, traces, or logs will contain the `store.location` tag which can then be used to search, filter, or correlate on this value.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
If you're interested in a deeper dive on the **OpenTelemetry Collector**, head over to the [**Self Service Observability**](../../self_service_observability/) workshop where you can get hands-on with configuring the collector or the [**OpenTelemetry Collector Ninja Workshop**](../../../../other/5-opentelemetry-collector) where you'll dissect the inner workings of each collector component.
{{% /notice %}}

![OpenTelemetry Collector Configuration](../../images/otel-config.png?width=60vw)

While this example is using a hard-coded value for the tag, parameterized values can also be used, allowing you to customize the tags dynamically based on the context of each host, application, or operation. This flexibility enables you to capture relevant metadata, user-specific details, or system parameters, providing rich context for metric, tracing, and log data while enhancing the observability of your distributed systems.

Now that you have the appropriate context, which as we've established is critical to Observability, lets head over to **Splunk Observability Cloud** and see how we can use the data we've just configured.  