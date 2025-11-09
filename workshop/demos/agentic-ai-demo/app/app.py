import logging
import uuid


from typing import List, Optional, TypedDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from opentelemetry import trace

# local
from config import Settings
from graph import build_graph
from shared.state import initial_state
from models.schemas import Message, OrderItem, OrderRequest, Customer, PaymentResult, InventoryReservation, FulfillmentResult, GraphState
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="Order Processing API",
    description="API for submitting customer orders to the LangGraph application.",
    version="1.0.0",
)

service_name = Settings.OTEL_SERVICE_NAME

# Initialize Traces
tracer = trace.get_tracer_provider().get_tracer(service_name)

langgraph_app = build_graph()

@app.post("/orders", response_model=dict, summary="Submit a new order")
async def create_order(order_data: OrderRequest):
    """
    Receives an HTTP POST request with order details, processes it through the LangGraph application,
    and returns the final state of the order.
    """
    try:
        with tracer.start_as_current_span("create_order") as span:
            logging.debug(f"About to process order: {order_data}")

            # Prepare the initial state for LangGraph
            state: GraphState = initial_state()

            # Map incoming order_data to GraphState
            order_id = order_data.order_id if order_data.order_id else str(uuid.uuid4())
            state["order_id"] = order_id
            span.set_attribute("app.order_id", order_id)

            state["customer"] = Customer(customer_id=order_data.customer_info.customer_id)
            span.set_attribute("app.order_id", order_data.customer_info.customer_id)

            # Convert Pydantic OrderItemRequest to your internal OrderItem objects
            state["items"] = [OrderItem(sku=item.sku, quantity=item.quantity) for item in order_data.items]

            # Construct the initial message for the graph, similar to your original example
            # This allows your existing graph nodes that parse messages to continue working.
            item_descriptions = [f"{item.quantity} x {item.sku}" for item in order_data.items]
            user_message_content = f"I'd like {', '.join(item_descriptions)}. {order_data.order_type.capitalize()} please."
            state["messages"].append(Message(role="user", content=user_message_content))

            # Pass other relevant structured fields directly to the state for graph nodes to use
            state["order_type"] = order_data.order_type
            if order_data.store_id:
                state["store_id"] = order_data.store_id
            if order_data.warehouse_id:
                state["warehouse_id"] = order_data.warehouse_id
            if order_data.shipping_address and order_data.order_type == "delivery":
                # You can pass the Pydantic model directly or convert it to a string/custom object
                state["shipping_address"] = order_data.shipping_address

            # Invoke the LangGraph application
            final_state = langgraph_app.invoke(state)

            # Convert the final_state objects to dictionaries for JSON serialization
            serializable_final_state = {}
            for key, value in final_state.items():
                if hasattr(value, 'to_dict'):
                    serializable_final_state[key] = value.to_dict()
                elif isinstance(value, list):
                    serializable_final_state[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
                elif isinstance(value, BaseModel): # Handle Pydantic models if they are in the final_state
                    serializable_final_state[key] = value.model_dump()
                else:
                    serializable_final_state[key] = value

            return serializable_final_state

    except Exception as e:
        # Log the error for debugging
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing order: {str(e)}")
