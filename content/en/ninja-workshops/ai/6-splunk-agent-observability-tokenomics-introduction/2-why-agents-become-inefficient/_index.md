---
title: Why Agents Become Token-Inefficient
linkTitle: 2. Three Causes
weight: 2
time: 10 minutes
---

### Cause 1: the wrong model

A capable, expensive model may be used for every step, including routing, extraction, or
classification that a smaller model could handle. The inverse also creates waste: a model that
is too weak may retry, call unnecessary tools, or require larger prompts to complete the task.

The optimization question is not "Which model is cheapest?" It is which model delivers the required quality and latency for this specific step at the lowest sustainable cost?

### Cause 2: over-engineered or verbose tools and workflows

Token waste can hide in:

* Tool descriptions repeated with every model call.
* Retrieval that returns too many, too few, or incorrectly sized chunks.
* Full conversation history sent when only recent context matters.
* Planner and tool loops that do not converge.
* Retries that repeat the same failing action.
* Verbose tool responses passed back into the model unchanged.

Design of your agent is very important.

### Cause 3: spend without outcomes

Bills will tell you how much the tokens cost, but not:

* Which agentic use case consumed it?
* Which value proposition it was supporting?
* Did the response meet the required quality and safety bar?
* Did an inexpensive configuration outperform an expensive one?

Without that context, teams optimize totals instead of value.

We're going to review how Splunk Agent Observability handles visibility and evaluation of these common failure modes,
and how the platform can help you make effective decisions and take action quickly to better use your tokens.
