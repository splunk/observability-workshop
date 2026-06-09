---
title: 2. Review Root Cause Analysis
weight: 2
---

The **Root Cause Analysis** tab expands the investigation. It presents suspected root causes and links to relevant Splunk Observability Cloud views so responders can inspect the suspicious behavior in context.

{{% notice title="Exercise" style="green" icon="running" %}}

* Open the **Root Cause Analysis** tab.
* Watch the AI Assistant chat area for investigation status. Root cause analysis can continue running after you leave the alert page. It runs once per user, and the existing results are available when you return.
* Review the suspected root causes one at a time.
* For each root cause, add this row to your incident notes:

| Hypothesis | Supporting signal | Weak signal or gap | Next action |
|------------|-------------------|--------------------|-------------|
| | | | |

* Follow the links in the suspected root cause summary to inspect the related Splunk Observability component, such as an APM service, trace, log set, Kubernetes workload, pod, or node.
* If the data changed materially since the first run, use the available regenerate option for the analysis path you are investigating.
* After reviewing the result quality, use the thumbs up or thumbs down feedback controls in the chat to rate the investigation.

{{< tabs >}}
{{% tab title="Question" %}}
**When should you regenerate root cause analysis instead of continuing with the existing result?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Regenerate when new telemetry, a changed time range, or an updated alert state makes the current hypothesis stale or incomplete.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Investigation Discipline" style="info" %}}
A useful AI-generated root cause is specific, time-aligned, and falsifiable. If the summary is broad, ask what concrete signal would prove or disprove it before moving to remediation.
{{% /notice %}}
