---
title: 3. Build the Incident Brief
weight: 3
---

AI-assisted troubleshooting works best when humans establish the operating frame. The brief keeps responders aligned while the agent evaluates root causes and evidence.

{{% notice title="Exercise" style="green" icon="running" %}}

Create a short incident brief before opening the AI-generated analysis.

```markdown
## Incident Brief

- Alert:
- Detector:
- Time started:
- Environment:
- Affected service or Kubernetes object:
- User or business impact:
- Recent deployments or configuration changes:
- Known maintenance windows:
- Initial severity:
- Incident commander:
- Service owner:
- Scribe:
- Allowed remediation scope:
- Rollback owner:
```

* Add the alert URL to the brief.
* Add any known recent change, such as a deployment, feature flag, scaling event, or cluster maintenance.
* Define what responders are allowed to do during the workshop:
  * Read-only investigation only.
  * Read-only investigation plus approved lab commands.
  * Full remediation in a non-production environment.
* Keep the brief open in a separate tab. You will update it as the agent surfaces root causes and remediation steps.

{{< tabs >}}
{{% tab title="Question" %}}
**Why write an incident brief before reviewing AI output?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It separates known facts and operational constraints from AI-generated hypotheses, making it easier to validate, reject, or act on the agent's suggestions.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Practice" style="info" %}}
Assign a scribe for the workshop. The scribe should record each hypothesis, the evidence that supported or weakened it, the remediation action selected, and the validation result. This becomes the raw material for the wrap-up and post-incident review.
{{% /notice %}}

