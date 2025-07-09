---
title: 2. Building In Resilience
linkTitle: 2. Building Resilience
time: 10 minutes
weight: 4
---

The OpenTelemetry Collector’s [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) enhances the resilience of your telemetry pipeline by providing reliable check-pointing, managing retries, and handling temporary failures effectively.  

With this extension enabled, the OpenTelemetry Collector can store intermediate states on disk, preventing data loss during network disruptions and allowing it to resume operations seamlessly.

{{% notice note %}}

This solution will work for metrics as long as the connection downtime is brief—up to 15 minutes. If the downtime exceeds this, Splunk Observability Cloud will drop data due to datapoints being out of order.

For logs, there are plans to implement a more enterprise-ready solution in one of the upcoming Splunk OpenTelemetry Collector releases.

{{% /notice %}}
