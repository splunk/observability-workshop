---
title: Key Concepts
linkTitle: 2. Key Concepts
weight: 2
time: 4 minutes
---

Splunk Agent Observability is built around a small vocabulary. You'll use each of these
concepts in the chapters that follow, so it's worth getting them straight first. They also
map directly to this workshop's agenda.

## Traces, spans, and sessions

{{% notice title="The shape of agent telemetry" style="green" icon="running" %}}

* A **trace** is one end-to-end request through your agent, for example a single user turn
  in the chat.
* A **span** is a single step inside a trace: an LLM call, a tool call, or a retrieval. Spans
  nest, so a trace shows the full tree of what the agent did and in what order.
* A **session** groups related traces, for example all the turns in one conversation.

{{% /notice %}}

Traces are organized by **project** and **log stream**. A project is a container for a use
case (`healthcare-assistant`); a log stream is a named destination within it (`local`, or one
per workshop instance). This is where you'll view traces and enable live metrics.

## Metrics: evaluating quality at scale

**Metrics** (evaluations) score your traces and spans, for example *Context Adherence*
(is the answer grounded?), *Correctness*, *Tool Selection Quality*, and *Prompt Injection*.
They turn qualitative quality questions into numbers you can monitor and alert on.

But evaluating every trace is hard to do affordably:

{{% notice title="Why evaluating at scale is hard, and how Luna solves it" style="info" %}}

Using a large general-purpose LLM as a judge works at hundreds of traces per day, but it
breaks down at millions: every evaluation is another expensive, slow LLM call, so teams
sample 5–10% of traffic and leave most production traces unscored.

Splunk Agent Observability uses **Luna**, a family of purpose-built Small Language Models
(SLMs) fine-tuned specifically for evaluation. The result is dramatically cheaper and faster
scoring, accurate enough to run on *all* of your traffic, and fast enough to power
**real-time guardrails** without hurting the user experience.

{{% /notice %}}

## Signals: surfacing the unknown unknowns

Metrics tell you about problems you thought to measure. **Signals** automatically surface
recurring failure patterns from production traces (planning loops, tool errors,
hallucinations, routing failures, and more) and explain *what* went wrong, *why*, and *what
to do next*. They turn weeks of post-incident analysis into minutes of targeted remediation.

## Guardrails: acting at runtime

Observing and measuring is not enough when an answer could harm a patient. **Guardrails**
(agent controls) evaluate each step at runtime and take action: **block** an unsafe step
outright, or **steer** the agent toward a safe response. Because policies are centralized,
you can change them in seconds without taking agents offline.

{{< checkpoint title="Knowledge Check" >}}

A single chat message triggers an LLM call followed by a patient-lookup tool call. How many
**traces** and how many **spans** does that produce?

{{< details summary="Click here to see the answer" >}}
**One trace, multiple spans.** The user turn is a single end-to-end request, so it's one
trace. Inside it you'll see nested spans: at minimum an LLM span and a tool span for the
lookup (and another LLM span when the model summarizes the tool result).
{{< /details >}}
