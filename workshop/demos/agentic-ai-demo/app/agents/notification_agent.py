from models.schemas import GraphState
from tools.notification_service import send_notification

def notify(state: GraphState) -> GraphState:
    customer = state.get("customer")
    order_id = state.get("order_id", "order-unknown")
    message = build_message(state)
    receipts = []
    if customer and customer.email:
        receipts.append(send_notification.invoke({"order_id": order_id, "channel": "email", "destination": customer.email, "message": message}))
    if customer and customer.phone:
        receipts.append(send_notification.invoke({"order_id": order_id, "channel": "sms", "destination": customer.phone, "message": message}))
    notifications = state.get("notifications", [])
    notifications.extend(receipts)
    return {"notifications": notifications, "next": "end"}

def build_message(state: GraphState) -> str:
    if state.get("error"):
        return f"We encountered an issue with your order: {state['error']}."
    if state.get("fulfillment") and state["fulfillment"].status == "ready_for_pickup":
        return "Your order is ready for pickup."
    if state.get("fulfillment") and state["fulfillment"].status == "out_for_delivery":
        return "Your order is out for delivery."
    if state.get("payment") and state["payment"].status == "declined":
        return "Your payment was declined. Please update your payment method."
    return "We are processing your order."