---
title: Introduction
linkTitle: 1. Introduction
weight: 1
time: 5 minutes
---

In [Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/) you instrumented and observed an **agentic AI travel planner**. That application is a **Flask API** wrapping a **LangGraph** workflow, where each node
(coordinator, flight specialist, hotel specialist, activity specialist, and synthesizer) calls an LLM
through **LangChain**'s `ChatOpenAI`.

In this follow-on workshop, you will take that same application and add **Splunk Agent Observability instrumentation** to
it. Rather than re-instrumenting from scratch, you'll attach a single Splunk Agent Observability callback to the LangGraph
workflow so every agent's LLM call is captured. This lets you compare and validate AI trace visibility
across tools using a workload you already understand.

{{% prerequisites title="Prerequisites" %}}

* The workshop 18 travel planner app (`~/workshop/agentic-ai/base-app`), or your own copy of it.
* A Splunk Agent Observability account and API key.
* An OpenAI API key (the same `OPENAI_API_KEY` the app already uses).
* Python 3.10+ environment with package install access.

{{% /prerequisites %}}
