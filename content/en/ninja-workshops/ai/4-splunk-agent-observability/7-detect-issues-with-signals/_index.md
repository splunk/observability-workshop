---
title: Surface Emerging Issues with Signals
linkTitle: 7. Surface Issues with Signals
weight: 7
time: 5 minutes
---

Metrics catch the problems you knew to measure. But agentic systems fail in ways you didn't
anticipate, like planning loops, routing failures, and tool errors. **Signals** find those
*unknown unknowns* for you.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you can't write a metric for every possible
failure mode, and you don't have time to read every trace. You need the platform to tell you,
proactively, "here's a pattern that's going wrong, and here's what to do about it."

{{% /notice %}}

> [!splunk] **Signals** automatically surface recurring failure patterns from your production
> traces and provide actionable context: *what* went wrong, *why* it happened, and *what to do
> next*, turning weeks of post-incident analysis into minutes of targeted remediation.

{{% notice title="What Signals detect" style="info" %}}

Signals analyze your traces to surface patterns such as:

* **Planning loops**: the agent spinning without converging.
* **Tool errors**: failing or misused tool calls.
* **Hallucinations**: ungrounded or fabricated content.
* **Routing failures**: the agent taking the wrong path.

…and more, including emerging patterns you never thought to define.

{{% /notice %}}

Continue to explore Signals in the console.
