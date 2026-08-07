---
title: 1.2 Validate and Test Host Metrics
linkTitle: 1.2 Validate Host Metrics
weight: 2
---

The Agent has three metrics pipelines:

- `metrics` collects the normal host-metrics set every 10 seconds. Cloud
  setups send it to SignalFx; it is not connected to detailed debug.
- `metrics/workshop` follows the original workshop pattern. It collects CPU
  metrics at startup and then once per hour, and writes only that bounded batch
  to debug and `agent-metrics.out`.
- `metrics/internal` retains the default Collector self-monitoring path. It is
  not part of the hands-on validation.

{{% exercise title="Validate the workshop metrics pipeline locally" %}}

The **Agent Console** should show one metrics block after startup, similar to:

```text
Descriptor:
     -> Name: system.cpu.time
NumberDataPoints: ...
```

If it has scrolled away, run this in the **Command terminal**:

```bash
jq -r '
  .resourceMetrics[].scopeMetrics[].metrics[]
  | select(.name == "system.cpu.time")
  | .name
' agent-metrics.out | sort -u
```

Expected output:

```text
system.cpu.time
```

Cloud-enabled attendees verify the separate `metrics` pipeline later in
Splunk Observability Cloud.

{{% /exercise %}}
