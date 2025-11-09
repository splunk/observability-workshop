from graph import build_graph
from shared.state import initial_state
from models.schemas import Message

def test_happy_path():
    app = build_graph()
    state = initial_state()
    state["order_id"] = "ORD-2002"
    state["messages"] = [Message(role="user", content="Order 1x SKU-003; pickup.")]
    result = app.invoke(state)
    assert result["fulfillment"].status in ("ready_for_pickup", "out_for_delivery")
    assert "notifications" in result