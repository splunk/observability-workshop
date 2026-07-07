"""Load secrets from .streamlit/secrets.toml and set environment variables."""
import os
from pathlib import Path

import toml


def setup_environment():
    """Load OpenAI and PostgreSQL settings from secrets.toml."""
    secrets_path = Path(".streamlit/secrets.toml")
    if not secrets_path.exists():
        secrets_path = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
    if not secrets_path.exists():
        print("⚠️  .streamlit/secrets.toml not found. Please create it with your API keys.")
        return

    try:
        secrets = toml.load(secrets_path)
        env_vars = {
            "OPENAI_API_KEY": secrets.get("openai_api_key", ""),
            "OPENAI_BASE_URL": secrets.get("openai_base_url", "https://api.openai.com/v1"),
            "GALILEO_API_KEY": secrets.get("galileo_api_key", ""),
            "GALILEO_CONSOLE_URL": secrets.get("galileo_console_url", ""),
            "GALILEO_API_URL": secrets.get("galileo_api_url", ""),
            "GALILEO_PROJECT": secrets.get("galileo_project", ""),
            "GALILEO_LOG_STREAM": secrets.get("galileo_log_stream", ""),
            "AGENT_CONTROL_URL": secrets.get("agent_control_url", ""),
            "AGENT_CONTROL_AGENT_NAME": secrets.get("agent_control_agent_name", ""),
            "AGENT_CONTROL_API_KEY_HEADER": secrets.get("agent_control_api_key_header", "Galileo-API-Key"),
            "AGENT_CONTROL_RUNTIME_AUTH_MODE": secrets.get("agent_control_runtime_auth_mode", "jwt"),
            "AGENT_CONTROL_TARGET_TYPE": secrets.get("agent_control_target_type", "log_stream"),
            "POSTGRES_HOST": secrets.get("postgres_host", "localhost"),
            "POSTGRES_PORT": secrets.get("postgres_port", "5432"),
            "POSTGRES_USER": secrets.get("postgres_user", "postgres"),
            "POSTGRES_PASSWORD": secrets.get("postgres_password", ""),
            "POSTGRES_DB": secrets.get("postgres_db", "vectordb"),
            "ENVIRONMENT": secrets.get("environment", "local"),
        }

        for key, value in env_vars.items():
            if value:
                os.environ[key] = str(value)
            else:
                print(f"⚠️  {key} not set (empty value)")

        print("🔧 Environment setup complete")
    except Exception as e:
        print(f"❌ Error loading secrets: {e}")


if __name__ == "__main__":
    setup_environment()
