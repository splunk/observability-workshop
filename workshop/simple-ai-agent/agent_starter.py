from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


PROFILE_PATH = Path(__file__).with_name("profile.json")


@dataclass
class Action:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    tool_name: str
    result: str


@dataclass
class AgentState:
    request: str
    observations: list[Observation] = field(default_factory=list)


def load_profile() -> dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def lookup_profile(profile: dict[str, Any], section: str) -> str:
    value = profile.get(section, "unknown")
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def create_task(profile: dict[str, Any], title: str, priority: str = "medium") -> str:
    return f"Created {priority}-priority task for {profile['name']}: {title}"


def draft_message(profile: dict[str, Any], audience: str, topic: str) -> str:
    style = profile.get("communication_style", "clear and concise")
    return (
        f"Draft for {audience}: Here is a {style} update about {topic}. "
        "I will share current status, next action, and any decision needed."
    )


# TODO: register lookup_profile, create_task, and draft_message.
TOOLS: dict[str, Callable[..., str]] = {}


def decide_next_action(state: AgentState) -> Action:
    request = state.request.lower()
    used_tools = {observation.tool_name for observation in state.observations}

    if "lookup_profile" not in used_tools:
        section = "current_goals" if "plan" in request else "communication_style"
        return Action("lookup_profile", {"section": section})

    if ("task" in request or "plan" in request) and "create_task" not in used_tools:
        return Action(
            "create_task",
            {
                "title": "Prepare the next useful step for the request",
                "priority": "high",
            },
        )

    if (
        "draft" in request or "message" in request or "update" in request
    ) and "draft_message" not in used_tools:
        return Action(
            "draft_message",
            {
                "audience": "stakeholders",
                "topic": state.request,
            },
        )

    return Action("final_answer")


def build_final_answer(state: AgentState) -> str:
    lines = ["Final answer:"]
    lines.append(f"- Request: {state.request}")
    for observation in state.observations:
        lines.append(f"- {observation.tool_name}: {observation.result}")
    return "\n".join(lines)


def run_agent(request: str) -> str:
    profile = load_profile()
    state = AgentState(request=request)

    print(f"request: {request}")

    for _ in range(5):
        action = decide_next_action(state)
        if action.tool_name == "final_answer":
            return build_final_answer(state)

        if action.tool_name not in TOOLS:
            raise ValueError(f"Tool is not registered: {action.tool_name}")

        # TODO: call the selected tool, store the observation, and continue the loop.
        raise NotImplementedError("Add the tool call and observation logic here.")

    return "The agent stopped because it reached the maximum number of steps."


if __name__ == "__main__":
    user_request = " ".join(sys.argv[1:]) or "Plan my day and draft a customer follow-up"
    print(run_agent(user_request))
