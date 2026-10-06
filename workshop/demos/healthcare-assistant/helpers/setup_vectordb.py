"""
Healthcare vector database setup using PostgreSQL/pgvector.

Usage:
    python helpers/setup_vectordb.py local
    python helpers/setup_vectordb.py hosted
"""
import argparse
import getpass
import os
import sys
import uuid
from pathlib import Path
from typing import List

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import DOCS_DIR, DOMAIN, load_config
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from setup_env import setup_environment
from helpers.pgvector_utils import create_pgvector_store, get_collection_name
from helpers.sql_utils import load_domain_relational_csvs


def setup_vectordb(environment: str) -> bool:
    """Set up vector database and relational tables for the healthcare app."""
    print(f"Setting up vector database for healthcare in {environment} environment")

    setup_environment()
    os.environ["ENVIRONMENT"] = environment

    app_config = load_config()
    rag_config = app_config.get("rag", {})
    vectorstore_config = app_config.get("vectorstore", {})

    chunk_size = rag_config.get("chunk_size", 1000)
    chunk_overlap = rag_config.get("chunk_overlap", 200)
    embedding_model = vectorstore_config.get("embedding_model", "text-embedding-3-large")

    print(f"Using chunk_size: {chunk_size}, chunk_overlap: {chunk_overlap}")
    print(f"Using embedding model: {embedding_model}")

    docs_dir = DOCS_DIR
    if not docs_dir.exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return False

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    if not os.environ.get("POSTGRES_PASSWORD"):
        os.environ["POSTGRES_PASSWORD"] = getpass.getpass("Enter PostgreSQL password: ")

    embeddings = OpenAIEmbeddings(model=embedding_model)
    collection_name = get_collection_name(DOMAIN, environment)
    print(f"Creating PostgreSQL/pgvector collection: {collection_name}")
    vector_store, collection_name = create_pgvector_store(
        embeddings,
        DOMAIN,
        environment,
        pre_delete_collection=True,
    )

    csv_path = docs_dir / "qa.csv"
    df = pd.read_csv(csv_path)
    doc_list: List[Document] = []
    uuid_list = []
    for _, row in df.iterrows():
        question = str(row.get("question", "") or "").strip()
        answer = str(row.get("answer", "") or "")
        body = (
            f"[FAQ] Healthcare FAQ. "
            f"Medication: {question}. "
            f"Information: {answer}. "
        )
        meta = {
            "doc_family": "healthcare",
            "question": question,
            "answer": answer,
        }
        doc_list.append(Document(page_content=body, metadata=meta))
        uuid_list.append(uuid.uuid4())

    print("Adding documents to vector store...")
    vector_store.add_documents(documents=doc_list, ids=uuid_list)
    embedded_count = len(doc_list)

    print("Loading relational tables for healthcare...")
    load_domain_relational_csvs(docs_dir, DOMAIN)

    print("✅ Successfully created vector database for healthcare")
    print(f"📊 Total documents embedded: {embedded_count}")
    print(f"🔗 PostgreSQL collection: {collection_name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Set up PostgreSQL/pgvector for the healthcare assistant"
    )
    parser.add_argument(
        "environment",
        choices=["local", "hosted"],
        help="Environment to use ('local' or 'hosted')",
    )
    args = parser.parse_args()

    if not setup_vectordb(args.environment):
        sys.exit(1)


if __name__ == "__main__":
    main()
