---
title: 1.2 Validate host metrics
linkTitle: 1.2 Validate host metrics
weight: 2
---

{{% exercise title="Validate the workshop metrics pipeline locally" %}}

The **Agent terminal** displays a metrics block after startup, similar to:

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

If you enabled cloud export, you verify host metrics in Splunk Observability
Cloud in Step 1.5.

{{% /exercise %}}
