---
title: 4. Building In Resilience
linkTitle: 4. Building Resilience
time: 10 minutes
weight: 4
---

The OpenTelemetry Collector’s [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) enhances the resilience of your telemetry pipeline by providing reliable checkpointing, managing retries, and handling temporary failures effectively.  

With this extension enabled, the OpenTelemetry Collector can store intermediate states on disk, preventing data loss during network disruptions and allowing it to resume operations seamlessly.

{{% notice note %}}

This solution will work for metrics as long as the connection downtime is brief—up to 15 minutes. If the downtime exceeds this, Splunk Observability Cloud will drop data due to datapoints being out of order.

For logs, there are plans to implement a more enterprise-ready solution in one of the upcoming Splunk OpenTelemetry Collector releases.

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `4-resilience`.
- Next, copy all contents from the `3-filelog` directory into `4-resilience`.
- After copying, remove any `*.out` and `*.log` files.
- Change **all** terminal windows to the `[WORKSHOP]/4-reslilience` directory.

Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /notice %}}
