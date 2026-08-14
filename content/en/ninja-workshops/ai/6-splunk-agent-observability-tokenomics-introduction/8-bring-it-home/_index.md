---
title: Bring It Home
linkTitle: 8. Bring It Home
weight: 8
time: 5 minutes
description: Close the tokenomics tour with a repeatable optimization cycle.
---

We began with a bill that told us how much was spent but not whether those tokens created value.
We ended with a traceable decision: which configuration met the outcome bar, where its tokens went,
and why it was the best trade-off for the workload.

## The three causes

1. **Wrong model:** choose models per task using quality, latency, and cost together.
2. **Over-engineered workflow:** use spans and Agent Efficiency to find oversized context,
   unnecessary calls, poor routes, loops, and retries.
3. **Spend without outcomes:** place token and cost trends beside quality, Action Completion, and
   business results.

## The optimization cycle

1. **Instrument** the complete agent workflow.
2. **Locate** consumption at trace and span level.
3. **Explain** the model or behavior that caused it.
4. **Evaluate** whether it improved the outcome.
5. **Compare** alternatives on a fixed dataset.
6. **Release** only configurations that meet predefined thresholds.
7. **Monitor and feed back** production evidence into the next experiment.

{{< checkpoint title="Final Reflection" >}}

Which of the three causes will you investigate first in your own agent workflow, and what evidence
will you need before changing it?

{{< details summary="Some questions to consider" >}}
Do you need per-model token and cost trends, a trace showing context growth, an evaluator such as
Agent Efficiency or Action Completion, a business outcome, or a controlled experiment comparing
candidate configurations?
{{< /details >}}

> Do not optimize tokens in isolation. Optimize the useful, safe outcomes you receive from them.
> Splunk Agent Observability gives you the evidence to make that trade-off visible and repeatable.

## References

* [Galileo documentation](https://docs.galileo.ai/)
* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)
* [Full Splunk Agent Observability workshop](../../4-splunk-agent-observability/)

{{< checkpoint title="Tour complete" >}}
