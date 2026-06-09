---
title: Galileo Instrumentation for LangChain Apps
linkTitle: Galileo Instrumentation for LangChain Apps
weight: 19
layout: chapter
time: 40 minutes
authors: ["Sam Goldfield"]
description: Add Galileo (Splunk Agent Observability) tracing to a LangChain app and inspect traces in the console UI.
draft: false
hidden: false
aliases:
  - /ninja-workshops/19-agent-observability-galileo/
product: "Observability Cloud"
---

This workshop picks up after workshop 18 and shows the fastest path to instrumenting a LangChain app with Galileo.

You will reuse the **multi-agent travel planner** from workshop 18. It is a Flask API backed by a LangGraph
workflow whose nodes (coordinator, flight specialist, hotel specialist, activity specialist, and
synthesizer) each call an LLM through LangChain. Instead of sending its telemetry to Splunk
Observability Cloud, you'll trace it with Galileo (Splunk Agent Observability).

You will:

* Install the Galileo SDK and set required environment variables.
* Add Galileo context initialization and a single LangChain callback to the travel planner.
* Run a real travel-planning request and verify the full multi-agent trace in the Galileo console.

Primary references:

* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)
