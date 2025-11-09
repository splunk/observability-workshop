from typing import Dict, Any
from models.schemas import GraphState

def initial_state() -> GraphState:
    return {
        "notifications": [],
        "messages": [],
        "heartbeat": {},
        "next": "order_intake",
    }