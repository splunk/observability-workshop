---
title: 2. Building In Resilience
linkTitle: 2. Building Resilience
time: 10 minutes
weight: 4
---

The OpenTelemetry Collector’s [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) is a critical component for building a more resilient telemetry pipeline. It enables the Collector to reliably checkpoint in-flight data, manage retries efficiently, and gracefully handle temporary failures without losing valuable telemetry.

With FileStorage enabled, the Collector can persist intermediate states to disk, ensuring that your traces, metrics, and logs are not lost during network disruptions, backend outages, or Collector restarts. This means that even if your network connection drops or your backend becomes temporarily unavailable, the Collector will continue to receive and buffer telemetry, resuming delivery seamlessly once connectivity is restored.

By integrating the FileStorage Extension into your pipeline, you can strengthen the durability of your observability stack and maintain high-quality telemetry ingestion, even in environments where connectivity may be unreliable.
{{% notice note %}}

This solution will work for metrics as long as the connection downtime is brief, up to 15 minutes. If the downtime exceeds this, Splunk Observability Cloud might  drop data to make sure no data-point is out of order.

For logs, there are plans to implement a full enterprise-ready solution in one of the upcoming Splunk OpenTelemetry Collector releases.

{{% /notice %}}
