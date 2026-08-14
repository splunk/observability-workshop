---
title: Gaining Visibility
linkTitle: 3. Gain Visibility
weight: 3
time: 10 minutes
---
## Architecture

Our assistant uses Streamlit, LangGraph, an OpenAI model, PostgreSQL with pgvector, and three tools.
One medication question can invoke an LLM, retrieval, a tool, and another LLM call. It is instrumented
into Splunk Agent Observability with a callback.

Requests into our assistant show up as sessions, traces, and spans.

* A **session** is a multi-turn conversation
* A **trace** is one end-to-end agent request, starting from an input and ending with its output. One turn of the conversation.
* A **span** is one step of the trace such as an LLM call, retrieval, or tool call.

Open the prepared Lisinopril trace:

1. Start with total input tokens, output tokens, latency, and cost.
2. Expand the span tree to show the path the agent chose.
3. Select an LLM span and point out model, prompt, response, and token counts.
4. Select the retrieval or tool span and show how its output becomes context for the next call.
5. Return to the root span and connect the detailed steps to the total.