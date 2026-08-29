---
title: Attach the Splunk Agent Observability Callback
linkTitle: 2. Attach the Splunk Agent Observability Callback
weight: 2
time: 5 minutes
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
from splunk_ao.deployment import DeploymentMode, resolve_deployment
from splunk_ao.handlers.langchain import SplunkAOAsyncCallback
```

{{< /step >}}

{{< step title="Wrap the graph invocation in a Splunk AO context" >}}

We've updated `~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py`
to open **one** `splunk_ao_context` when the agent is created and keep it open for the
whole Streamlit chat. Each turn attaches a fresh callback that flushes when the LangGraph
chain ends:

```python
    async def _open_splunk_ao_session(self) -> None:
        self._splunk_ao_context_manager = splunk_ao_context(
            project=os.getenv("SPLUNK_AO_PROJECT"),
            agent_stream=os.getenv("SPLUNK_AO_AGENT_STREAM"),
        )
        self._splunk_ao_context_manager.__enter__()

        if resolve_deployment() == DeploymentMode.STANDALONE:
            backend_session_id = splunk_ao_context.start_session(
                external_id=self.session_id,
            )
            splunk_ao_context.set_session(backend_session_id)
        else:
            splunk_ao_context.set_session(self.session_id)

    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        ...
        splunk_ao_logger = splunk_ao_context.get_logger_instance()
        splunk_ao_logger.reset_parent_tracking()

        callback = SplunkAOAsyncCallback(flush_on_chain_end=True)
        run_config = {
            "configurable": {"thread_id": str(uuid.uuid4())},
            "callbacks": [callback],
        }

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            run_config,
        )
        await self._retry_export_if_rejected(splunk_ao_logger)
```

Do **not** wrap each turn in its own `with splunk_ao_context(...)`. Exiting that block
flushes again on every turn. Combined with `flush_on_chain_end=True`, standalone deployments
can reject the first OTLP batch and leave an empty session in the UI until a later turn succeeds.

On standalone, the agent registers the chat once through the Sessions API
(`start_session(external_id=...)`). On O11y Cloud it uses the Streamlit UUID with
`set_session`, matching the [official SDK example](https://github.com/splunk/splunk-ao-python/tree/main/examples/agent/healthcare-assistant).
If the first export is still rejected, `_retry_export_if_rejected` waits briefly and flushes again.

Streamlit in Docker uses **uvloop**, which cannot be patched by `nest_asyncio`. The agent
therefore runs `ainvoke` on a dedicated stdlib asyncio thread so Splunk AO context stays
consistent across turns. Reset parent tracking before each invoke so turns do not share
trace state.

{{< /step >}}

{{< step title="Send only the latest user message from Streamlit" >}}

In `app.py`, we pass only the most recent user turn to the agent. Sending the full chat history
on every invoke makes traces look like one long conversation:

```python
        # Pass only the latest user message to keep each trace a single input/output pair.
        latest_user = [m for m in conversation_messages if m["role"] == "user"][-1:]
        response = st.session_state.agent.process_query(latest_user)
```

The UI still displays the full chat history; only the trace payload is scoped to the current turn.

{{< /step >}}

{{< /exercise >}}

{{% notice title="Why a single callback per request?" style="info" %}}

Creating one `SplunkAOAsyncCallback(flush_on_chain_end=True)` per call to `_process_query_async`
keeps each user turn in its own trace. Because it's attached to the LangGraph run config, every
node's LLM and tool call becomes a nested span under that same trace, giving you the end-to-end
view of a turn instead of a pile of disconnected spans.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

Why does this app use `SplunkAOAsyncCallback` rather than `SplunkAOCallback`?

{{< details summary="Click here to see the answer" >}}
Because the agent streams/invokes the graph **asynchronously** (`self.graph.ainvoke(...)`).
The async callback matches the async run. A synchronous app that called `invoke(...)` would
use `SplunkAOCallback` instead.
{{< /details >}}
