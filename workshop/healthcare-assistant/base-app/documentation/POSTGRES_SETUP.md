# PostgreSQL with pgvector Setup Guide

This guide explains how to set up PostgreSQL with the pgvector extension for the healthcare assistant workshop app.

## Overview

The app uses **PostgreSQL with pgvector** for vector storage via LangChain's `PGVector` integration. The healthcare collection is named `healthcare_{environment}_index` (e.g. `healthcare_local_index`).

## Step 1: Run PostgreSQL with pgvector in Docker

```bash
docker pull pgvector/pgvector:pg16

docker run -e POSTGRES_USER=postgres \
           -e POSTGRES_PASSWORD=mypassword \
           -e POSTGRES_DB=vectordb \
           --name healthcare-postgres \
           -p 5432:5432 \
           -d pgvector/pgvector:pg16
```

## Step 2: Enable the pgvector Extension

```bash
docker exec -it healthcare-postgres psql -U postgres -d vectordb
```

Then run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Verify installation:

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

## Step 3: Configure Secrets

Add your PostgreSQL credentials to `.streamlit/secrets.toml`:

```toml
postgres_host = "localhost"
postgres_port = "5432"
postgres_user = "postgres"
postgres_password = "mypassword"
postgres_db = "vectordb"

environment = "local"
```

## Step 4: Load Documents

From the `simplified-app` directory:

```bash
python helpers/setup_vectordb.py local
```

This creates the `healthcare_local_index` pgvector collection from `docs/qa.csv` and loads patient records from `docs/relational_patient.csv` into the `healthcare_patient` table.

## Troubleshooting

- **Collection not found at runtime** — Re-run `python helpers/setup_vectordb.py local`.
- **Connection refused** — Confirm the Docker container is running and port 5432 is exposed.
- **Authentication failed** — Check `postgres_password` in `.streamlit/secrets.toml` matches your container.
