---
title: 7. Wrap Up
linkTitle: 7. Wrap Up
weight: 7
time: 5 minutes
---

You created a small AI-agent-shaped application:

* The user request became agent state.
* The agent selected tools from an allowlist.
* Each tool returned an observation.
* The final answer was generated after the agent collected enough context.

The exercise used deterministic Python to keep the mechanics visible. To move this into
a real AI agent, replace `decide_next_action` with an LLM or framework such as LangGraph,
LangChain, Semantic Kernel, or another agent runtime. Keep the same discipline around
tool boundaries, state, safety, and observability.

## Next Steps

Use the **Monitoring Agentic AI Applications** workshop to learn how to instrument agent
frameworks and inspect model calls, tool calls, quality signals, and security risks in
Splunk Observability Cloud.
