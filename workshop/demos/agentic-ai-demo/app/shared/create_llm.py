from langchain_openai import ChatOpenAI
from config import Settings

def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> ChatOpenAI:
    """Create an LLM instance decorated with tags/metadata for tracing."""
    model = Settings.OPENAI_MODEL
    tags = [f"agent:{agent_name}", "agentic-ai-demo"]
    metadata = {
        "agent_name": agent_name,
        "agent_type": agent_name,
        "session_id": session_id,
        "thread_id": session_id,
        "ls_model_name": model,
        "ls_temperature": temperature,
    }
    return ChatOpenAI(
        api_key=Settings.OPENAI_API_KEY,
        model=model,
        temperature=temperature,
        tags=tags,
        metadata=metadata,
    )
