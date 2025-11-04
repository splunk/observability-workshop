from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import tool
from models.schemas import PaymentResult

class PaymentInput(BaseModel):
    order_id: str = Field(..., min_length=1)
    amount_cents: int = Field(..., gt=0)
    currency: str = "USD"
    payment_method_token: str = Field(..., min_length=8)

@tool("process_payment", args_schema=PaymentInput)
def process_payment(order_id: str, amount_cents: int, currency: str, payment_method_token: str) -> PaymentResult:
    """Processes a payment of the specified amount and currency"""
    # Placeholder for a PCI-compliant gateway call; do not log sensitive tokens.
    authorized = payment_method_token.endswith("OK")
    if not authorized:
        return PaymentResult(status="declined", amount_cents=amount_cents, currency=currency, error="Authorization failed")
    return PaymentResult(status="authorized", transaction_id=f"txn_{order_id}", amount_cents=amount_cents, currency=currency)