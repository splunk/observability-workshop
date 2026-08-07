"""Validate required environment variables are set."""
import os

REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "OPENAI_BASE_URL",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "ENVIRONMENT",
]


def setup_environment():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    for var in missing:
        print(f"⚠️  {var} not set")
    if not missing:
        print("🔧 Environment setup complete")


if __name__ == "__main__":
    setup_environment()
