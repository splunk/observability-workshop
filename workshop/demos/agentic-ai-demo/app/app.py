import logging
import asyncio

from typing import List, Dict, Optional, Any, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

from fastapi import FastAPI, HTTPException

# local
from config import Settings
from graph import build_graph
from models.schemas import AgentState
from agents.coordination_agent import coordinator_node
from tools.inventory_tool import restore_inventory
from tools.order_tool import archive_orders

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

instrumentor = LangchainInstrumentor()
instrumentor.instrument()

app = FastAPI(
    title="Dark Mode Coffee Agents API",
    description="API for submitting requests to Dark Mode Coffee agents.",
    version="1.0.0",
)

service_name = Settings.OTEL_SERVICE_NAME

# Initialize Traces
tracer = trace.get_tracer_provider().get_tracer(service_name)

langgraph_app = build_graph()

class ChatRequest(BaseModel):
    customer_id: int = Field(..., gt=0, description="Authenticated customer's ID.")
    request: str = Field(..., min_length=1, max_length=4000, description="User's request.")

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse, summary="Chat with the AI assistant")
async def chat(payload: ChatRequest) -> ChatResponse:
    """
    Receives a POST with customer_id and request. Calls the coordinator agent which
    routes the request to other agents as required, then returns an answer.
    """
    try:
        with tracer.start_as_current_span("chat") as span:
            span.set_attribute("customer_id", payload.customer_id)
            span.set_attribute("request.length", len(payload.request))

            logging.getLogger().info(
                f"Chat request: customer_id={payload.customer_id}, request={payload.request[:200]}..."
            )

            state = {
                "messages": [HumanMessage(content=payload.request)],
                "customer_id": payload.customer_id,
                "inventory_summary": None,
                "order_summary": None,
                "product_summary": None,
                "payment_summary": None,
                "final_answer": None,
                "fulfilled_by": None,
                "finalized_by_selector": False,
            }

            answer: AgentState = langgraph_app.invoke(state)
            logging.getLogger().info(f"Answer is: {answer}")

            # Prefer the single, selector-derived final answer when available.
            display = answer.get("final_answer")
            if not display:
                # Fallback to the last assistant message if the selector didn't produce a final answer.
                display = answer["messages"][-1].content

            return ChatResponse(answer=display)

    except Exception as e:
        logging.getLogger().exception("/chat request failed")
        # Let FastAPI produce a 500 response with a generic detail
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/refresh_inventory")
async def refresh_inventory():
    restore_inventory()
    return "success"

@app.get("/archive_orders")
async def archive_orders_endpoint():
    archive_orders()
    return "success"