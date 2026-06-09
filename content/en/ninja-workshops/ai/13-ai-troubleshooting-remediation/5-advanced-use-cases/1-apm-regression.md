---
title: 1. APM Deployment Regression
weight: 1
---

Deployment regressions are a strong fit for AI-assisted troubleshooting because the agent can correlate alert timing, service behavior, traces, logs, and metadata such as version or environment.

{{% notice title="Exercise" style="green" icon="running" %}}

Use an APM service alert where latency, error rate, or request rate changed near a deployment.

* On **Overview**, confirm the affected service and impact radius.
* On **Root Cause Analysis**, look for suspected causes that reference:
  * A service version or deployment marker.
  * A specific endpoint or operation.
  * A dependency that became slow or erroring.
  * A log or trace pattern that started near the alert time.
* On **Evidence**, compare affected and unaffected dimensions:

| Dimension | Example question |
|-----------|------------------|
| `version` | Is one version worse than the previous version? |
| `environment` | Is the issue isolated to one environment? |
| Endpoint | Did one route or RPC method regress? |
| Dependency | Did a downstream service or database become the bottleneck? |
| Customer or tenant tag | Is impact isolated to a subset of traffic? |

* Open the action plan and choose the deployment-regression hypothesis if the evidence supports it.
* Prefer a low-risk action sequence:
  * Confirm deployment timing.
  * Compare traces between healthy and unhealthy versions.
  * Check logs for new error signatures.
  * Roll back or disable a feature flag only after approval.

{{< tabs >}}
{{% tab title="Question" %}}
**What evidence would make a rollback more defensible than a scale-out action?**
{{% /tab %}}
{{% tab title="Answer" %}}
**A clear version-specific regression where the new version shows elevated errors or latency while the previous version remains healthy.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Advanced Pattern

Use the agent to accelerate the first pass, then use APM views to prove the version split. A rollback should be tied to a specific bad change, not just a general alert.

