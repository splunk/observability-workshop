from datetime import datetime
from typing import Literal
from models.schemas import GraphState
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def set_heartbeat(state: GraphState, agent_name: str) -> None:
    hb = state.get("heartbeat", {})
    hb[agent_name] = datetime.utcnow().isoformat()
    state["heartbeat"] = hb

def route(state: GraphState) -> GraphState:

    logging.debug(f"about to route based on {state}", state)
    set_heartbeat(state, "coordination")
    # If an error exists, decide whether to end or retry.
    if state.get("error"):
        state["next"] = "notify"
        return {"next": state["next"]}
    # Routing policy.
    if "items" not in state or "customer" not in state:
        state["next"] = "order_intake"
    elif "inventory" not in state:
        state["next"] = "inventory"
    elif state["inventory"].ok and "payment" not in state:
        state["next"] = "payment"
    elif state.get("payment") and state["payment"].status in ("authorized", "captured") and "fulfillment" not in state:
        state["next"] = "fulfillment"
    elif "fulfillment" in state and state["fulfillment"].status in ("ready_for_pickup", "out_for_delivery") and "notifications" not in state:
        state["next"] = "notify"
    else:
        state["next"] = "end"

    logging.debug(f"about to route to {state["next"]}")

    return {"next": state["next"]}