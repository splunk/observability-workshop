---
title: 5. Identify the Root Cause
weight: 5
---

You've filtered to the right service, analyzed the timeline, and examined the error patterns. Time to identify the root cause.

{{% notice title="Exercise" style="green" icon="running" %}}

* Click on an error entry in the log table to open the detail pane.
* Read the `message` field carefully.

{{< tabs >}}
{{% tab title="Question" %}}
**Based on the error message, what is the root cause? What would you recommend to the development team?**
{{% /tab %}}
{{% tab title="Answer" %}}
<!-- TODO: Update with actual root cause from OTel Demo v2.0.1 fault injection -->
The error message reveals the specific failure. Based on this, you would recommend the development team investigate the failing component — whether it's an invalid configuration, an expired credential, a missing dependency, or a code defect.
{{% /tab %}}
{{< /tabs >}}

<!-- TODO screenshot: Log entry detail showing the root cause error message -->

* Click the **X** to close the log entry detail pane.

{{% /notice %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

You have successfully used **Splunk Log Observer** as a standalone investigation tool. Starting from scratch with no prior context — no traces, no metrics dashboards — you:

1. Opened Log Observer and set your environment filter
2. Grouped by severity and filtered to errors
3. Identified the failing service
4. Analyzed the error timeline to understand when the issue started
5. Inspected log entries to find the root cause

All within Log Observer, using only point-and-click filtering.

{{% /notice %}}

## Summary

| Technique | What it showed |
|-----------|---------------|
| Group by severity | Error vs info vs debug distribution across all services |
| Filter by service | Isolated the failing component from the noise |
| Timeline analysis | When the problem started — spike vs constant |
| Log entry inspection | The specific error message and root cause |

{{% notice title="Info" style="info" %}}
In this scenario, Log Observer was your **primary** investigation tool. In practice, you can also arrive at Log Observer from APM traces via **Related Content** — a feature that automatically correlates traces and logs using shared identifiers like `trace_id`. Both paths are valid; the right starting point depends on the signals available to you at the time of the incident.
{{% /notice %}}
