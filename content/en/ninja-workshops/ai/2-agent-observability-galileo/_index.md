---
title: Splunk Agent Observability Instrumentation for LangChain Apps
linkTitle: Splunk Agent Observability Instrumentation for LangChain Apps
weight: 2
layout: chapter
time: 40 minutes
authors: ["Sam Goldfield"]
description: Add Splunk Agent Observability tracing to a LangChain app and inspect traces in the console UI.
aliases:
  - /ninja-workshops/19-agent-observability-galileo/
product: "Observability Cloud"
---

This workshop picks up after workshop 18 and shows the fastest path to instrumenting a LangChain app with Splunk Agent Observability, powered by Galileo.

You will reuse the **multi-agent travel planner** from workshop [Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/). It is a Flask API backed by a LangGraph
workflow whose nodes (coordinator, flight specialist, hotel specialist, activity specialist, and
synthesizer) each call an LLM through LangChain. Instead of sending its telemetry to Splunk
Observability Cloud, you'll trace it with Splunk Agent Observability.

{{< objectives title="Objectives" >}}

* Install the Splunk Agent Observability SDK and set required environment variables.
* Add Splunk Agent Observability context initialization and a single LangChain callback to the travel planner.
* Run a real travel-planning request and verify the full multi-agent trace in the Splunk Agent Observability console.

{{< /objectives >}}

{{% notice style="info" title="Primary references" %}}

* [Splunk Agent Observability Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Splunk Agent Observability LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}

