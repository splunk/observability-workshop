"""Validate required environment variables are set."""
import os

REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "ENVIRONMENT",
    "SPLUNK_AO_PROJECT",
    "SPLUNK_AO_AGENT_STREAM",
]

# O11y deployment requires REALM + token; standalone requires API_KEY + console URL.
SPLUNK_AO_O11Y_VARS = ["SPLUNK_AO_REALM", "SPLUNK_AO_O11Y_TOKEN"]
SPLUNK_AO_STANDALONE_VARS = ["SPLUNK_AO_API_KEY", "SPLUNK_AO_CONSOLE_URL"]

def setup_environment():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    for var in missing:
        print(f"⚠️  {var} not set")

    has_o11y = all(os.getenv(v) for v in SPLUNK_AO_O11Y_VARS)
    has_standalone = all(os.getenv(v) for v in SPLUNK_AO_STANDALONE_VARS)
    if not has_o11y and not has_standalone:
        print(f"⚠️  Set either {SPLUNK_AO_O11Y_VARS} (O11y) or {SPLUNK_AO_STANDALONE_VARS} (standalone)")

    if not missing and (has_o11y or has_standalone):
        print("🔧 Environment setup complete")


if __name__ == "__main__":
    setup_environment()
