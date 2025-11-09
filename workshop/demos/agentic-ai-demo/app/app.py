from graph import build_graph
from shared.state import initial_state
from models.schemas import Message

def main():
    app = build_graph()
    state = initial_state()
    state["order_id"] = "ORD-1001"
    state["messages"] = [Message(role="user", content="I'd like 1 x SKU-001. Pick up please.")]
    final_state = app.invoke(state)
    print("Final state:", final_state)

if __name__ == "__main__":
    main()