---
title: Update Pipeline and Visualize Metrics
linkTitle: 4. Update Pipeline and Visualize Metrics
weight: 1
---

## Context Matters

In the previous section, you reviewed the raw Kubernetes audit logs and created an Ingest Processor Pipeline to convert them to metrics and send those  metrics to Splunk Observability Cloud. 

Now that this pipeline is defined we are collecting the new metrics in Splunk Observability Cloud. This is a great start; however, you will only see a single metric showing the total number of kubernetes audit events for a given time period. It would be much more valuable to add dimensions so that you can split the metric by the event type, user, response status, and so on. 

In this section you will update the Ingest Processor Pipeline to include additional dimensions from the Kubernetes audit logs to the metrics that are being collected. This will allow you to further filter, group, visualize, and alert on specific aspects of the audit logs. After updating the metric, you will create a new dashboard showing the status of the different types of actions associated with the logs. 