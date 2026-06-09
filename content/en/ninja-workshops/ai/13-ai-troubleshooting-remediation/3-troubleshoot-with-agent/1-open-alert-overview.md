---
title: 1. Open the Alert Overview
weight: 1
---

The **Overview** tab is the first stop. It summarizes the alert, the triggering rule, the impact analysis, the primary root cause, and additional troubleshooting information. Use it to decide how urgent the incident is and which responders need to be involved.

{{% notice title="Exercise" style="green" icon="running" %}}

* Open the alert from your notification link or from **Alerts & Detectors** > **Active Alerts**.
* Review the available tabs:
  * **Overview**
  * **Root Cause Analysis**
  * **Evidence**
* On **Overview**, capture the following:

| Area | What to capture |
|------|-----------------|
| Alert summary | Rule triggered, severity, detector, and start time. |
| Impact analysis | Affected applications, services, workloads, or infrastructure objects. |
| Primary root cause | The top suspected cause presented by the agent. |
| Additional troubleshooting information | Any linked services, traces, logs, charts, or Kubernetes objects. |

* Update your incident brief with the first-pass impact and suspected root cause.
* If the alert indicates customer-facing impact, assign a communications owner before continuing.

{{< tabs >}}
{{% tab title="Question" %}}
**What should you decide before moving from Overview to deeper root cause analysis?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Decide the severity, impacted domain, responsible owner, and whether the primary root cause is plausible enough to investigate first.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Triage Guidance

Do not treat the top root cause as final just because it appears on the Overview tab. Treat it as the best current hypothesis and look for corroborating evidence in the next pages.

