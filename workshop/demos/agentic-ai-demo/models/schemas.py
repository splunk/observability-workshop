from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field, EmailStr

class OrderItem(BaseModel):
    sku: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class Customer(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20)

class PaymentResult(BaseModel):
    status: Literal["authorized", "declined", "captured"] = "authorized"
    transaction_id: Optional[str] = None
    amount_cents: int = 0
    currency: str = "USD"
    error: Optional[str] = None

class InventoryReservation(BaseModel):
    ok: bool = False
    reserved: List[OrderItem] = []
    backordered: List[OrderItem] = []
    error: Optional[str] = None

class FulfillmentResult(BaseModel):
    status: Literal["pending", "ready_for_pickup", "out_for_delivery", "failed"] = "pending"
    location_id: Optional[str] = None
    tracking_id: Optional[str] = None
    error: Optional[str] = None

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class GraphState(TypedDict, total=False):
    order_id: str
    items: List[OrderItem]
    customer: Customer
    payment: PaymentResult
    inventory: InventoryReservation
    fulfillment: FulfillmentResult
    notifications: List[str]
    messages: List[Message]
    error: Optional[str]
    next: str  # routing key the coordination agent uses
    heartbeat: dict  # agent name -> last timestamp or counters