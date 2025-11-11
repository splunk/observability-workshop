from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from models.schemas import OrderItem, Customer, GraphState, OrderRequest
from tools.order_tool import add_order_to_db

prompt = PromptTemplate.from_template(
    "Extract structured order details.\n\nUser message:\n{message}\n\nReturn JSON with fields: items[{sku, quantity}], customer{name, email, phone}."
)
parser = PydanticOutputParser(pydantic_object=Customer)

llm = ChatOpenAI(model="gpt-4o-mini")  # replace with your provider/model

def intake(state: GraphState) -> GraphState:

    order = state["order"]

    order_id = add_order_to_db.func(order)
    order.order_id = order_id

    return {"order": order, "order_intake": True, "next": "inventory"}

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