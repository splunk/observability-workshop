---
title: Wrap-up
linkTitle: 5. Wrap-up
weight: 5
time: 20 minutes
---

You took the workshop 18 multi-agent travel planner and instrumented it with Galileo (Splunk Agent Observability) by adding just
two things: `galileo_context.init(...)` and a single `GalileoCallback` on the LangGraph run config.
With that, every agent node's LLM call now appears as a nested span in a single Galileo trace per
request — no per-node changes required and very low maintenance.

You now have the same workload traced in **two** observability tools (Splunk Observability Cloud from
workshop 18, and Galileo here), which is a useful basis for comparison.

Next, we're going to expand on this by:

* Adding Galileo metrics (for example, `Context Adherence`) to the captured traces.
* Working through the features that help Galileo support better observability of agents.
* Leveraging powerful features like Signals.
* Using a dedicated `GalileoLogger(project=..., log_stream=...)` to route specific runs to different
  log streams.
* Adding more complexity to our agents.

## References

* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)
