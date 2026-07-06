---
title: Set Up and Configure
linkTitle: 1. Set Up and Configure
weight: 1
time: 10 minutes
---

{{% notice style="warning" title="TODO" %}}
Verify what fields will already be set through workshop provisioning and which ones will need to be provided to and updated by the attendees.
{{% /notice %}}

Work in the `1-base-app` folder for this chapter. These steps create the Python
environment, configure secrets, start the database, and load the sample data the agent
needs.

{{< exercise title="Set up the base application" >}}

{{< step title="Log into your lab instance" >}}

Connect to your workshop EC2 instance (your instructor will provide the connection details).
The healthcare assistant is pre-loaded under `~/workshop/healthcare-assistant/`, and your
`OPENAI_API_KEY` is already configured in the environment.

{{< /step >}}

{{< step title="Activate the environment" >}}

Change into the base app directory, create a virtual environment, and install dependencies:

```bash
cd ~/workshop/healthcare-assistant/1-base-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Configure secrets" >}}

The app reads its credentials from `.streamlit/secrets.toml`. Copy the template and open it
for editing:

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Your workshop instance is pre-configured with an `OPENAI_API_KEY`, so you can reference it
rather than pasting a key into the file. Set `openai_api_key` and confirm the PostgreSQL and
environment settings:

```toml
openai_api_key = "your_openai_api_key_here"

postgres_host = "localhost"
postgres_port = "5432"
postgres_user = "postgres"
postgres_password = "mypassword"
postgres_db = "vectordb"
environment = "local"
```

{{% notice title="Keep secrets out of source control" style="info" %}}

`.streamlit/secrets.toml` holds API keys and database credentials and is **not** committed
to the repository; only the `.template` file is. Never paste real keys into a committed
file.

{{% /notice %}}

{{< /step >}}

{{< step title="Start PostgreSQL with pgvector" >}}

The agent stores the medicine FAQ embeddings and patient records in PostgreSQL with the
`pgvector` extension. Start a local container:

```bash
docker run -e POSTGRES_USER=postgres \
           -e POSTGRES_PASSWORD=mypassword \
           -e POSTGRES_DB=vectordb \
           --name healthcare-postgres \
           -p 5432:5432 \
           -d pgvector/pgvector:pg16

docker exec -it healthcare-postgres psql -U postgres -d vectordb -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

{{< /step >}}

{{< step title="Load vector data and relational tables" >}}

Embed the medicine FAQ into pgvector and load the patient registry into PostgreSQL. The
helper script does both:

```bash
./start_vectordb.sh
```

This runs `python helpers/setup_vectordb.py local`, which creates the
`healthcare_local_index` pgvector collection from `docs/qa.csv` and the
`healthcare_patient` table from `docs/relational_patient.csv`.

{{< /step >}}

{{< /exercise >}}
