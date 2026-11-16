"""PostgreSQL utilities for relational demo tables and SQL execution."""
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from helpers.pgvector_utils import get_postgres_connection_string


def relational_table_name(domain_name: str, table_suffix: str) -> str:
    """Build a domain-scoped, SQL-safe table name."""
    safe_domain = re.sub(r"[^a-z0-9_]", "_", domain_name.lower())
    safe_suffix = re.sub(r"[^a-z0-9_]", "_", table_suffix.lower())
    return f"{safe_domain}_{safe_suffix}"


def parse_relational_csv_name(csv_path: str | Path) -> Optional[str]:
    """Extract the table suffix from relational_<name>.csv."""
    stem = Path(csv_path).stem
    prefix = "relational_"
    if not stem.startswith(prefix):
        return None
    suffix = stem[len(prefix) :].strip()
    return suffix or None


def _infer_pg_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "BIGINT"
    if pd.api.types.is_float_dtype(series):
        return "NUMERIC"
    return "TEXT"


def _guess_primary_key(columns: List[str]) -> str:
    for col in columns:
        if col.endswith("_id"):
            return col
    return columns[0]


def _sanitize_identifier(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


def load_relational_csv(
    engine: Engine,
    csv_path: str | Path,
    domain_name: str,
) -> Tuple[str, int]:
    """Load a relational_<table>.csv file into PostgreSQL."""
    csv_path = Path(csv_path)
    table_suffix = parse_relational_csv_name(csv_path)
    if not table_suffix:
        raise ValueError(f"Not a relational CSV file: {csv_path}")

    table_name = relational_table_name(domain_name, table_suffix)
    df = pd.read_csv(csv_path, skipinitialspace=True)
    if df.empty:
        raise ValueError(f"No rows found in {csv_path}")

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    columns = [_sanitize_identifier(str(c)) for c in df.columns]
    df.columns = columns
    pk_col = _guess_primary_key(columns)

    col_defs = []
    for col in columns:
        pg_type = _infer_pg_type(df[col])
        col_defs.append(f'"{col}" {pg_type}')

    create_sql = (
        f'CREATE TABLE "{table_name}" (\n  '
        + ",\n  ".join(col_defs)
        + f',\n  PRIMARY KEY ("{pk_col}")\n)'
    )

    with engine.begin() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
        conn.execute(text(create_sql))

        column_list = ", ".join(f'"{c}"' for c in columns)
        placeholders = ", ".join(f":{col}" for col in columns)
        insert_sql = (
            f'INSERT INTO "{table_name}" ({column_list}) '
            f"VALUES ({placeholders})"
        )
        conn.execute(text(insert_sql), df.to_dict(orient="records"))

        for col in columns:
            if col == pk_col:
                continue
            conn.execute(
                text(
                    f'CREATE INDEX IF NOT EXISTS "{table_name}_{col}_idx" '
                    f'ON "{table_name}" ("{col}")'
                )
            )

    return table_name, len(df)


def load_domain_relational_csvs(docs_dir: str | Path, domain_name: str) -> List[Tuple[str, int]]:
    """Load every relational_*.csv file in the docs directory."""
    docs_path = Path(docs_dir)
    engine = create_engine(get_postgres_connection_string())
    results: List[Tuple[str, int]] = []

    for csv_path in sorted(docs_path.glob("relational_*.csv")):
        table_name, row_count = load_relational_csv(engine, csv_path, domain_name)
        print(f"✓ Loaded relational table {table_name} ({row_count} rows) from {csv_path.name}")
        results.append((table_name, row_count))

    return results


def get_table_schema_description(engine: Engine, table_name: str) -> str:
    """Return a human-readable schema snippet for Text-to-SQL prompts."""
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table not found: {table_name}")

    pk = inspector.get_pk_constraint(table_name).get("constrained_columns") or []
    lines = [f'Table "{table_name}" columns:']
    for col in inspector.get_columns(table_name):
        name = col["name"]
        col_type = str(col["type"])
        extras = []
        if name in pk:
            extras.append("PRIMARY KEY")
        if col.get("nullable") is False and name not in pk:
            extras.append("NOT NULL")
        suffix = f" ({', '.join(extras)})" if extras else ""
        lines.append(f"  - {name}: {col_type}{suffix}")
    return "\n".join(lines)


def _sql_operation(sql: str) -> str:
    cleaned = (sql or "").strip().lstrip("(").upper()
    for keyword in ("SELECT", "DELETE", "INSERT", "UPDATE"):
        if cleaned.startswith(keyword):
            return keyword.lower()
    return "unknown"


def execute_sql(sql: str) -> Dict[str, Any]:
    """Execute a SQL statement and return a JSON-serializable result."""
    sql_clean = (sql or "").strip().rstrip(";")
    operation = _sql_operation(sql_clean)
    engine = create_engine(get_postgres_connection_string())

    with engine.begin() as conn:
        result = conn.execute(text(sql_clean))
        if operation == "select":
            rows = [dict(row) for row in result.mappings()]
            count = len(rows)
        else:
            rows = []
            count = result.rowcount

    return {
        "sql": sql_clean,
        "rows": rows,
        "count": count,
        "source": "postgres",
        "operation": operation,
    }
