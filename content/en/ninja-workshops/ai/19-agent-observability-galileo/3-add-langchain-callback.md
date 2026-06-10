---
title: Add the LangChain Callback
linkTitle: 3. Add the LangChain Callback
weight: 3
time: 5 minutes
---

Galileo's `GalileoCallback` is a standard LangChain callback handler. When you attach it to a
LangChain or LangGraph run, it automatically captures prompts, responses, model names, token usage,
timing, and the nesting of each step.

Because the travel planner is a **LangGraph** workflow, you don't need to edit every node. Instead,
pass a single callback in the **run config** when the compiled graph is streamed. Galileo then records
one trace per request, with a nested LLM span for each agent node (coordinator, flight, hotel,
activity, and synthesizer).

{{< exercise title="Add the LangChain callback" >}}

{{< step title="Import the callback"  >}}

Add the callback import alongside the other LangChain imports in `main.py`:

```python
from galileo.handlers.langchain import GalileoCallback
```

{{< /step >}}

{{< step title="Attach the callback to the graph run config"  >}}
In `plan_travel_internal()`, create a callback and attach it to the run config passed to `compiled_app.stream(...)`. The existing code should look something like this:

```python
    workflow = build_workflow()
    compiled_app = workflow.compile()

    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

Update it to build a config that includes the Galileo callback (merging it with any existing config the app already passes). This passes the execution of each node in the agent to Galileo:

```python
    workflow = build_workflow()
    compiled_app = workflow.compile()

    # One callback per request keeps each travel plan in its own trace.
    callback = GalileoCallback()
    run_config = {**config, "callbacks": [callback]}

    for step in compiled_app.stream(initial_state, run_config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

Passing the callback at the graph level means it propagates to every node's `llm.invoke(...)` call automatically. No further instrumentation is needed.

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

Where do you attach the `GalileoCallback` in a LangGraph workflow?

{{% notice title="Async workflows" style="blue" icon="info-circle" %}}
If your app streams the graph asynchronously (`compiled_app.astream(...)`), use
`GalileoAsyncCallback` instead of `GalileoCallback`. The travel planner runs synchronously, so
`GalileoCallback` is correct here.
{{% /notice %}}
