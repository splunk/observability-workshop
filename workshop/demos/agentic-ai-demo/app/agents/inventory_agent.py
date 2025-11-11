from models.schemas import GraphState
from tools.inventory_tool import check_and_reserve_inventory

def reserve(state: GraphState) -> GraphState:
    items = state.get("items", [])
    if not items:
        return {"error": "No items to reserve.", "next": "notify"}
    reservation = check_and_reserve_inventory.invoke({"items": items})
    next_step = "payment" if reservation.ok else "notify"
    return {"inventory": reservation, "next": next_step}