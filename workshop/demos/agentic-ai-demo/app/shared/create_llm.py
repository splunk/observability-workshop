import os
import logging

from langchain_openai import ChatOpenAI
from config import Settings
from shared.token_manager import TokenManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

use_cisco_api = Settings.USE_CISCO_API
cisco_client_id = Settings.CISCO_CLIENT_ID
cisco_client_secret = Settings.CISCO_CLIENT_SECRET
cisco_app_key = Settings.CISCO_APP_KEY

def init_token_manager():

    if not use_cisco_api or use_cisco_api=="false":
        logging.getLogger().info(
           "USE_CISCO_API is set to False; using OPENAI APIs instead."
        )
        return None

    token_manager = None

    if not all([cisco_client_id, cisco_client_secret, cisco_app_key]):
        logging.getLogger().error(
           "ERROR: Missing Cisco credentials. Please set CISCO_CLIENT_ID, CISCO_CLIENT_SECRET, and CISCO_APP_KEY environment variables."
        )
    else:
        token_manager = TokenManager(
            cisco_client_id, cisco_client_secret, cisco_app_key
        )
        return token_manager

cisco_token_manager = init_token_manager()

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

    if cisco_token_manager is None:
        return ChatOpenAI(
            api_key=Settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature,
            tags=tags,
            metadata=metadata,
        )
    else:
        cisco_access_token = cisco_token_manager.get_token()

        return ChatOpenAI(
            api_key="dummy-key",
            base_url="https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini",
            model="gpt-4o-mini",
            temperature=temperature,
            tags=tags,
            metadata=metadata,
            default_headers={"api-key": cisco_access_token},
            model_kwargs={"user": f'{{"appkey": "{cisco_app_key}"}}'},
        )
