---
title: 3. Validate Recovery and Close the Alert
weight: 3
---

Remediation is not complete when a command returns successfully. It is complete when the alert condition, service behavior, and user impact have recovered.

{{% notice title="Exercise" style="green" icon="running" %}}

After completing the action plan steps:

* Return to the alert page and review whether the alert is still firing.
* Check the detector chart over a time range that includes:
  * The pre-incident baseline.
  * The alert trigger.
  * The remediation action.
  * The recovery window.
* Validate the affected domain:
  * For APM: check service RED metrics, endpoints, traces, and error or latency outliers.
  * For Kubernetes: check workload health, pod restarts, node pressure, and resource utilization.
* Confirm that downstream services or workloads did not move into a worse state after the remediation.
* In the action plan, complete any final summary step.
* If the outcome is satisfactory, mark the alert as resolved and close the incident through your normal process.

{{< tabs >}}
{{% tab title="Question" %}}
**What validation signal is more trustworthy than a successful remediation command?**
{{% /tab %}}
{{% tab title="Answer" %}}
**A time-aligned return to healthy service or infrastructure telemetry, plus confirmation that the original alert condition cleared.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Closure Note Template

```markdown
## Closure Note

- Root cause accepted:
- Evidence used:
- Remediation action:
- Rollback prepared:
- Validation signal:
- Alert resolved at:
- Follow-up work:
```

