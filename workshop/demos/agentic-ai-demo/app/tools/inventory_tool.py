from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, conint
from langchain.tools import tool
from itertools import chain
from collections import defaultdict

# Postgres
import psycopg2
import psycopg2.extras

from config import Settings

class ProductStorePair(BaseModel):
    product_id: int = Field(..., description="Unique identifier for the product.")
    store_id: int = Field(..., description="Unique identifier for the store.")

class GetInventoryForPairsArgs(BaseModel):
    pairs: List[ProductStorePair] = Field(
        ..., min_items=1, description="List of (product_id, store_id) pairs to fetch."
    )

@tool("get_inventory_for_products_and_stores", args_schema=GetInventoryForPairsArgs)
def get_inventory_for_products_and_stores(pairs: List[Dict[str, int]]) -> List[Dict[str, Any]]:
    """Retrieves inventory for the specified (product_id, store_id) pairs."""
    connection = None
    result_inventory: List[Dict[str, Any]] = []

    if not pairs:
        return result_inventory

    # Flatten parameters for (%s, %s), (%s, %s), ...
    tuple_placeholders = ", ".join(["(%s, %s)"] * len(pairs))
    params = list(chain.from_iterable((p["product_id"], p["store_id"]) for p in pairs))

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = f"""
                    SELECT
                        i.inventory_id,
                        i.product_id,
                        i.store_id,
                        i.quantity
                    FROM inventory AS i
                    WHERE (i.product_id, i.store_id) IN ({tuple_placeholders})
                    ORDER BY i.inventory_id
                """
                cursor.execute(query, params)
                for r in cursor.fetchall():
                    result_inventory.append({
                        "inventory_id": str(r["inventory_id"]),
                        "product_id": str(r["product_id"]),
                        "store_id": r["store_id"],
                        "quantity": r["quantity"],
                    })

        return result_inventory

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error fetching inventory for pairs {pairs}: {e}")
        raise
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")

class DecrementItem(BaseModel):
    product_id: int = Field(..., description="Product ID.")
    store_id: int = Field(..., description="Store ID.")
    quantity: conint(gt=0) = Field(..., description="Amount to decrement (must be > 0).")

class BatchDecrementArgs(BaseModel):
    items: List[DecrementItem] = Field(..., min_items=1, description="List of items to decrement.")
    all_or_none: bool = Field(
        default=True,
        description="If True, rollback unless all items succeed. If False, apply partial updates and report failures."
    )

@tool("batch_decrement_inventory", args_schema=BatchDecrementArgs)
def batch_decrement_inventory(items: List[Dict[str, int]], all_or_none: bool = True) -> Dict[str, Any]:
    """
    Decrements inventory for multiple (product_id, store_id, quantity) items in one statement.
    Aggregates duplicates and prevents negative quantities.
    """
    connection = None

    # Aggregate duplicates (sum quantities per (product_id, store_id))
    agg = defaultdict(int)
    for it in items:
        key = (int(it["product_id"]), int(it["store_id"]))
        qty = int(it["quantity"])
        if qty <= 0:
            continue
        agg[key] += qty

    if not agg:
        return {"status": "no_op", "updated": [], "failed": []}

    pairs: List[Tuple[int, int, int]] = [(pid, sid, qty) for (pid, sid), qty in agg.items()]
    tuple_placeholders = ", ".join(["(%s, %s, %s)"] * len(pairs))
    params: List[int] = []
    for pid, sid, qty in pairs:
        params.extend([pid, sid, qty])

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = f"""
                    WITH v(product_id, store_id, qty) AS (
                        VALUES {tuple_placeholders}
                    )
                    UPDATE inventory AS i
                    SET quantity = i.quantity - v.qty
                    FROM v
                    WHERE i.product_id = v.product_id
                      AND i.store_id = v.store_id
                      AND i.quantity >= v.qty
                    RETURNING i.inventory_id, i.product_id, i.store_id, i.quantity
                """
                cursor.execute(query, params)
                updated_rows = cursor.fetchall()

                # Build sets to detect failures
                requested_keys = {(pid, sid) for (pid, sid, _qty) in pairs}
                updated_keys = {(int(r["product_id"]), int(r["store_id"])) for r in updated_rows}
                failed_keys = requested_keys - updated_keys

                if all_or_none and failed_keys:
                    connection.rollback()
                    failed_list = [
                        {"product_id": str(pid), "store_id": sid, "requested_decrement": next(q for (p, s, q) in pairs if p == pid and s == sid)}
                        for (pid, sid) in failed_keys
                    ]
                    return {
                        "status": "rolled_back",
                        "reason": "One or more items not found or insufficient quantity.",
                        "updated": [],
                        "failed": failed_list,
                    }

                # Partial success or full success
                failed_list = [
                        {"product_id": str(pid), "store_id": sid, "requested_decrement": next(q for (p, s, q) in pairs if p == pid and s == sid)}
                        for (pid, sid) in failed_keys
                    ]
                updated_list = [{
                    "inventory_id": str(r["inventory_id"]),
                    "product_id": str(r["product_id"]),
                    "store_id": r["store_id"],
                    "new_quantity": r["quantity"],
                } for r in updated_rows]

                return {
                    "status": "updated" if not failed_list else "partial",
                    "updated": updated_list,
                    "failed": failed_list,
                }

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error batch decrementing inventory: {e}")
        raise
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")

class IncrementItem(BaseModel):
    product_id: int = Field(..., description="Product ID.")
    store_id: int = Field(..., description="Store ID.")
    quantity: conint(gt=0) = Field(..., description="Amount to increment (must be > 0).")

class BatchUpsertIncrementArgs(BaseModel):
    items: List[IncrementItem] = Field(..., min_items=1, description="List of items to increment or insert.")

@tool("batch_upsert_increment_inventory", args_schema=BatchUpsertIncrementArgs)
def batch_upsert_increment_inventory(items: List[Dict[str, int]]) -> Dict[str, Any]:
    """
    Increments inventory for multiple items; inserts missing rows.
    """
    connection = None
    from itertools import chain

    # Aggregate duplicates
    from collections import defaultdict
    agg = defaultdict(int)
    for it in items:
        key = (int(it["product_id"]), int(it["store_id"]))
        qty = int(it["quantity"])
        if qty <= 0:
            continue
        agg[key] += qty

    if not agg:
        return {"status": "no_op", "rows": []}

    triples = [(pid, sid, qty) for (pid, sid), qty in agg.items()]
    placeholders = ", ".join(["(%s, %s, %s)"] * len(triples))
    params = list(chain.from_iterable(triples))

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = f"""
                    WITH v(product_id, store_id, qty) AS (
                        VALUES {placeholders}
                    )
                    INSERT INTO inventory (product_id, store_id, quantity)
                    SELECT v.product_id, v.store_id, v.qty
                    FROM v
                    ON CONFLICT (product_id, store_id) DO UPDATE
                    SET quantity = inventory.quantity + EXCLUDED.quantity
                    RETURNING inventory_id, product_id, store_id, quantity
                """
                cursor.execute(query, params)
                rows = cursor.fetchall()
                result = [{
                    "inventory_id": str(r["inventory_id"]),
                    "product_id": str(r["product_id"]),
                    "store_id": r["store_id"],
                    "new_quantity": r["quantity"],
                } for r in rows]
                return {"status": "upserted", "rows": result}
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error batch upsert incrementing inventory: {e}")
        raise
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")