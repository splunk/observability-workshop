# Healthcare Assistant — Workshop Base App

This folder (`base-app/`) is the **starting point** for the agent observability workshop. It is a single-domain healthcare assistant that participants run locally, then instrument with observability tooling during the session.

## Purpose

Provide a working, easy-to-understand agentic application without the complexity of a multi-domain demo platform. The app is intentionally minimal so participants can focus on:

- Deploying and configuring observability products
- Adding traces, spans, and metrics to an existing agent
- Understanding how LLM, tool, and retrieval calls flow through the system

**Observability instrumentation is not included.** Do not add Galileo, OpenTelemetry, or similar integrations unless the workshop exercise explicitly calls for it.

## Tech stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit (`app.py`) |
| Agent runtime | LangGraph (`agent.py`) |
| LLM | OpenAI via LangChain (`ChatOpenAI`) |
| Vector store | PostgreSQL + pgvector via LangChain `PGVector` |
| Relational data | PostgreSQL tables loaded from CSV |
| Config | `config.yaml`, `system_prompt.json`, `.streamlit/secrets.toml` |

## Architecture

```
User (Streamlit)
       │
       ▼
    app.py ──────────────────────────────┐
       │                                  │ sidebar: model selection
       ▼                                  │
 HealthcareAgent (agent.py)               │
       │                                  │
       ├── LangGraph StateGraph           │
       │     chatbot ◄──► tools           │
       │                                  │
       ├── tools/logic.py                 │
       │     ├── get_patient_info         │──► text_to_sql_utils ──► PostgreSQL (healthcare_patient)
       │     ├── delete_patient_record    │──► text_to_sql_utils ──► PostgreSQL (healthcare_patient)
       │     └── search_medicine_qa       │──► rag.py ──► pgvector (healthcare_local_index)
       │                                  │
       └── rag.py (optional RAG tool)     └──► pgvector (healthcare_local_index)
```

### Request flow

1. **Streamlit** collects user input and maintains chat history in session state.
2. **`HealthcareAgent.process_query()`** converts messages to LangChain format and invokes the LangGraph graph.
3. The **chatbot node** calls the LLM with the system prompt and bound tools.
4. If the LLM requests a tool, the **tools node** runs the matching function from `tools/logic.py` (or the RAG retrieval tool from `rag.py`).
5. Tool results return to the chatbot node until the LLM produces a final answer.

## Key files

| File | Role |
|------|------|
| `app.py` | Streamlit entry point; chat UI, example queries, model sidebar |
| `agent.py` | `HealthcareAgent` — builds LangGraph graph, loads tools, runs queries |
| `rag.py` | `HealthcareRAGSystem` — LangChain retrieval chain over pgvector |
| `config.py` | Loads `config.yaml` and `system_prompt.json`; exposes path constants |
| `config.yaml` | Model, RAG, UI, and vectorstore settings |
| `system_prompt.json` | System prompt instructing tool use |
| `setup_env.py` | Reads `.streamlit/secrets.toml` and sets `OPENAI_*`, `POSTGRES_*`, `ENVIRONMENT` |
| `tools/logic.py` | Async tool functions exported as `TOOLS` list |
| `tools/schema.json` | JSON schemas used when registering tools with LangChain |
| `helpers/setup_vectordb.py` | CLI to embed FAQ docs and load patient CSV into PostgreSQL |
| `helpers/pgvector_utils.py` | Connection string, collection naming, PGVector store creation |
| `helpers/sql_utils.py` | CSV → PostgreSQL table load, SQL execution |
| `helpers/text_to_sql_utils.py` | LLM-generated SELECT/DELETE for patient tools |

## Data stores

### pgvector collection

- **Name:** `healthcare_{environment}_index` (e.g. `healthcare_local_index`)
- **Source:** `docs/qa.csv` (medicine FAQ)
- **Setup:** `python helpers/setup_vectordb.py local`

### Relational table

- **Name:** `healthcare_patient`
- **Source:** `docs/relational_patient.csv`
- **Setup:** same `setup_vectordb.py` script (loads relational CSVs after embedding)

## Tools

| Tool | Purpose | Backend |
|------|---------|---------|
| `search_medicine_qa` | Answer medicine questions (dosage, side effects, etc.) | RAG over pgvector |
| `get_patient_info` | Look up patient by ID | Text-to-SQL → `healthcare_patient` |
| `delete_patient_record` | Delete patient by ID | Text-to-SQL → `healthcare_patient` |

Tool descriptions and parameter schemas live in `tools/schema.json`. Implementations live in `tools/logic.py`. The agent registers tools in `HealthcareAgent.load_tools()`.

When RAG is enabled in `config.yaml` (`rag.enabled: true`), `agent.py` also adds a separate `retrieve_healthcare_documents` LangChain tool via `rag.create_rag_tool()`.

## Configuration

- **`config.yaml`** — change default model, RAG `top_k`, UI title, example queries
- **`system_prompt.json`** — change agent behaviour and tool-use instructions
- **`.streamlit/secrets.toml`** — API keys and database credentials (not committed; use `secrets.toml.template`)

Environment variable `ENVIRONMENT` (`local` or `hosted`) selects the pgvector collection suffix.

## Conventions for changes

- Keep the app **healthcare-only**. Do not reintroduce multi-domain abstractions (domain manager, plug-in domains, per-domain routing).
- Prefer **direct imports** over factories or dynamic domain discovery.
- New tools: add the function to `tools/logic.py`, append to `TOOLS`, and add a schema entry in `tools/schema.json`.
- Avoid adding observability SDKs or manual span/logging helpers unless a workshop step requires it.
- Match existing patterns: async tool functions, JSON string returns from tools, config via `load_config()`.

## Running and verifying

```bash
python helpers/setup_vectordb.py local
streamlit run app.py
```

Smoke-test with the example queries in `config.yaml`:

1. Lisinopril question → should invoke RAG
2. Patient P001 lookup → should invoke text-to-SQL

## Related docs

- [README.md](README.md) — participant setup instructions
- [documentation/POSTGRES_SETUP.md](documentation/POSTGRES_SETUP.md) — PostgreSQL/pgvector setup
