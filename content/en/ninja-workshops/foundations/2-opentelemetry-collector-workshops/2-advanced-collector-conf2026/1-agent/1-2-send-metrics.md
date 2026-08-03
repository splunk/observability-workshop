---
title: 1.2 Validate and Test Host Metrics
linkTitle: 1.2 Validate Host Metrics
weight: 2
---

The Agent is configured to collect host metrics automatically. We will verify
that the receiver, processors, and debug exporter form a working local metrics
pipeline.

{{% exercise title="Validate host metrics" %}}

**Verify the Agent is running:** The foreground Collector from Step 1.1 must
still be running in the **Agent Console**. If it is not, start it again using
the command in Step 1.1.

**Verify host metrics:**

1. Leave the **Agent Console** running for at least 10 seconds.
2. Confirm that the Agent displays host metrics in its detailed debug output.
3. On Linux, look for metrics such as `system.cpu.time`,
   `system.memory.usage`, `system.cpu.load_average.1m`, and
   `system.network.io`. Apple
   Silicon can expose a different OS-supported subset, so validate the
   `system.*` metrics that appear in your console.

The output should resemble the following snippet:

```text
NumberDataPoints #31
Data point attributes:
     -> state: Str(wait)
StartTimestamp: 2026-08-02 10:00:00 +0000 UTC
Timestamp: 2026-08-02 10:00:10 +0000 UTC
Value: 77.380000
        {"otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "metrics"}
```

Version `0.157.0` aggregates CPU metrics across logical CPUs by default, so
your output might not contain a separate `cpu` attribute for every processor.

At this stage, the Agent continues to collect host metrics every 10 seconds.
The metrics are always written to the local debug console and
`agent-metrics.out`. With valid cloud credentials, the default `signalfx`
exporter also sends them to Infrastructure Monitoring.

{{% /exercise %}}
