---
title: The Challenge
linkTitle: 1. The Challenge
weight: 1
time: 5 minutes
---

## When an agent gets it wrong

Imagine a patient posts this the day after your assistant goes live:

> *"I tried the new AI assistant to ask about my medication, and it told me to take
> **double** the dose listed on my prescription. That's not a small mistake. That's
> dangerous. If I hadn't double-checked with my doctor, I could have actually followed that
> advice."*

The infrastructure was healthy. The API returned `200 OK`. Latency was fine. Every
traditional signal said the system was working, and yet the agent produced an answer that
could harm someone. **That's the agentic AI trust gap**, and it's invisible to
infrastructure and APM monitoring alone.

Agentic systems introduce a new class of risk:

* **Unpredictable reasoning**: the agent chooses a path you didn't anticipate.
* **Hallucinations**: confident answers that aren't grounded in your data.
* **Tool-selection errors**: the agent calls the wrong tool, or the right tool with the
  wrong arguments.
* **Cost spikes**: runaway loops and oversized prompts quietly burning tokens.
* **Sensitive-data exposure**: the agent reveals or acts on data it shouldn't.

## What Splunk Agent Observability gives you

Splunk Agent Observability, powered by Galileo, is built to close that gap across the
entire agent lifecycle, from development through production.

{{% notice title="Three things you get" style="info" %}}

* **Accurate evaluations**: evaluate agent, output, and RAG quality with high-accuracy evals
  plus out-of-the-box and custom metrics, so "is this answer good?" becomes a number you can
  track.
* **Instant visibility**: see the root cause of errors across complex, multi-step agent
  workflows, instead of guessing from logs.
* **Runtime guardrails**: block or steer hallucinations, prompt injections, and safety
  violations before they ever reach an end user.

{{% /notice %}}

Over the rest of this workshop you'll apply all three to the Careful Health Provider
assistant, turning that frightening social post into a problem you can detect, measure,
prevent, and govern.

{{< checkpoint title="Knowledge Check" >}}

The assistant told a patient to take double their dose, but every infrastructure and APM
signal was green. Why didn't traditional monitoring catch it?

{{< details summary="Click here to see the answer" >}}
Because the failure was in the **quality and safety of the agent's reasoning and output**,
not in the health of the system. The request succeeded, was fast, and returned a valid
response. It was just *wrong*. Catching that requires observability that understands agent
behavior: traces of what the agent did, plus evaluations of how good and how safe the result
was.
{{< /details >}}
