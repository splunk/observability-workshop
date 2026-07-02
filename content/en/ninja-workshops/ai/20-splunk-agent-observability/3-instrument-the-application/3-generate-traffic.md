---
title: Generate Traffic
linkTitle: 3. Generate Traffic
weight: 3
time: 5 minutes
---

With the callback attached, run the instrumented app and send a few requests. Every turn now
produces a trace in Splunk Agent Observability. You'll explore those traces in detail in the
next chapter.

{{< exercise title="Run the app and generate traces" >}}

{{< step title="Run the app" >}}

From `2-app-with-instrumentation` (virtual environment active, database loaded, and your
Galileo credentials set in `.streamlit/secrets.toml`), start the app and open it in your
browser:

```bash
streamlit run ~/workshop/healthcare-assistant/2-app-with-instrumentation/app.py
```

{{< /step >}}

{{< step title="Send a few requests" >}}

Exercise both tool paths so you generate a RAG trace and a text-to-SQL trace:

> What is the dosage and common side effects of Lisinopril?

> Can you look up information for patient P001?

Then send a trickier medical question to give yourself something interesting to investigate
later:

> Is it safe to double my dose of Lisinopril if I miss a day?

Each message returns a normal answer; the callback doesn't change the app's behavior, it
just records it.

{{< /step >}}

{{< step title="Confirm traces are flowing" >}}

Watch the terminal where `streamlit run app.py` is running. With instrumentation in place, you
should see Galileo activity as each turn completes. The traces are now landing in your project
and log stream, ready to explore.

{{% notice title="Tip" style="tip" icon="exclamation-triangle" %}}

To see exactly what the SDK is doing, you can temporarily add the following near the top of
`agent.py`:

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{% notice title="What you just unlocked" style="info" %}}

In one small change you went from a black box to full capture: every prompt, response, tool
call, retrieval, token count, and latency for every turn is now recorded. In the next chapter
you'll put that to work and investigate exactly what the agent did.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

You sent three messages. Roughly how many traces did you create, and what determines that?

{{< details summary="Click here to see the answer" >}}
**Three traces, one per user turn.** A fresh callback is attached per call, and the whole
LangGraph turn runs as a single root run, so each message becomes one trace containing nested
LLM and tool spans. You'll review the traces in more detail in the next section.
{{< /details >}}
