from langgraph.graph import StateGraph, END, START
from models.schemas import GraphState
from agents.coordination_agent import route as coordination_node
from agents.order_agent import intake as order_intake_node, payment as payment_node
from agents.inventory_agent import reserve as inventory_node
from agents.fulfillment_agent import fulfill as fulfillment_node
from agents.notification_agent import notify as notification_node
from agents.chatbot_agent import chat as chatbot_node

def build_graph():
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("coordination", coordination_node)
    graph.add_node("order_intake", order_intake_node)
    graph.add_node("inventory", inventory_node)
    graph.add_node("payment", payment_node)
    graph.add_node("fulfillment", fulfillment_node)
    graph.add_node("notify", notification_node)
    graph.add_node("chat", chatbot_node)  # optional path

    # Start at coordination
    graph.add_edge(START, "coordination")

    # Conditional routing driven by state["next"]
    def router(state: GraphState) -> str:
        return state.get("next", "end")

    graph.add_conditional_edges(
        "coordination",
        router,
        {
            "order_intake": "order_intake",
            "inventory": "inventory",
            "payment": "payment",
            "fulfillment": "fulfillment",
            "notify": "notify",
            "chat": "chat",
            "end": END,
        },
    )

    # After each node, return to coordination for next decision.
    for node in ["order_intake", "inventory", "payment", "fulfillment", "notify", "chat"]:
        graph.add_edge(node, "coordination")

    return graph.compile()