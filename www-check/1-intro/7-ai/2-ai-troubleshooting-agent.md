---
title: 2. AI Troubleshooting Agent
weight: 2
---

When a **detector** fires on an APM service or a Kubernetes component, Splunk Observability Cloud **automatically triggers the AI Troubleshooting Agent**. It behaves like a fellow SRE: it correlates metrics, events, logs and traces across your environment and presents **evidence-backed suspected root causes** in plain language — no dashboard-hopping required.

Your instructor has a detector firing on the **paymentservice error rate** (the same fault you've been chasing).

{{% exercise title="Read the AI-generated root cause" %}}

* Open the firing **alert / incident** from the bell icon, or from **Alerts & Detectors**.
* Open the **Root Cause Analysis** tab.
* Read the ranked **suspected root causes**. Each is written in plain language.
* Open the **Evidence** tab to see the exact logs, exemplar traces and APM services that support each hypothesis — click through to the same trace and log lines you found manually earlier.

{{< tabs >}}
{{% tab title="Question" %}}
**How does the agent's suspected root cause compare with what you found in the APM and Logs sections?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It matches.** The agent identifies `paymentservice` as the originating source of errors (with `checkoutservice` errors inherited downstream), backs it with exemplar error traces and the failing log lines, and assesses the immediate impact on affected services and user sessions — the same conclusion, reached automatically.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

## The Remediation Plan

Diagnosis is only half the job. Below a suspected root cause, the **AI Remediation Plan** turns the finding into guided, **human-verified** steps.

{{% exercise title="Work through the action plan" %}}

* Below a suspected root cause, click **View AI-generated action plan**.
* The plan pairs **hypotheses** with concrete **actions** (for our fault, that's rolling back the bad `paymentservice` version — or, if the fault was injected via a feature flag, disabling that flag).
* Select a hypothesis and a root cause, then walk through the actions to resolve the alert.

{{% /exercise %}}

{{% notice style="blue" title="Why this matters" icon="circle-info" %}}
The AI Troubleshooting Agent collapses **MTTI**. A brand-new engineer gets the same evidence-backed answer a veteran SRE would reach — the agent removes the knowledge barrier, and you stay in control because the remediation plan is human-verified. You still own the decision; the AI just did the legwork.
{{% /notice %}}
