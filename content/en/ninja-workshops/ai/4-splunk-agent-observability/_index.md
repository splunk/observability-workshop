---
title: Splunk Agent Observability
linkTitle: Splunk Agent Observability
weight: 4
layout: chapter
time: 2 hours
authors: ["Derek Mitchell", "Sam Goldfield", "Tim Hard"]
description: See inside your agentic AI applications. Instrument them, trace and evaluate agent behavior, surface emerging issues, and apply runtime guardrails with Splunk Agent Observability (powered by Galileo).
draft: false
hidden: true
aliases:
  - /ninja-workshops/20-splunk-agent-observability/
product: "Observability Cloud"
---

Agentic AI applications think, plan, and act on their own. That autonomy is exactly what
makes them powerful, and exactly what makes them hard to trust. When an agent reasons its
way to the wrong answer, calls the wrong tool, hallucinates, or leaks sensitive data, *where
do you even look?*

**Splunk Agent Observability**, powered by Galileo, closes that gap. It gives you
observability across the entire agent lifecycle, from development through production, so you
can see what your agents actually did, measure how well they did it, catch failures before
your users do, and enforce safe behavior at runtime.

> [!splunk] **The scenario.** 
> **Careful Health Provider** is launching an agentic AI
> healthcare assistant that answers patient questions about medications and looks up patient
> records. They already have strong observability for infrastructure and application
> performance, but agentic systems introduce a new class of risk: unpredictable reasoning,
> hallucinations, cost spikes, and exposure of sensitive data. One bad answer, telling a
> patient to take *double* their prescribed dose, is all it takes to make headlines. In this
> workshop, *you* help Careful Health Provider get ahead of that risk.

In this hands-on workshop you'll take a working healthcare assistant, built with
**Streamlit**, **LangGraph**, and **PostgreSQL/pgvector**, and progressively make it
observable, measurable, and safe.

{{< objectives title="What you will learn" >}}

* **Instrument** the application to capture traces and see exactly what happened during each
  agent request.
* **Trace and investigate** agent behavior to pinpoint the root cause of errors in complex,
  multi-step workflows.
* **Enable out-of-the-box quality metrics** to evaluate agent interactions and quickly
  surface anomalies such as hallucinations and tool-selection errors.
* **Surface emerging issues with Signals** that automatically detect agent failure patterns
  that are hard to catch through evals or manual investigation.
* **Apply guardrails at runtime** that detect and act on policy violations, sensitive-data
  exposure, and unsafe prompts or responses, blocking *or* steering them.

{{< /objectives >}}

{{% notice title="Splunk Agent Observability, powered by Galileo" style="info" %}}

Splunk Agent Observability brings observability to the agent lifecycle, from development
through production:

* **Accurate evaluations**: evaluate agent, output, and RAG quality with high-accuracy evals
  and both out-of-the-box and custom metrics.
* **Instant visibility**: see the root cause of errors across complex, multi-step agent
  workflows.
* **Runtime guardrails**: block hallucinations, prompt injections, and safety violations
  before they reach your users.

{{% /notice %}}

{{% notice style="info" title="Primary references" %}}

* [Galileo documentation](https://docs.galileo.ai/)
* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}
