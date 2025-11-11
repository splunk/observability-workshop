from typing import Dict, Any
from models.schemas import GraphState, OrderRequest, PaymentResult, InventoryReservation, FulfillmentResult

def initial_state() -> GraphState:
    return {
        "order": OrderRequest(),
        "order_intake": False,
        "notifications": [],
        "heartbeat": {},
        "payment": PaymentResult(),
        "inventory": InventoryReservation(),
        "fulfillment": FulfillmentResult(),
    }