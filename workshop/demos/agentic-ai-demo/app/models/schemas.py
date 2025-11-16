from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field, EmailStr
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    next_agent: str  # Store routing decision
    customer_id: int

class Customer(BaseModel):
    customer_id: int = Field(..., description="Unique identifier for the customer")

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
