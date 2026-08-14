---
title: Cause 2 — Over-Engineered Workflows
linkTitle: 5. Simplify the Workflow
weight: 5
time: 15 minutes
---

A correctly selected model can still be wrapped in an inefficient workflow. Open the prepared
**E-Commerce Customer Session** to see the work behind several customer-facing answers.

The message view shows product discovery, shopping advice, exchanges, loyalty points, and returns
within one session. The span tree shows how the agent handles those turns.

### 1. Follow one request through the workflow

Expand a **Customer Q&A Question** trace and identify the main stages:

1. **Classify Turn** determines the user's intent.
2. **Model Router** selects a model for the task.
3. **Knowledge Base Retrieval** finds relevant product or policy context.
4. The selected model generates the final answer.

A user sees one response, but the system may perform several model and retrieval operations. Each
step has to justify the tokens and latency it adds.

### 2. Inspect the trace shape

Compare several turns in the same session. The prepared view shows individual turns taking roughly
2.49 to 4.9 seconds. Expand the slower turns and ask:

* Did the workflow add a model or retrieval call?
* Did a step repeat or retry?
* Did the selected route match the user's intent?
* Did retrieval return more context than the answer required?

Extra spans are not automatically waste. A retrieval step may be essential for a grounded answer.
The goal is to find work that does not improve the outcome.

### 3. Locate token growth

Select each LLM span and compare its input and output tokens. Then inspect the span immediately
before it. Common sources of growth include:

* Too many retrieved chunks or chunks that are incorrectly sized.
* Full conversation history sent when only recent context matters.
* Verbose tool definitions or results repeated on every call.
* A router sending a simple request through an unnecessarily complex path.
* Retries that repeat the same action without changing the inputs.

### 4. Check the session evaluators

Return to the session and review **Action Completion** and **Agent Efficiency**. In the prepared
example, Action Completion is `true` while Agent Efficiency is `false`.

This distinction matters: an agent can eventually complete the user's task while taking an
inefficient route. Open the Agent Efficiency result to read its rationale and identify the turn or
behavior that should be investigated.

> Successful is not the same as efficient. Agent-level evaluation helps find waste that a simple
> error-rate chart will miss.

Which change would you test first, and what regression could it introduce?

* Fewer retrieval chunks may omit necessary evidence.
* Shorter history may lose conversational intent.
* A simpler route may send a difficult request to an unsuitable model.
* Tighter retry limits may reduce recovery from transient failures.

{{< checkpoint title="Knowledge Check" >}}

Why can Action Completion be true while Agent Efficiency is false?

{{< details summary="Click here to see the answer" >}}
The agent can reach the requested outcome while using unnecessary steps, context, retries, or an
expensive route. Action Completion measures whether the work was completed; Agent Efficiency asks
whether the path taken was effective and economical.
{{< /details >}}

We have now attributed spend to a model and to a workflow. Next, we will connect those individual
requests to trends and outcomes across the application.
