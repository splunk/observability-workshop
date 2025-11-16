from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field, EmailStr
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    next_agent: str  # Store routing decision
    customer_id: int

class OrderItem(BaseModel):
    sku: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class Customer(BaseModel):
    customer_id: int = Field(..., description="Unique identifier for the customer")

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

class OrderItemRequest(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit of the item")
    quantity: int = Field(..., gt=0, description="Quantity of the item")

class ShippingAddressRequest(BaseModel):
    line1: str = Field(..., description="Shipping address line 1")
    line2: Optional[str] = Field(None, description="Shipping address line 2")
    city: str = Field(..., description="Shipping city")
    state: str = Field(..., description="Shipping state/province")
    postal_code: str = Field(..., description="Shipping postal code")
    country: str = Field(..., description="Shipping country")

class OrderRequest(BaseModel):
    order_id: Optional[str] = Field(None, description="Optional unique identifier for the order. If not provided, one will be generated.")
    customer_info: Customer = None
    order_type: str = Field("delivery", pattern="^(delivery|pickup)$", description="Type of order: 'delivery' or 'pickup'")
    items: List[OrderItemRequest] = Field([], min_items=1, description="List of items in the order")
    store_id: Optional[int] = Field(None, description="ID of the store for pickup orders")
    warehouse_id: Optional[int] = Field(None, description="ID of the warehouse for fulfillment")
    shipping_address: Optional[ShippingAddressRequest] = Field(None, description="Shipping address details for delivery orders")

class GraphState(TypedDict, total=False):
    order: OrderRequest
    order_intake: bool = False
    payment: PaymentResult
    inventory: InventoryReservation
    fulfillment: FulfillmentResult
    notifications: List[str]
    messages: List[Message]
    error: Optional[str]
    next: str  # routing key the coordination agent uses
    heartbeat: dict  # agent name -> last timestamp or counters
