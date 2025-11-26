from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import tool

import psycopg2
import psycopg2.extras
import requests
import simplejson as json

from config import Settings


class ProcessOrderPaymentArgs(BaseModel):
    order_id: int = Field(..., description="Unique identifier for the order.")


@tool("process_order_payment", args_schema=ProcessOrderPaymentArgs)
def process_order_payment(order_id: int) -> str:
    """
    Processes the payment for the specified order by:
    - Fetching the order and payment method from the database.
    - Invoking a payment service to create a charge.
    - Updating the order payment_status and charge_token accordingly.

    Returns:
        A JSON string with the result, including status and any relevant identifiers.
    """

    connection: Optional[psycopg2.extensions.connection] = None

    try:
        connection = psycopg2.connect(Settings.DB_CONNECTION_STRING)

        # Use a RealDictCursor to access columns by name, and a transaction context.
        with connection, connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # --- Step 1: Lookup customer_id, payment_status, and order amount associated with the order ---
            cursor.execute(
                """
                SELECT customer_id, payment_status, total_amount
                FROM orders
                WHERE order_id = %s
                FOR UPDATE;
                """,
                (order_id,),
            )
            order_row = cursor.fetchone()

            if not order_row:
                return json.dumps(
                    {"ok": False, "error": "No order found for the provided order_id.", "order_id": order_id}
                )

            customer_id = order_row["customer_id"]
            payment_status = order_row["payment_status"]
            total_amount = order_row["total_amount"]

            # If already processed successfully, short-circuit.
            if payment_status == "successful":
                return json.dumps(
                    {"ok": True, "order_id": order_id, "status": "already_paid"}
                )

            # --- Step 2: Lookup the customer payment method ---
            cursor.execute(
                """
                SELECT cc_num, exp_month, exp_year, cvc
                FROM payment_methods
                WHERE customer_id = %s
                LIMIT 1;
                """,
                (customer_id,),
            )
            pm_row = cursor.fetchone()

            if not pm_row:
                return json.dumps(
                    {"ok": False, "error": "No payment methods found for the provided customer_id.", "customer_id": customer_id}
                )

            cc_num = pm_row["cc_num"]
            exp_month = int(pm_row["exp_month"])
            exp_year = int(pm_row["exp_year"])
            cvc = pm_row["cvc"]

            # --- Step 3: Invoke the payment service ---
            base_url = Settings.PAYMENT_SERVICE_URL
            idempotency_key = f"charge-order-{order_id}"

            payload = {
                "amount": int(total_amount),  # assuming total_amount is in smallest currency unit (e.g., cents)
                "currency": "USD",
                "payment_method": {
                    "number": cc_num,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
                "idempotency_key": idempotency_key,
                "metadata": {"order_id": str(order_id)},
            }

            try:
                resp = requests.post(
                    f"{base_url}/charges",
                    json=payload,
                    timeout=10,
                    headers={"Content-Type": "application/json"},
                )
                resp.raise_for_status()
            except requests.RequestException as re:
                return json.dumps(
                    {"ok": False, "error": "Payment service request failed.", "details": str(re), "order_id": order_id}
                )

            try:
                charge = resp.json()
            except ValueError:
                return json.dumps(
                    {"ok": False, "error": "Invalid JSON response from payment service.", "order_id": order_id}
                )

            charge_token = charge.get("charge_token") or charge.get("id")
            charge_status = charge.get("status", "unknown")

            if not charge_token:
                return json.dumps(
                    {"ok": False, "error": "Payment service did not return a charge token.", "order_id": order_id}
                )

            # --- Step 4: Update the payment_status based on the charge result ---
            if charge_status == "succeeded":
                cursor.execute(
                    """
                    UPDATE orders
                    SET payment_status = %s,
                        charge_token = %s
                    WHERE order_id = %s;
                    """,
                    ("successful", charge_token, order_id),
                )
                return json.dumps(
                    {"ok": True, "order_id": order_id, "status": "successful", "charge_token": charge_token}
                )
            else:
                cursor.execute(
                    """
                    UPDATE orders
                    SET payment_status = %s,
                        charge_token = %s
                    WHERE order_id = %s;
                    """,
                    ("failed", charge_token, order_id),
                )
                return json.dumps(
                    {"ok": False, "order_id": order_id, "status": charge_status, "charge_token": charge_token}
                )

    except Exception as e:
        # Roll back the transaction if anything unexpected occurs.
        if connection:
            try:
                connection.rollback()
            except Exception:
                pass
        return json.dumps(
            {"ok": False, "error": "Unhandled error during payment processing.", "details": str(e), "order_id": order_id}
        )
    finally:
        # Ensure the connection is closed.
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass