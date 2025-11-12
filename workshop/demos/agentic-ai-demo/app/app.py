import logging
import asyncio

from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

from opentelemetry import trace
from opentelemetry.instrumentation.auto_instrumentation import initialize
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

# OpenTelemetry initialize() must be called before importing FastAPI because of how instrumentation is patched
initialize()

from fastapi import FastAPI, HTTPException

# local
from config import Settings
from graph import build_graph
from shared.state import initial_state
from models.schemas import Message, OrderItem, OrderRequest, Customer, PaymentResult, InventoryReservation, FulfillmentResult, GraphState
from dotenv import load_dotenv
from tools.order_tool import fetch_orders_for_customer, FetchOrdersForCustomerArgs

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

instrumentor = LangchainInstrumentor()
instrumentor.instrument()

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
            logging.getLogger().info(f"About to process order: {order_data}")

            # Prepare the initial state for LangGraph
            state: GraphState = initial_state()

            state["order"] = order_data
            logging.getLogger().info(f"Invoking the graph")

            # Invoke the LangGraph application
            final_state = langgraph_app.invoke(state)

            logging.getLogger().info(f"final_state: {final_state}")

            if span:
                span.end()

            return final_state

    except Exception as e:
        # Log the error for debugging
        logging.getLogger().error(f"An error occurred: {e}")
        if span:
            span.record_exception(e)
            span.end()
        raise HTTPException(status_code=500, detail=f"Error processing order: {str(e)}")

@app.get("/get_orders_for_customer", response_model=List[OrderRequest], summary="Get orders for a specific customer")
async def get_orders_for_customer(customer_id: int):
    """
    Receives an HTTP GET request with a customer_id, and returns a list of orders for
    that customer.
    """
    try:
        with tracer.start_as_current_span("get_orders_for_customer") as span:
            logging.getLogger().info(f"About to get orders for customer_id: {customer_id}")

            fetch_orders_for_customer_args = FetchOrdersForCustomerArgs(customer_id=customer_id)

            # Call the synchronous function in a separate thread using asyncio.to_thread
            # This prevents blocking the event loop.
            orders = await asyncio.to_thread(fetch_orders_for_customer.func, fetch_orders_for_customer_args)

            if span:
                span.end()
            return orders

    except Exception as e:
        # Log the error for debugging
        logging.getLogger().error(f"An error occurred: {e}")
        if span:
            span.record_exception(e)
            span.end()
        raise HTTPException(status_code=500, detail=f"Error retrieving customers: {str(e)}")