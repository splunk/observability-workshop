from typing import List
from langchain_openai import ChatOpenAI
from models.schemas import GraphState, Message

# Safe defaults; add toggles to demonstrate issues in a controlled, non-harmful way.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def chat(state: GraphState) -> GraphState:
    messages: List[Message] = state.get("messages", [])
    if not messages:
        return {"next": "end"}
    # A basic chat turn; consider retrieval or guardrails for production.
    user = next((m.content for m in messages[::-1] if m.role == "user"), "")
    answer = f"I received: {user}. (Demo response; do not rely on this for factual information.)"
    new_messages = messages + [Message(role="assistant", content=answer)]
    return {"messages": new_messages, "next": "end"}