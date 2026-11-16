"""Single source of truth for the three Agent Observability targets.

Each target is backed by ConfigMaps/Secrets that already exist in the cluster
(see README.md). The orchestrator reads this map to decide which env sources to
mount on a back-end pod; the front-end reads it to render the target picker.

Keep this in sync with the cluster objects — nothing else should hard-code
target-specific config map / secret names.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Target:
    key: str                      # stable id used in URLs / pod names
    label: str                    # human label for the UI picker
    config_maps: list[str]        # target-specific ConfigMaps (envFrom)
    secret_name: str              # target-specific Secret holding the auth credential
    auth_env: str                 # env var the app reads the credential from
    auth_secret_key: str          # key within secret_name holding the credential


# Config maps/secrets shared by every back-end regardless of target.
COMMON_CONFIG_MAPS: list[str] = ["healthcare-assistant-config", "postgres-config"]

TARGETS: dict[str, Target] = {
    "standalone": Target(
        key="standalone",
        label="Standalone Agent Observability",
        config_maps=["splunk-ao-config", "splunk-agent-control-config"],
        secret_name="splunk-ao-secret",
        auth_env="SPLUNK_AO_API_KEY",
        auth_secret_key="SPLUNK_AO_API_KEY",
    ),
    "us-splunk-show": Target(
        key="us-splunk-show",
        label="US Splunk Show (o11y Cloud)",
        config_maps=[
            "splunk-ao-config-us-splunk-show",
            "splunk-agent-control-config-us-splunk-show",
        ],
        secret_name="splunk-ao-secret-us-splunk-show",
        auth_env="SPLUNK_AO_O11Y_TOKEN",
        auth_secret_key="SPLUNK_AO_O11Y_TOKEN",
    ),
    "eu-splunk-show": Target(
        key="eu-splunk-show",
        label="EU Splunk Show (o11y Cloud)",
        config_maps=[
            "splunk-ao-config-eu-splunk-show",
            "splunk-agent-control-config-eu-splunk-show",
        ],
        secret_name="splunk-ao-secret-eu-splunk-show",
        auth_env="SPLUNK_AO_O11Y_TOKEN",
        auth_secret_key="SPLUNK_AO_O11Y_TOKEN",
    ),
}

DEFAULT_TARGET = "standalone"


def get_target(key: str) -> Target:
    if key not in TARGETS:
        raise KeyError(f"Unknown target '{key}'. Valid targets: {sorted(TARGETS)}")
    return TARGETS[key]
