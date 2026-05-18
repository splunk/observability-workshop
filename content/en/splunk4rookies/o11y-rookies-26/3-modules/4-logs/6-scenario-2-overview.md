---
title: 6. Scenario 2 — TBD
weight: 6
---

{{% notice title="Under Development" style="warning" icon="triangle-exclamation" %}}
This scenario is under development. The content below is a placeholder.
{{% /notice %}}

## Candidate Scenarios

Two directions are being considered for this second scenario:

**Option A: Error Spike Investigation**
An error spike appears in a specific time window. You must use Log Observer to identify when it started, which services are affected, and correlate with deployment events to determine what changed.

**Option B: Cross-Service Log Correlation**
A user-facing failure leaves breadcrumbs across multiple services. You use Log Observer filtering and field analysis to trace the problem across service boundaries — stitching the story together from logs alone, without using APM traces.

Both options build on the filtering and grouping skills from Scenario 1 while introducing more advanced Log Observer techniques.
