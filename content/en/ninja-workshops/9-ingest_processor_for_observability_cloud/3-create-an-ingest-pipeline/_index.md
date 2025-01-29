---
title: Create an Ingest Pipeline
linkTitle: 3. Create an Ingest Pipeline
weight: 1
---

## Scenario Overview

In this scenario you will be playing the role of a Splunk Admin responsible for managing your organizations Splunk Enterprise Cloud environment. You recently worked with an internal application team on instrumenting their Kubernetes environment with Splunk APM and Infrastructure monitoring using OpenTelemetry to monitor their critical microservice applications.

The logs from the Kubernetes environment are also being collected and sent to Splunk Enter Prize Cloud. These logs include:

* Pod logs (application logs)
* Kubernetes Events
* Kubernetes Cluster Logs
    * Control Plane Node logs
    * Worker Node logs
    * Audit Logs

As a Splunk Admin you want to ensure that the data you are collecting is optimized so it can be analyzed in the most efficient way possible. Taking this approach accelerates troubleshooting and ensures efficient license utilization.

One way to accomplish this is by using Ingest Processor to convert robust logs to metrics and use Splunk Observability Cloud as the destination for those metrics. Not only does this make collecting the logs more efficient, you have the added ability of using the newly created metrics in Splunk Observability which can then be correlated with Splunk APM data (traces) and Splunk Infrastructure Monitoring data providing additional troubleshooting context. Because Splunk Observability Cloud uses a streaming metrics pipeline, the metrics can be alerted on in real-time speeding up problem identification. Additionally, you can use the Metrics Pipeline Management functionality to further optimize the data by aggregating, dropping unnecessary fields, and archiving less important or un-needed metrics.

In the next step you'll create an Ingest Processor Pipeline which will convert Kubernetes Audit Logs to metrics that will be sent to Observability Cloud.