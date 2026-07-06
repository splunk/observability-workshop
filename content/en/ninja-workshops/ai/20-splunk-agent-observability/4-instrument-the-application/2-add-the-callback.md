---
title: Attach the Galileo Callback
linkTitle: 2. Attach the Galileo Callback
weight: 2
time: 5 minutes
---

The agent runs its LangGraph workflow asynchronously, so you'll attach Galileo's
**async** callback. Because the callback is passed at the graph level, it propagates to every
node automatically, with no per-tool instrumentation required.

{{< exercise title="Add the callback to the agent" >}}

{{< step title="Add the imports" >}}

Open `agent.py`. At the end of the import section, just before `class State(TypedDict)`,
add:

```python
import os
from galileo import galileo_context
from galileo.handlers.langchain import GalileoAsyncCallback
```

{{< /step >}}

{{< step title="Wrap the graph invocation in a Galileo context" >}}

The base version of `_process_query_async` invokes the graph with no tracing:

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

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            self.langgraph_config,
        )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

Update it to open a `galileo_context`, start a session keyed to the agent's `session_id`,
and attach a fresh `GalileoAsyncCallback` to the run config:

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

        with galileo_context(
            project=os.getenv("GALILEO_PROJECT"),
            log_stream=os.getenv("GALILEO_LOG_STREAM"),
        ):
            galileo_context.start_session(external_id=self.session_id)

            # One callback per request keeps each user turn in its own trace.
            callback = GalileoAsyncCallback()
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

Creating one `GalileoAsyncCallback` per call to `_process_query_async` keeps each user turn
in its own trace. Because it's attached to the LangGraph run config, every node's LLM and
tool call becomes a nested span under that same trace, giving you the end-to-end view of a
turn instead of a pile of disconnected spans.

{{% /notice %}}

{{% notice title="Troubleshooting" style="tip" icon="exclamation-triangle" %}}

If traces aren't appearing and you want to see what the SDK is doing, temporarily add the
following to `agent.py`:

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

Why does this app use `GalileoAsyncCallback` rather than `GalileoCallback`?

{{< details summary="Click here to see the answer" >}}
Because the agent streams/invokes the graph **asynchronously** (`self.graph.ainvoke(...)`).
The async callback matches the async run. A synchronous app that called `invoke(...)` would
use `GalileoCallback` instead.
{{< /details >}}
