---
title: 3. Filelog Setup
linkTitle: 3. Filelog Setup
time: 10 minutes
weight: 3
---

The **FileLog** receiver in the OpenTelemetry Collector is used to ingest logs from files.

It monitors specified files for new log entries and streams those logs into the Collector for further processing or exporting. It is useful for testing and development purposes.

For this part of the workshop, there is script that will generate log lines in a file. The Filelog receiver will read these log lines and send them to the OpenTelemetry Collector.

{{% notice title="Exercise" style="green" icon="running" %}}

- Move to the **log-gen** terminal window.
- Navigate to the `[WORKSHOP]` directory and create a new subdirectory named `3-filelog`.
- Next, copy all contents from the `2-gateway` directory into `3-filelog`.
- After copying, remove any `*.out` and `*.log` files.

Your updated directory structure will now look like this:

{{% tabs %}}
{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
│   ├── agent.yaml          # Agent Collector configuration file
│   ├── gateway.yaml        # Gateway Collector configuration file
│   └── trace.json          # Example trace file
└── otelcol                 # OpenTelemetry binary
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}
