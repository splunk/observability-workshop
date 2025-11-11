from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.tools import tool
from models.schemas import OrderItem, InventoryReservation, OrderRequest
# Postgres
import psycopg2

from config import Settings

# In-memory example; replace with a real DB.
INVENTORY: Dict[str, int] = {"SKU-001": 10, "SKU-002": 0, "SKU-003": 5}

class InventoryInput(BaseModel):
    items: List[OrderItem]

@tool("check_and_reserve_inventory", args_schema=InventoryInput)
def check_and_reserve_inventory(items: List[OrderItem]) -> InventoryReservation:
    """Checks whether inventory is available for the specified list of items"""
    reserved, backordered = [], []
    for item in items:
        stock = INVENTORY.get(item.sku, 0)
        if stock >= item.quantity:
            INVENTORY[item.sku] = stock - item.quantity
            reserved.append(item)
        else:
            backordered.append(item)
    ok = len(backordered) == 0
    return InventoryReservation(ok=ok, reserved=reserved, backordered=backordered, error=None if ok else "Insufficient stock")

def add_order_to_db(order: OrderRequest):

    connection = None

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:

            with connection.cursor() as cursor:
                # Define the SQL query
                query = """INSERT INTO orders (customer_id, order_status, order_type,
                    order_date, store_id, warehouse_id, total_amount, shipping_address_line1,
                    shipping_address_line2, shipping_city, shipping_state, shipping_postal_code,
                    shipping_country)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING order_id; """

                # Execute the query
                cursor.execute(
                    query,
                    (
                        order.customer_info.customer_id,
                        'new',
                        order.order_type,
                        order.store_id,
                        order.warehouse_id,
                        0,
                        None if order.order_type == "pickup" else order.shipping_address.line1,
                        None if order.order_type == "pickup" else order.shipping_address.line2,
                        None if order.order_type == "pickup" else order.shipping_address.city,
                        None if order.order_type == "pickup" else order.shipping_address.state,
                        None if order.order_type == "pickup" else order.shipping_address.postal_code,
                        None if order.order_type == "pickup" else order.shipping_address.country
                    )
                )

                order_id = cursor.fetchone()[0]
                connection.commit() # Commit the transaction after successful insertion and fetching
                return order_id

    except Exception as e:
        if connection:
            connection.rollback() # Rollback in case of error
        raise e
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                pass