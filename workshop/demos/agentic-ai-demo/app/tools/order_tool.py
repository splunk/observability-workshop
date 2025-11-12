from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.tools import tool
from models.schemas import OrderItem, OrderRequest, OrderItemRequest, Customer, ShippingAddressRequest

# Postgres
import psycopg2
import psycopg2.extras

from config import Settings

@tool("add_order_to_db", args_schema=OrderRequest)
def add_order_to_db(order: OrderRequest) -> int:
    """Adds the specified order to the database"""
    connection = None

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:

                # --- Step 1: Lookup product_id and unit_price for each item and calculate total_amount ---
                processed_items = []
                total_amount = 0.0

                for item_request in order.items:
                    # Query the products table to get product_id and cost (unit_price)
                    cursor.execute(
                        "SELECT product_id, cost FROM products WHERE sku = %s;",
                        (item_request.sku,)
                    )
                    product_data = cursor.fetchone()

                    if not product_data:
                        raise ValueError(f"Product with SKU '{item_request.sku}' not found.")

                    product_id, unit_price = product_data
                    quantity = item_request.quantity

                    processed_items.append({
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price": float(unit_price) # Ensure it's a float for calculation
                    })
                    total_amount += quantity * float(unit_price)

                # --- Step 2: Insert into the 'orders' table ---
                orders_query = """INSERT INTO orders (customer_id, order_status, order_type,
                                    order_date, store_id, warehouse_id, total_amount, shipping_address_line1,
                                    shipping_address_line2, shipping_city, shipping_state, shipping_postal_code,
                                    shipping_country)
                                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    RETURNING order_id;"""

                cursor.execute(
                    orders_query,
                    (
                        order.customer_info.customer_id,
                        'new',
                        order.order_type,
                        order.store_id,
                        order.warehouse_id,
                        total_amount, # Use the calculated total_amount
                        None if order.order_type == "pickup" else (order.shipping_address.line1 if order.shipping_address else None),
                        None if order.order_type == "pickup" else (order.shipping_address.line2 if order.shipping_address else None),
                        None if order.order_type == "pickup" else (order.shipping_address.city if order.shipping_address else None),
                        None if order.order_type == "pickup" else (order.shipping_address.state if order.shipping_address else None),
                        None if order.order_type == "pickup" else (order.shipping_address.postal_code if order.shipping_address else None),
                        None if order.order_type == "pickup" else (order.shipping_address.country if order.shipping_address else None)
                    )
                )

                # Retrieve the newly generated order_id
                order_id = cursor.fetchone()[0]

                # --- Step 3: Insert items into the 'order_items' table ---
                order_items_query = """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                                        VALUES (%s, %s, %s, %s);"""

                for item in processed_items:
                    cursor.execute(
                        order_items_query,
                        (
                            order_id,
                            item["product_id"],
                            item["quantity"],
                            item["unit_price"]
                        )
                    )

                connection.commit()  # Commit the transaction after all insertions
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

class FetchOrdersForCustomerArgs(BaseModel):
    customer_id: int = Field(..., description="The ID of the customer to fetch orders for.")

@tool("fetch_orders_for_customer", args_schema=FetchOrdersForCustomerArgs)
def fetch_orders_for_customer(args: FetchOrdersForCustomerArgs) -> List[OrderRequest]:
    """Retrieves all orders for the specified customer"""
    connection = None
    customer_id = args.customer_id
    result_orders: List[OrderRequest] = []

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            # Use DictCursor to access columns by name, which is more readable
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # 1. Fetch main order details for the customer
                # We select only the columns relevant to the OrderRequest Pydantic model
                orders_query = """
                    SELECT
                        order_id, customer_id, order_type, store_id, warehouse_id,
                        shipping_address_line1, shipping_address_line2, shipping_city,
                        shipping_state, shipping_postal_code, shipping_country
                    FROM orders
                    WHERE customer_id = %s;
                """
                cursor.execute(orders_query, (customer_id,))
                order_records = cursor.fetchall()

                if not order_records:
                    return [] # No orders found for this customer, return empty list

                order_ids = [record['order_id'] for record in order_records]

                # 2. Fetch all order items (with SKU) for these orders
                # We join with the products table to get the SKU
                # Using `ANY(%s)` is the standard way to pass a list to an IN clause in psycopg2
                order_items_query = """
                    SELECT
                        oi.order_id, p.sku, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = ANY(%s);
                """
                cursor.execute(order_items_query, (order_ids,))
                order_item_records = cursor.fetchall()

                # Group order items by order_id for easier reconstruction
                order_items_map: Dict[int, List[Dict[str, Any]]] = {}
                for item_record in order_item_records:
                    order_id = item_record['order_id']
                    if order_id not in order_items_map:
                        order_items_map[order_id] = []
                    order_items_map[order_id].append({
                        "sku": item_record['sku'],
                        "quantity": item_record['quantity']
                    })

                # 3. Reconstruct OrderRequest objects
                for order_record in order_records:
                    shipping_address_obj: Optional[ShippingAddressRequest] = None
                    # Only create ShippingAddressRequest if it's a delivery order and address details exist
                    if order_record['order_type'] == "delivery" and order_record['shipping_address_line1']:
                        shipping_address_obj = ShippingAddressRequest(
                            line1=order_record['shipping_address_line1'],
                            line2=order_record['shipping_address_line2'],
                            city=order_record['shipping_city'],
                            state=order_record['shipping_state'],
                            postal_code=order_record['shipping_postal_code'],
                            country=order_record['shipping_country']
                        )

                    # Get the items for the current order from the map
                    items_for_this_order = [
                        OrderItemRequest(sku=item['sku'], quantity=item['quantity'])
                        for item in order_items_map.get(order_record['order_id'], [])
                    ]

                    # Create the OrderRequest Pydantic object
                    order_req = OrderRequest(
                        order_id=str(order_record['order_id']), # Convert DB int ID to str as per OrderRequest model
                        customer_info=Customer(customer_id=order_record['customer_id']),
                        order_type=order_record['order_type'],
                        items=items_for_this_order,
                        store_id=order_record['store_id'],
                        warehouse_id=order_record['warehouse_id'],
                        shipping_address=shipping_address_obj
                    )
                    result_orders.append(order_req)

                return result_orders

    except Exception as e:
        if connection:
            connection.rollback() # Rollback in case of any error during the transaction
        print(f"Error fetching orders for customer {customer_id}: {e}")
        raise e
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")