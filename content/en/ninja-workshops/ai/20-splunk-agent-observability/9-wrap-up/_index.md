---
title: Wrap-up
linkTitle: 9. Wrap-up
weight: 9
archetype: chapter
time: 5 minutes
description: Congratulations, you have completed the Splunk Agent Observability workshop.
---

Congratulations, you've completed the **Splunk Agent Observability** workshop!

You took Careful Health Provider's agentic healthcare assistant from a black box that could
quietly tell a patient to take double their dose, and turned it into a system you can see,
measure, and govern.

## What you accomplished

* **Instrumented** the application to trace every agent interaction.
* **Traced and investigated** agent behavior to find the root cause of errors fast.
* **Enabled quality metrics** to automatically catch hallucinations and tool-selection errors.
* **Used Signals** to surface the unknown unknowns, the recurring failure patterns you didn't
  think to measure.
* **Ran experiments** to replace guesswork with evidence and prevent regressions before
  release.
* **Added guardrails** to block dangerous actions and steer unsafe answers to safety at
  runtime.

## Why Splunk Agent Observability

Splunk Agent Observability closes the AI trust gap that traditional infrastructure and APM
monitoring can't see:

* **Accurate, low-cost evaluations**: purpose-built Luna SLMs detect hallucinations, bias,
  and more, affordably enough to score *all* your traffic.
* **End-to-end visibility for the entire AI stack**: observe agents, models, vector
  databases, proxies, and more in one place.
* **Built-in runtime security and privacy guardrails**: block inaccurate and harmful behavior
  before it ever reaches a customer.

And because it's part of Splunk Observability, your agent telemetry lives right alongside your
infrastructure, APM, and log data: one platform for the whole stack.

## Where to go next

* Add custom metrics and **Signals** tuned to your own failure modes.
* Wire experiments into CI/CD as an automated release gate.
* Expand guardrails across more steps: prompt injection, PII exposure, scope enforcement.
* Route different workloads to dedicated log streams for cleaner separation.

## References

* [Galileo documentation](https://docs.galileo.ai/)
* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

<!-- TODO screenshot: celebratory image (trophy, fireworks, etc.) sized for the wrap-up page -->
![Congratulations on completing the workshop](../images/congratulations.png?width=20vw)

{{< checkpoint title="Workshop complete -- **nice work!**" >}}
