"""Load healthcare app configuration from YAML and JSON files."""
import os
from pathlib import Path
from typing import Any

import yaml

APP_ROOT = Path(__file__).resolve().parent
DOMAIN = "healthcare"
CONFIG_PATH = APP_ROOT / "config.yaml"
SYSTEM_PROMPT_PATH = APP_ROOT / "system_prompt.json"
DOCS_DIR = APP_ROOT / "docs"
TOOLS_DIR = APP_ROOT / "tools"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt() -> str:
    import json

    with SYSTEM_PROMPT_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["system_prompt"]


def create_chat_llm(model: str, temperature: float = 0.1, **kwargs: Any):
    """Return AzureChatOpenAI when AZURE_OPENAI_ENDPOINT is set, otherwise ChatOpenAI."""
    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_deployment=model,
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            temperature=temperature,
            **kwargs,
        )
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model, temperature=temperature, **kwargs)


def create_embeddings(model: str):
    """Return AzureOpenAIEmbeddings when AZURE_OPENAI_ENDPOINT is set, otherwise OpenAIEmbeddings."""
    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        from langchain_openai import AzureOpenAIEmbeddings
        return AzureOpenAIEmbeddings(
            azure_deployment=os.environ.get("AZURE_EMBEDDING_DEPLOYMENT", model),
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        )
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(model=model)
