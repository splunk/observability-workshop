---
title: 2. AI-Assisted Incident Runbook Template
weight: 2
---

A reusable runbook prevents every team from inventing its own AI-assisted incident process. The template should say when to use the feature, how to validate output, and what to record.

{{% notice title="Exercise" style="green" icon="running" %}}

Copy this runbook template into your incident documentation system and adapt it for one service team.

```markdown
# AI-Assisted Incident Runbook

## Scope

Use this runbook for Splunk Observability Cloud alerts from supported APM service or Kubernetes detectors in the `us1` realm.

Do not use this runbook as the sole remediation process for unsupported custom metric detectors, security-sensitive changes, or production changes without approval.

## Roles

- Incident commander:
- Service owner:
- Scribe:
- Change approver:
- Communications owner:

## Investigation

1. Open the alert Overview tab.
2. Record severity, impacted component, and primary suspected root cause.
3. Open Root Cause Analysis.
4. Review each suspected root cause as a hypothesis.
5. Open Evidence and record supporting and contradictory signals.
6. Rate the AI investigation result when enough evidence has been reviewed.

## Remediation

1. Open the AI-generated action plan for the selected root cause.
2. Classify each step as read-only, diagnostic with load, state-changing, or code-changing.
3. Run read-only diagnostics first.
4. Submit command output to the plan.
5. Execute state-changing steps only after approval and rollback review.
6. Mark steps completed only after command success and telemetry validation.

## Validation

1. Confirm the alert condition has cleared.
2. Confirm service or Kubernetes health in the product view.
3. Confirm downstream impact has not worsened.
4. Record the final root cause, action, and follow-up work.
```

{{% /notice %}}

## Suggested Runbook Links

Add links to the service's normal operating material:

| Link | Purpose |
|------|---------|
| Service dashboard | Validate service health after remediation. |
| Detector list | Find related alerts or mute noisy lab detectors. |
| Deployment history | Confirm version changes and rollback targets. |
| Kubernetes namespace dashboard | Confirm workload and pod recovery. |
| On-call schedule | Find the service owner and approver. |
| Post-incident template | Convert workshop notes into follow-up work. |

