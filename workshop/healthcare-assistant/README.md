# Healthcare Assistant — Workshop Base App

Starting point for the agent observability workshop. This is a healthcare-only assistant built with **Streamlit**, **LangGraph**, and **PostgreSQL/pgvector**.

The app runs end-to-end chat with RAG and text-to-SQL tools, but **does not include observability instrumentation**. Workshop participants add tracing, metrics, and related product integration during the session.

## Prerequisites

- Python 3.8+
- OpenAI API key
- PostgreSQL with pgvector (local Docker container or hosted instance)

## Setup

Run these steps from the `base-app` directory.

1. **Start PostgreSQL with pgvector (Docker)**

   ```bash
   docker pull pgvector/pgvector:pg16

   docker run -e POSTGRES_USER=postgres \
              -e POSTGRES_PASSWORD=mypassword \
              -e POSTGRES_DB=vectordb \
              --name healthcare-postgres \
              -p 5432:5432 \
              -d pgvector/pgvector:pg16

   docker exec -it healthcare-postgres psql -U postgres -d vectordb -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```

   See [documentation/POSTGRES_SETUP.md](documentation/POSTGRES_SETUP.md) for more detail.

2. **Create a virtual environment and install dependencies**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure secrets**

   Copy the template and add your keys:

   ```bash
   cp .streamlit/secrets.toml.template .streamlit/secrets.toml
   ```

   Edit `.streamlit/secrets.toml`:

   ```toml
   openai_api_key = "your_openai_api_key_here"

   postgres_host = "localhost"
   postgres_port = "5432"
   postgres_user = "postgres"
   postgres_password = "mypassword"
   postgres_db = "vectordb"
   environment = "local"
   ```

4. **Load vector data and relational tables**

   ```bash
   python helpers/setup_vectordb.py local
   ```

   Or use the helper script:

   ```bash
   ./start_vectordb.sh
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

   Open `http://localhost:8501`.

## Model selection

Use the **Model** dropdown in the sidebar to switch LLMs. Available models are defined in `config.yaml`.

## Example queries

- "What is the dosage and common side effects of Lisinopril?" — RAG over the medicine FAQ (`search_medicine_qa`)
- "Can you look up information for patient P001?" — text-to-SQL patient lookup (`get_patient_info`)

## Project layout

```
base-app/
├── app.py                 # Streamlit UI and chat loop
├── agent.py               # LangGraph agent (HealthcareAgent)
├── rag.py                 # RAG retrieval chain (pgvector)
├── config.py              # Config loader
├── config.yaml            # App settings (model, RAG, UI)
├── system_prompt.json     # Agent system prompt
├── setup_env.py           # Loads .streamlit/secrets.toml into env vars
├── tools/
│   ├── logic.py           # Tool implementations
│   └── schema.json        # Tool JSON schemas for LangChain
├── docs/
│   ├── qa.csv             # Medicine FAQ source data (embedded into pgvector)
│   └── relational_patient.csv  # Patient registry (loaded into PostgreSQL)
├── helpers/
│   ├── setup_vectordb.py  # One-time DB setup script
│   ├── pgvector_utils.py  # pgvector collection helpers
│   ├── sql_utils.py       # Relational table load and SQL execution
│   └── text_to_sql_utils.py  # LLM-generated SQL for patient tools
└── documentation/
    └── POSTGRES_SETUP.md  # Database setup guide
```

For architecture details and guidance when modifying the codebase, see [AGENTS.md](AGENTS.md).
