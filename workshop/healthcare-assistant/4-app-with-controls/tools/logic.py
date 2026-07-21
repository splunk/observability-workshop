"""
Healthcare domain tools.

- get_patient_info: Text-to-SQL lookup against the patient registry in PostgreSQL
- delete_patient_record: Text-to-SQL delete against the patient registry in PostgreSQL
- search_medicine_qa: semantic vector search against the QA knowledge base
"""
import json
import logging
from typing import Optional, Tuple

from langchain_postgres import PGVector

from config import DOMAIN, load_config
from helpers.agent_control_helpers import make_controlled_tool
from helpers.pgvector_utils import get_pgvector_store
from helpers.sql_utils import execute_sql, relational_table_name
from helpers.text_to_sql_utils import generate_sql
from rag import get_rag_system

_TABLE_SUFFIX = "patient"
_ID_COLUMN = "patient_id"

_vector_store: Optional[PGVector] = None
_embedding_model: Optional[str] = None
_collection_name_cached: Optional[str] = None


def _get_vector_store() -> Tuple[PGVector, str]:
    global _vector_store, _embedding_model, _collection_name_cached

    app_config = load_config()
    embedding_model = (
        app_config.get("vectorstore", {}).get("embedding_model") or "text-embedding-3-large"
    )

    if (
        _vector_store is not None
        and _collection_name_cached is not None
        and _embedding_model == embedding_model
    ):
        return _vector_store, _collection_name_cached

    _vector_store, collection_name = get_pgvector_store(DOMAIN, embedding_model)
    _embedding_model = embedding_model
    _collection_name_cached = collection_name
    return _vector_store, collection_name


async def _execute_patient_sql(sql: str) -> str:
    """Execute a SQL lookup against the patient registry."""
    try:
        result = execute_sql(sql)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e), "sql": sql})


_execute_patient_sql = make_controlled_tool(_execute_patient_sql, "get_patient_info")


async def _execute_patient_delete_sql(sql: str) -> str:
    """Execute a SQL delete against the patient registry."""
    try:
        result = execute_sql(sql)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e), "sql": sql})


_execute_patient_delete_sql = make_controlled_tool(_execute_patient_delete_sql, "delete_patient_record")


async def get_patient_info(patient_id: str) -> str:
    """Retrieve patient information by their patient ID."""
    patient_id = patient_id.strip().upper()
    q = (patient_id or "").strip()
    if not q:
        return json.dumps({"error": "patient_id is required"})

    app_config = load_config()
    model = app_config.get("model", {}).get("default_model", "gpt-4o-mini")
    table_name = relational_table_name(DOMAIN, _TABLE_SUFFIX)

    try:
        sql = await generate_sql(
            domain_name=DOMAIN,
            table_suffix=_TABLE_SUFFIX,
            id_column=_ID_COLUMN,
            record_id=q,
            operation="select",
            model=model,
            use_case_identifier="patient_id",
            use_case_value=patient_id,
        )
    except Exception as e:
        return json.dumps({"error": str(e), "patient_id": q})

    raw = await _execute_patient_sql(sql)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"error": "Invalid SQL execution response", "raw": raw}

    if "error" not in result:
        result["query"] = q
        result["table"] = table_name

    return json.dumps(result)


async def delete_patient_record(patient_id: str) -> str:
    """Permanently delete a patient record from the registry by patient ID."""
    patient_id = patient_id.strip().upper()
    q = (patient_id or "").strip()
    if not q:
        return json.dumps({"error": "patient_id is required"})

    app_config = load_config()
    model = app_config.get("model", {}).get("default_model", "gpt-4o-mini")
    table_name = relational_table_name(DOMAIN, _TABLE_SUFFIX)

    try:
        sql = await generate_sql(
            domain_name=DOMAIN,
            table_suffix=_TABLE_SUFFIX,
            id_column=_ID_COLUMN,
            record_id=q,
            operation="delete",
            model=model,
            use_case_identifier="patient_id",
            use_case_value=patient_id,
        )
    except Exception as e:
        return json.dumps({"error": str(e), "patient_id": q})

    raw = await _execute_patient_delete_sql(sql)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"error": "Invalid SQL execution response", "raw": raw}

    if "error" not in result:
        result["query"] = q
        result["table"] = table_name

    return json.dumps(result)


async def search_medicine_qa(query: str) -> str:
    """Search the Medicine knowledge base using semantic vector search."""
    q = query
    try:
        _get_vector_store()
    except Exception as e:
        return json.dumps({"error": str(e), "query": q})

    try:
        rag_system = get_rag_system(top_k=1)
        raw = await rag_system.search(q)
    except Exception as e:
        logging.exception("search_medicine_qa search failed")
        return json.dumps({"error": str(e), "query": q})

    return json.dumps([raw])


TOOLS = [get_patient_info, delete_patient_record, search_medicine_qa]
