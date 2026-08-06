---
title: 1.2 Validate and Test Host Metrics
linkTitle: 1.2 Validate Host Metrics
weight: 2
---

The metrics pipeline follows the original workshop pattern: it collects CPU
metrics at startup and then once per hour. This keeps detailed debug output
readable.

{{% exercise title="Validate host metrics locally" %}}

The **Agent Console** should show one metrics block after startup, similar to:

```text
Metric #0
Descriptor:
     -> Name: system.cpu.time
NumberDataPoints: ...
```

If it has scrolled away, check the local output file:

```bash
cd [WORKSHOP]/1-agent
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

When cloud export is enabled, this same metrics pipeline also sends the batch
to Splunk Observability Cloud. Cloud verification is optional and appears in
Step 5.2.

{{% /exercise %}}
