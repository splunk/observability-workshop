from pydantic import BaseModel, Field, EmailStr
from langchain.tools import tool

class NotificationInput(BaseModel):
    order_id: str = Field(..., min_length=1)
    channel: str = Field(..., pattern="^(email|sms)$")
    destination: str = Field(..., min_length=7)
    message: str = Field(..., min_length=1)

@tool("send_notification", args_schema=NotificationInput)
def send_notification(order_id: str, channel: str, destination: str, message: str) -> str:
    """Sends a notification to the user with the specified channel"""
    # Replace with provider SDK calls. Avoid logging PII in production.
    return f"notified:{channel}:{destination}:{order_id}"