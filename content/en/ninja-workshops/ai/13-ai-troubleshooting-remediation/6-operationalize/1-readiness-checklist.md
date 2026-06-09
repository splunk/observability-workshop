---
title: 1. Team Readiness Checklist
weight: 1
---

Use this checklist before telling a team that AI troubleshooting will be part of its incident response process.

{{% notice title="Exercise" style="green" icon="running" %}}

Score one service team using the checklist.

| Area | Ready when | Score |
|------|------------|-------|
| Feature access | Team uses a `us1` Observability Cloud org where the feature is enabled. | |
| Supported detectors | Critical APM and Kubernetes alerts use supported standard/default metrics where applicable. | |
| Metadata | Services, environments, versions, Kubernetes namespaces, workloads, pods, and nodes are consistently tagged. | |
| Ownership | Alerts identify the owning team, escalation route, and business service. | |
| Telemetry quality | Metrics, traces, logs, and infrastructure data are available for the same time window. | |
| Notification path | Alerts reach responders through email, Slack, ServiceNow, or another managed route. | |
| Access | Responders can view evidence and run approved diagnostic commands. | |
| Change control | State-changing remediation has an approval and rollback path. | |
| Feedback loop | Teams know when to rate AI results and how to report gaps. | |

* Mark each row as **Ready**, **Partial**, or **Not Ready**.
* Pick the two lowest-scoring rows and convert them into action items.
* Decide whether the team should use full remediation, read-only action plans, or tabletop review until gaps are closed.

{{< tabs >}}
{{% tab title="Question" %}}
**Which readiness item usually has the highest leverage?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Consistent metadata and ownership usually have the highest leverage because they improve correlation, routing, evidence review, and accountability at the same time.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

