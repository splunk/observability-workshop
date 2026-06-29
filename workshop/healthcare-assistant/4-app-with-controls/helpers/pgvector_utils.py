"""Shared PostgreSQL/pgvector utilities for vector storage and retrieval."""
import os
from typing import Optional, Tuple

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import create_engine, text


def get_postgres_connection_string() -> str:
    """Build SQLAlchemy connection string from environment variables."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    database = os.environ.get("POSTGRES_DB", "vectordb")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


def get_collection_name(domain_name: str, environment: Optional[str] = None) -> str:
    """SQL-safe collection name for a domain/environment pair."""
    env = environment or os.environ.get("ENVIRONMENT", "local")
    return f"{domain_name}_{env}_index"


def collection_exists(domain_name: str, environment: Optional[str] = None) -> bool:
    """Return True if the pgvector collection has been created."""
    collection_name = get_collection_name(domain_name, environment)
    engine = create_engine(get_postgres_connection_string())
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT 1 FROM langchain_pg_collection WHERE name = :name LIMIT 1"),
            {"name": collection_name},
        ).fetchone()
    return row is not None


def create_pgvector_store(
    embeddings: OpenAIEmbeddings,
    domain_name: str,
    environment: Optional[str] = None,
    *,
    pre_delete_collection: bool = False,
) -> Tuple[PGVector, str]:
    """Create or connect to a PGVector store for the given domain."""
    collection_name = get_collection_name(domain_name, environment)
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=get_postgres_connection_string(),
        use_jsonb=True,
        pre_delete_collection=pre_delete_collection,
    )
    return vector_store, collection_name


def get_pgvector_store(
    domain_name: str,
    embedding_model: str = "text-embedding-3-large",
    environment: Optional[str] = None,
) -> Tuple[PGVector, str]:
    """Return a PGVector store for retrieval, raising if the collection is missing."""
    env = environment or os.environ.get("ENVIRONMENT", "local")
    collection_name = get_collection_name(domain_name, env)

    if not collection_exists(domain_name, env):
        raise ValueError(
            f"PostgreSQL collection not found: {collection_name}. "
            f"Run: python helpers/setup_vectordb.py {env}"
        )

    embeddings = OpenAIEmbeddings(model=embedding_model)
    return create_pgvector_store(embeddings, domain_name, env)
