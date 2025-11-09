from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from models.schemas import OrderItem, Customer, GraphState

prompt = PromptTemplate.from_template(
    "Extract structured order details.\n\nUser message:\n{message}\n\nReturn JSON with fields: items[{sku, quantity}], customer{name, email, phone}."
)
parser = PydanticOutputParser(pydantic_object=Customer)

llm = ChatOpenAI(model="gpt-4o-mini")  # replace with your provider/model

def intake(state: GraphState) -> GraphState:
    # Either use provided structured data or LLM extraction from messages.
    msg = next((m.content for m in state.get("messages", []) if m.role == "user"), "")
    if state.get("items") and state.get("customer"):
        return {"next": "inventory"}
    if not msg:
        return {"error": "No user message with order details.", "next": "notify"}
    # Minimal demo parsing: In production, use robust parsing and validation.
    # Here we simulate extracted data for clarity.
    items = [OrderItem(sku="SKU-001", quantity=1)]
    customer = Customer(name="Jane Doe", email="jane@example.com", phone="+12065550123")
    return {"items": items, "customer": customer, "next": "inventory"}

def payment(state: GraphState) -> GraphState:
    from tools.payment_tool import process_payment
    amount = 1000  # compute from items; placeholder
    payment_result = process_payment.invoke({
        "order_id": state.get("order_id", "order-unknown"),
        "amount_cents": amount,
        "currency": "USD",
        "payment_method_token": "tok_demo_OK",
    })
    next_step = "fulfillment" if payment_result.status in ("authorized", "captured") else "notify"
    return {"payment": payment_result, "next": next_step}