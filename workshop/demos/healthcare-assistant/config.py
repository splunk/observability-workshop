"""Load healthcare app configuration from YAML and JSON files."""
from pathlib import Path

import yaml

APP_ROOT = Path(__file__).resolve().parent
DOMAIN = "healthcare"
CONFIG_PATH = APP_ROOT / "config.yaml"
SYSTEM_PROMPT_PATH = APP_ROOT / "system_prompt.json"
DOCS_DIR = APP_ROOT / "../docs"
TOOLS_DIR = APP_ROOT / "tools"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt() -> str:
    import json

    with SYSTEM_PROMPT_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["system_prompt"]
