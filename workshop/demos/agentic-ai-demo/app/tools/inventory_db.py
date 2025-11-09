from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.tools import tool
from models.schemas import OrderItem, InventoryReservation

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