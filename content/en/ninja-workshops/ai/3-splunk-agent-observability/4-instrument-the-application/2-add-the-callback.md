---
title: Attach the Splunk Agent Observability Callback
linkTitle: 2. Attach the Splunk Agent Observability Callback
weight: 2
time: 3 minutes
---

The agent runs its LangGraph workflow asynchronously, so you'll attach Splunk Agent Observability's
**async** callback handler. Because the callback is passed at the graph level, it propagates to every
node automatically, with no per-tool instrumentation required.

{{< exercise title="Add the callback to the agent" >}}

{{< step title="Add the imports" >}}

We've already added the following imports to the
`~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py` file, which are required
to collect traces:

```python
import os
from splunk_ao import splunk_ao_context
from splunk_ao.handlers.langchain import SplunkAOAsyncCallback
```

{{< /step >}}

{{< step title="Wrap the graph invocation in a Splunk AO context" >}}

We've updated the `~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py` file
to update the `_process_query_async` function to open a `splunk_ao_context`, start a session keyed to the agent's `session_id`,
and attach a fresh `SplunkAOAsyncCallback` to the run config:

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        with splunk_ao_context(
            project=os.getenv("SPLUNK_AO_PROJECT"),
            agent_stream=os.getenv("SPLUNK_AO_AGENT_STREAM"),
        ):
            splunk_ao_context.start_session(external_id=self.session_id)

            # One callback per request keeps each user turn in its own trace.
            callback = SplunkAOAsyncCallback()
            run_config = {**self.langgraph_config, "callbacks": [callback]}

            result = await self.graph.ainvoke(
                {"messages": langchain_messages},
                run_config,
            )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

{{< /step >}}

{{< /exercise >}}

{{% notice title="Why a single callback per request?" style="info" %}}

Creating one `SplunkAOAsyncCallback` per call to `_process_query_async` keeps each user turn
in its own trace. Because it's attached to the LangGraph run config, every node's LLM and
tool call becomes a nested span under that same trace, giving you the end-to-end view of a
turn instead of a pile of disconnected spans.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

Why does this app use `SplunkAOAsyncCallback` rather than `SplunkAOCallback`?

{{< details summary="Click here to see the answer" >}}
Because the agent streams/invokes the graph **asynchronously** (`self.graph.ainvoke(...)`).
The async callback matches the async run. A synchronous app that called `invoke(...)` would
use `SplunkAOCallback` instead.
{{< /details >}}
