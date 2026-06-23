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
            "GALILEO_PROJECT": secrets.get("galileo_project", ""),
            "GALILEO_LOG_STREAM": secrets.get("galileo_log_stream", ""),
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
