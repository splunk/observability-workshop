from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from langchain.tools import tool
from models.schemas import Customer, OrderRequest, OrderItemRequest

# Postgres
import psycopg2
import psycopg2.extras
from psycopg2.extras import DictCursor

import simplejson as json

from config import Settings
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@tool("create_order", args_schema=OrderRequest)
def create_order(
    order_id: Optional[str] = None,
    customer_info: Customer = None,
    items: List[OrderItemRequest] = None,
    store_id: Optional[int] = None,
) -> int:
    """Adds the specified order to the database and returns the new order_id."""
    # Re-construct and validate the full request inside the tool
    order = OrderRequest(
        order_id=order_id,
        customer_info=customer_info,
        items=items,
        store_id=store_id,
    )

    connection = None

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:

                # --- Step 1: Lookup product_sku and unit_price for each item and calculate total_amount ---
                processed_items = []
                total_amount = 0.0

                for item_request in order.items:
                    # Query the products table to get product_sku and cost (unit_price)
                    cursor.execute(
                        "SELECT product_sku, cost FROM products WHERE product_sku = %s;",
                        (item_request.product_sku,)
                    )
                    product_data = cursor.fetchone()

                    if not product_data:
                        raise ValueError(f"Product with SKU '{item_request.product_sku}' not found.")

                    product_sku, unit_price = product_data
                    quantity = item_request.quantity

                    processed_items.append({
                        "product_sku": product_sku,
                        "quantity": quantity,
                        "unit_price": float(unit_price) # Ensure it's a float for calculation
                    })
                    total_amount += quantity * float(unit_price)

                # --- Step 2: Insert into the 'orders' table ---
                orders_query = """INSERT INTO orders (customer_id, order_status,
                                    order_date, store_id, total_amount, payment_status)
                                    VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
                                    RETURNING order_id;"""

                cursor.execute(
                    orders_query,
                    (
                        order.customer_info.customer_id,
                        'new',
                        order.store_id,
                        total_amount,  # Use the calculated total_amount
                        'unpaid'
                    )
                )

                # Retrieve the newly generated order_id
                order_id = cursor.fetchone()[0]

                # --- Step 3: Insert items into the 'order_items' table ---
                order_items_query = """INSERT INTO order_items (order_id, product_sku, quantity, unit_price)
                                        VALUES (%s, %s, %s, %s);"""

                for item in processed_items:
                    cursor.execute(
                        order_items_query,
                        (
                            order_id,
                            item["product_sku"],
                            item["quantity"],
                            item["unit_price"]
                        )
                    )

                connection.commit()  # Commit the transaction after all insertions
                return json.dumps(order_id, use_decimal=True)

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

class FetchOrdersForCustomerArgs(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer to fetch orders for.")

@tool("fetch_orders_for_customer", args_schema=FetchOrdersForCustomerArgs)
def fetch_orders_for_customer(customer_id: int) -> List[Dict[str, Any]]:
    """Retrieves all orders for the specified customer"""
    connection = None
    result_orders: List[Dict[str, Any]] = [] # Changed type hint

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                orders_query = """
                    SELECT
                        order_id, customer_id, order_status, order_date,
                        store_id, total_amount
                    FROM orders
                    WHERE customer_id = %s;
                """
                cursor.execute(orders_query, (customer_id,))
                order_records = cursor.fetchall()

                if not order_records:
                    return json.dumps("No orders found for the provided customer_id.")

                order_ids = [record['order_id'] for record in order_records]

                order_items_query = """
                    SELECT
                        oi.order_id, p.product_sku, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_sku = p.product_sku
                    WHERE oi.order_id = ANY(%s);
                """
                cursor.execute(order_items_query, (order_ids,))
                order_item_records = cursor.fetchall()

                order_items_map: Dict[int, List[Dict[str, Any]]] = {}
                for item_record in order_item_records:
                    order_id = item_record['order_id']
                    if order_id not in order_items_map:
                        order_items_map[order_id] = []
                    order_items_map[order_id].append({
                        "product_sku": item_record['product_sku'],
                        "quantity": item_record['quantity']
                    })

                for order_record in order_records:

                    # Get the items for the current order from the map as a list of dictionaries
                    items_for_this_order = [
                        {"product_sku": item['product_sku'], "quantity": item['quantity']}
                        for item in order_items_map.get(order_record['order_id'], [])
                    ]

                    # Create a dictionary representing the order
                    order_dict = {
                        "order_id": str(order_record['order_id']),
                        "customer_id": str(order_record['customer_id']),
                        "order_status": str(order_record['order_status']),
                        "store_id": str(order_record['store_id']),
                        "total_amount": str(order_record['total_amount']),
                        "items": items_for_this_order
                    }
                    result_orders.append(order_dict) # Append the dictionary

                return json.dumps(result_orders, use_decimal=True)

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error fetching orders for customer {customer_id}: {e}")
        raise e
    finally:
        if connection is not None:
             try:
                connection.close()
             except Exception as e:
                print(f"Error closing database connection: {e}")

def archive_orders():
    """
    Called periodically to archive older orders, which ensures the order table doesn't grow too large.
    """

    connection = None
    try:
        connection = psycopg2.connect(Settings.DB_CONNECTION_STRING)
        # Using the connection as a context manager will commit on success and
        # roll back automatically if an exception is raised.
        with connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    "DELETE FROM orders WHERE order_date < NOW() - INTERVAL '6 hours';"
                )
    except Exception as e:
        # Extra safety: rollback if the connection exists.
        if connection:
            try:
                connection.rollback()
            except Exception:
                pass
        logging.getLogger().error(f"Error archiving orders: {e}")
        raise
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                logging.getLogger().error(f"Error closing database connection: {e}")