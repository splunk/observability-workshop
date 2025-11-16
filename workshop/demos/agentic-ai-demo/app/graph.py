from langgraph.graph import StateGraph, END
from models.schemas import AgentState
from agents.coordination_agent import coordinator_node, route_based_on_state
from agents.order_agent import order_agent as order_node
from agents.product_agent import product_agent as product_node

def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("product", product_node)
    graph.add_node("order", order_node)

    # Start at coordinator
    graph.set_entry_point("coordinator")

    graph.add_conditional_edges(
        "coordinator",
        route_based_on_state,
        {
            "product": "product",
            "order": "order",
            "complete": END,
        },
    )

    # After each node, return to coordination for next decision.
    for node in ["product", "order"]:
        graph.add_edge(node, "coordinator")

    return graph.compile()