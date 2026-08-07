---
title: 1.4 Send Logs
linkTitle: 1.4 Send Logs
weight: 4
---

{{% exercise title="Send logs through the pipeline" %}}

**Start the log load generator:** In the **Command terminal**, run:

```bash
../loadgen -logs
```

The command writes a continuous stream of quotes to `quotes.log`. The
`file_log/quotes` receiver reads the file, converts each line into an
OpenTelemetry log record, and sends it through `logs/workshop` to the Agent
debug and file exporters.

The **Agent Console** should display output similar to:

```text { title="Agent Debug Output" }
Timestamp: 1970-01-01 00:00:00 +0000 UTC
ObservedTimestamp: 2026-08-02 10:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(2026-08-02 10:00:00 [ERROR] - There is some good in this world, and it's worth fighting for. LOTR)
Attributes:
     -> log.file.path: Str(/path/to/advanced-collector-conf2026/quotes.log)
Trace ID:
Span ID:
Flags: 0
```

The log resource also includes attributes such as:

```text
service.name: quote-generator
com.splunk.sourcetype: quotes
host.name: workshop-instance
os.type: linux
otelcol.service.mode: agent
```

**Stop `loadgen`:** Press `Ctrl-C` in the **Command terminal**.

At this point, the workshop directory contains:

```text { title="Updated Directory Structure" }
.
├── agent-logs.out
├── agent-traces.out
├── agent-metrics.out
├── agent_config.yaml
└── quotes.log
```

The log is available in the console and `agent-logs.out`.

{{% /exercise %}}
