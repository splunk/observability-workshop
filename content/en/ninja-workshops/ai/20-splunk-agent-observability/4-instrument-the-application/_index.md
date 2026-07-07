---
title: Instrument the Application
linkTitle: 4. Instrument the Application
weight: 4
time: 15 minutes
---

You can't observe what you don't capture. In this chapter you'll add **Splunk Agent
Observability (Galileo)** tracing to the assistant so that every user turn becomes a trace,
with a nested span for each LLM and tool call, and you'll do it without rewriting the agent.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you want end-to-end visibility into the agent's
decisions with minimal code change and minimal maintenance. Rather than hand-instrument every
step, you'll attach a single LangChain callback at the graph level and let Splunk Agent
Observability capture the whole tree automatically.

{{% /notice %}}

> [!splunk] Instrumentation is remarkably lightweight: a Galileo callback is a standard
> LangChain callback handler. Attach it to a LangGraph run and it captures prompts,
> responses, model names, token usage, timing, and span nesting for you.

{{% notice title="Where to work" style="info" %}}

This chapter works in the `~/workshop/healthcare-assistant/2-app-with-instrumentation` folder.

{{% /notice %}}

Continue to the subsections to add the SDK, attach the callback, and generate traffic.
