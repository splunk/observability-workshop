---
title: 2. Create or Select a Supported Alert Scenario
weight: 2
---

A good workshop alert is specific enough for the agent to reason about and realistic enough for responders to practice decision-making. The target is not merely "make something red." The target is a supported alert with enough correlated telemetry to evaluate hypotheses.

{{% notice title="Exercise" style="green" icon="running" %}}

Choose one of the following paths.

**Path A: Use an existing active alert**

* In **Active Alerts**, filter by your workshop environment or service owner tag.
* Select an alert from an APM service or Kubernetes detector.
* Verify that the alert has enough history to show behavior before and after the trigger time.
* Confirm that the alert maps to a real owner, service, workload, or cluster.

**Path B: Use a lab detector**

* In a non-production environment, create or clone a detector from an APM or Kubernetes detector template that uses standard/default metrics.
* Configure notifications to a workshop-only email, Slack channel, or ServiceNow target.
* Trigger a known lab issue, such as a controlled error-rate increase, latency injection, pod restart loop, or resource saturation.
* Restore the detector threshold after the alert is generated so the workshop does not create unnecessary alert noise.

{{< tabs >}}
{{% tab title="Question" %}}
**What makes an alert useful for AI-assisted troubleshooting instead of just useful for notification?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It has a supported detector type, clear ownership, aligned APM or Kubernetes metadata, and enough correlated metrics, traces, logs, or events for the agent to evaluate hypotheses.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Scenario Quality Checklist

Use this checklist before the group begins the investigation:

| Check | Why it matters |
|-------|----------------|
| Alert is active or recently resolved | The alert page has a bounded investigation window. |
| Detector uses supported standard metrics | The AI troubleshooting feature can run in the expected path. |
| Service or Kubernetes object is named clearly | Responders can connect AI output to operational ownership. |
| Telemetry has consistent `service.name`, `environment`, and Kubernetes metadata | Evidence can be correlated across product areas. |
| Alert has enough impact to discuss | The team can practice prioritization and blast-radius review. |
| Remediation environment is controlled | Suggested commands can be reviewed and tested without production risk. |

