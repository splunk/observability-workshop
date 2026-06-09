---
title: 8. Wrap Up
linkTitle: 8. Wrap Up
weight: 8
time: 5 minutes
---

You created a small AI-agent-shaped application:

* The user request became agent state.
* The agent selected tools from an allowlist.
* Each tool returned an observation.
* The final answer was generated after the agent collected enough context.
* The local LLM controller reused the same tools that the hosted API path can use.

The exercise used a model call for the decision function while keeping the tool registry
and validation boundary in Python. Larger systems can use frameworks such as LangGraph,
LangChain, Semantic Kernel, or another agent runtime, but the same discipline around tool
boundaries, state, safety, and observability still applies.

## Next Steps

Use the **Monitoring Agentic AI Applications** workshop to learn how to instrument agent
frameworks and inspect model calls, tool calls, quality signals, and security risks in
Splunk Observability Cloud.
