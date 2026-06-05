---
title: 4. Timeline and Patterns
weight: 4
---

You've narrowed down to error logs from a single service. Now let's understand *when* the problem started and *what* the errors look like.

{{% notice title="Exercise" style="green" icon="running" %}}

**Step 1: Analyze the Timeline**

* Look at the timeline chart at the top of the page. Focus on the shape of the error bars.

{{< tabs >}}
{{% tab title="Question" %}}
**Is the error rate constant, or did it spike at a specific time? What might that tell you?**
{{% /tab %}}
{{% tab title="Answer" %}}
A sudden spike suggests a deployment, configuration change, or external dependency failure at that point in time. A constant error rate suggests the issue has been present since the service started. Both patterns are clues to the root cause.
{{% /tab %}}
{{< /tabs >}}

<!-- TODO screenshot: Timeline showing error spike pattern -->

**Step 2: Expand a Log Entry**

* Click on a representative error log entry in the table to expand it.
* The detail pane shows all structured fields attached to the log entry.

Examine these key fields:

| Field | What it tells you |
|-------|-------------------|
| `message` | The actual error text — often contains the root cause |
| `service.name` | Confirms which service emitted the log |
| `k8s.pod.name` | The specific pod instance |
| `deployment.environment` | Your workshop environment |
| `severity` | The log level (should be ERROR) |

<!-- TODO screenshot: Expanded log entry showing structured fields -->

**Step 3: Look for Patterns**

* Scroll through several error entries. Do they all have the same message, or are there different error types?
* Note any version tags, deployment identifiers, or dependency references in the log messages.

{{< tabs >}}
{{% tab title="Question" %}}
**Do all the error logs share the same message pattern, or are there multiple distinct errors?**
{{% /tab %}}
{{% tab title="Answer" %}}
<!-- TODO: Update with actual patterns from OTel Demo v2.0.1 -->
Look for repeating message templates. If all errors share the same pattern, you likely have a single root cause. Multiple patterns may indicate cascading failures.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Info" style="info" %}}
Structured logging with OpenTelemetry means every log entry carries consistent, queryable fields. This is what makes Log Observer's no-code filtering so effective — the structure is built into the data, not imposed after the fact.
{{% /notice %}}
