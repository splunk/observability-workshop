from typing import Dict, Any
from models.schemas import GraphState, PaymentResult, InventoryReservation, FulfillmentResult

def initial_state() -> GraphState:
    return {
        "messages": [],
        "notifications": [],
        "heartbeat": {},
        "payment": PaymentResult(),
        "inventory": InventoryReservation(),
        "fulfillment": FulfillmentResult(),
    }