---
title: Trace and Investigate Agent Behavior
linkTitle: 5. Trace and Investigate
weight: 5
time: 10 minutes
---

Now that traces are flowing, let's use them. In this chapter you'll pivot into Splunk Agent
Observability and investigate exactly what your agent did on each request: the reasoning, the
tool calls, the retrieved context, the tokens, and the latency, all in one place.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you finally have complete visibility into the
assistant. When a patient reports a bad answer, you no longer guess; you open the trace and
see the exact path the agent took to get there.

{{% /notice %}}

> [!splunk] **Instant visibility.** Splunk Agent Observability shows the root cause of errors
> across complex, multi-step agent workflows. Instead of stitching together logs, you see the
> full request as a tree of spans you can expand and inspect.

The traces you'll explore here come from the instrumented app in
`~/workshop/healthcare-assistant/2-app-with-instrumentation` (the traffic you generated in the
previous chapter).

Continue to explore and investigate a trace.
