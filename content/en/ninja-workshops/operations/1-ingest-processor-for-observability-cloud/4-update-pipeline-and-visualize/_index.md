---
title: Update Pipeline and Visualize Metrics
linkTitle: 4. Update Pipeline and Visualize Metrics
weight: 1
---

## Context Matters

In the previous section, you reviewed the raw Kubernetes audit logs and created an Ingest Processor Pipeline to convert them to metrics and send those metrics to Splunk Observability Cloud.

Now that this pipeline is defined we are collecting the new metrics in Splunk Observability Cloud. This is a great start; however, you will only see a single metric showing the total number of Kubernetes audit events for a given time period. It would be much more valuable to add dimensions so that you can split the metric by the event type, user, response status, and so on.

In this section you will update the Ingest Processor Pipeline to include additional dimensions from the Kubernetes audit logs to the metrics that are being collected. This will allow you to further filter, group, visualize, and alert on specific aspects of the audit logs.

## Why Metric Cardinality Matters

Every unique combination of a metric name and its dimension values creates a distinct **Metric Time Series (MTS)**. The number of active MTS, also known as cardinality, is what determines your metrics utilization in Splunk Observability Cloud. Adding dimensions makes your metrics far more useful, but not every dimension is worth keeping. High-cardinality dimensions, those that have a unique or near-unique value on every event, can cause the number of MTS to explode, which inflates your utilization without adding any analytical value.

To demonstrate this, you will add the `auditID` dimension to the pipeline. Because Kubernetes assigns a unique `auditID` to every single audit event, this field is guaranteed to be unique. Adding it as a dimension means that every metric data point produces a brand new MTS, turning what should be a small, well-organized metric into thousands of single-use time series. This is a classic example of cardinality explosion, and it is something that can easily happen by accident when teams add convenient but overly granular dimensions to their data.

## Optimizing with Metrics Pipeline Management

Once that noisy dimension is in place, you will use **Metrics Pipeline Management (MPM)** in Splunk Observability Cloud to bring cardinality back under control. MPM lets you aggregate, archive, or drop metrics and dimensions after the data arrives, so you can optimize your utilization without changing anything at the ingest endpoint (the collector, the Ingest Processor Pipeline, or the applications sending data). This is a key advantage: you get full control over your metrics directly from the UI, without having to coordinate changes across every team or redefine your ingest pipelines.

You will create an aggregation rule that rolls the data up into a new, lower-cardinality metric that drops the unique `auditID` dimension, and then drop the raw, high-cardinality metric you no longer need. Along the way you will see the exact reduction in MTS, giving you a concrete measure of the utilization you reclaimed.

After optimizing the metric, you will create a new dashboard showing the status of the different types of actions associated with the logs.
