---
title: Attach the Splunk Agent Observability Callback
linkTitle: 2. Attach the Splunk Agent Observability Callback
weight: 2
time: 5 minutes
---

The agent runs its LangGraph workflow asynchronously, so you'll attach Splunk Agent Observability's
**async** callback handler. Because the callback is passed at the graph level, it propagates to every
node automatically, with no per-tool instrumentation required.

Splunk Agent Observability ships traces through its **ingest API**: a lightweight logger buffers the
spans produced during a turn, then flushes them together when the LangGraph chain ends. All of the
turns in a single chat are grouped under one **session**, so the whole conversation stays together in
the console.

{{< exercise title="Add the callback to the agent" >}}

{{< step title="Add the imports" >}}

We've already added the following imports to the
`~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py` file, which are required
to collect traces:

```python
import os
from splunk_ao import SplunkAOLogger
from splunk_ao.handlers.langchain import SplunkAOAsyncCallback
from splunk_ao.schema.trace import TracesIngestRequest
```

{{< /step >}}

{{< step title="Create the loggers and register a session" >}}

We've updated `~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py` so that when the
agent is created, it sets up its logging and registers **one** session for the whole Streamlit chat:

```python
    async def _open_splunk_ao_session(self) -> None:
        project = os.getenv("SPLUNK_AO_PROJECT")
        agent_stream = os.getenv("SPLUNK_AO_AGENT_STREAM")

        # Backend-connected logger: owns the session and sends traces via the ingest API.
        self._ingest_logger = SplunkAOLogger(project=project, agent_stream=agent_stream)
        self._backend_session_id = self._ingest_logger.start_session(
            external_id=self.session_id,
        )

        # Batch-mode logger: the callback buffers spans here, then flushes them
        # through the ingestion hook (below) when each turn ends.
        self._traced_logger = SplunkAOLogger(
            project=project,
            agent_stream=agent_stream,
            mode="batch",
            ingestion_hook=self._ingest_hook,
        )

    def _ingest_hook(self, request: TracesIngestRequest) -> None:
        # Tag every buffered trace with the shared session, then send it to the ingest API.
        request.session_id = uuid.UUID(str(self._backend_session_id))
        request.log_stream_id = uuid.UUID(str(self._ingest_logger.agent_stream_id))
        self._ingest_logger.ingest_traces(request)
```

Two loggers cooperate here. `_ingest_logger` is connected to the backend: it registers the session
with `start_session(external_id=...)` and performs the actual `ingest_traces` call. `_traced_logger`
runs in **batch mode** with an *ingestion hook* — the LangChain callback buffers each turn's spans on
it, and when the turn ends the hook forwards them (retriever documents and all) through `_ingest_logger`.

Because every turn — and the *Log Hallucination* demo — flushes through the same `_ingest_logger` and
the same `_backend_session_id`, they all land in **one session** in the console.

{{% notice title="Why register the session up front?" style="info" %}}

`start_session(external_id=self.session_id)` is idempotent: the first call creates the session, and
any later call with the same external id reuses it. Registering it once when the agent is created
gives every trace in the chat a stable home to group under.

{{% /notice %}}

{{< /step >}}

{{< step title="Attach the callback to each turn" >}}

Each user turn attaches a fresh `SplunkAOAsyncCallback`, pointed at the batch-mode logger, and flushes
when the LangGraph chain ends:

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        ...
        callback = SplunkAOAsyncCallback(
            splunk_ao_logger=self._traced_logger,
            flush_on_chain_end=True,
        )
        run_config = {
            "configurable": {"thread_id": str(uuid.uuid4())},
            "callbacks": [callback],
        }

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            run_config,
        )
```

Streamlit in Docker uses **uvloop**, which cannot be patched by `nest_asyncio`. The agent therefore
runs `ainvoke` on a dedicated stdlib asyncio thread so the loggers stay consistent across turns.

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
