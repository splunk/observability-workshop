from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field, EmailStr
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    next_agent: str  # Store routing decision
    customer_id: int
    inventory_summary: Optional[str]
    order_summary: Optional[str]
    product_summary: Optional[str]
    payment_summary: Optional[str]
    final_answer: Optional[str]
    fulfilled_by: Optional[str]
    finalized_by_selector: bool

class Customer(BaseModel):
    customer_id: int = Field(..., description="Unique identifier for the customer")

class OrderItemRequest(BaseModel):
    product_sku: str = Field(..., description="Stock Keeping Unit of the item")
    quantity: int = Field(..., gt=0, description="Quantity of the item")

class OrderRequest(BaseModel):
    order_id: Optional[str] = Field(None, description="Optional unique identifier for the order. If not provided, one will be generated.")
    customer_info: Customer = None
    items: List[OrderItemRequest] = Field([], min_items=1, description="List of items in the order")
    store_id: Optional[int] = Field(None, description="ID of the store for pickup orders")
