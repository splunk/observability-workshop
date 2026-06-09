from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


PROFILE_PATH = Path(__file__).with_name("profile.json")
DEFAULT_REQUEST = "Plan my day and draft a customer follow-up"
SUPPORTED_BACKENDS = {"ollama", "openai", "api"}
PROFILE_SECTIONS = {
    "name",
    "role",
    "current_goals",
    "communication_style",
    "working_hours",
}


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


@dataclass
class ModelConfig:
    backend: str
    base_url: str
    model: str
    api_key: str | None = None


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


TOOLS: dict[str, Callable[..., str]] = {
    "lookup_profile": lookup_profile,
    "create_task": create_task,
    "draft_message": draft_message,
}


def get_backend() -> str:
    backend = os.getenv("AGENT_BACKEND", "ollama").strip().lower()
    if backend not in SUPPORTED_BACKENDS:
        supported = ", ".join(sorted(SUPPORTED_BACKENDS))
        raise ValueError(f"Unsupported AGENT_BACKEND '{backend}'. Use one of: {supported}")
    return "openai" if backend == "api" else backend


def get_model_config(backend: str) -> ModelConfig:
    if backend == "ollama":
        return ModelConfig(
            backend=backend,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            api_key=os.getenv("OLLAMA_API_KEY") or None,
        )

    if backend == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")
        if not api_key:
            raise RuntimeError("Set OPENAI_API_KEY before using AGENT_BACKEND=openai.")
        if not model:
            raise RuntimeError("Set OPENAI_MODEL to a model available to your API key.")
        return ModelConfig(
            backend=backend,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            model=model,
            api_key=api_key,
        )

    raise ValueError(f"Backend '{backend}' does not use a model config.")


def chat_completion(config: ModelConfig, messages: list[dict[str, str]]) -> str:
    url = f"{config.base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": 0,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    timeout = float(os.getenv("AGENT_MODEL_TIMEOUT", "45"))

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Model request failed with HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach model endpoint {url}: {exc}") from exc

    data = json.loads(response_body)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected model response: {response_body}") from exc


def action_from_json(text: str) -> Action:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError(f"Model did not return JSON: {text}")
        payload = json.loads(text[start : end + 1])

    tool_name = payload.get("tool_name")
    arguments = payload.get("arguments", {})

    if not isinstance(tool_name, str):
        raise ValueError(f"Model action is missing tool_name: {payload}")
    if not isinstance(arguments, dict):
        raise ValueError(f"Model action arguments must be an object: {payload}")

    return Action(tool_name=tool_name, arguments=arguments)


def normalize_action(action: Action, state: AgentState) -> Action:
    used_tools = {observation.tool_name for observation in state.observations}

    if action.tool_name == "final_answer":
        if state.observations:
            return Action("final_answer")
        raise ValueError("Model asked for final_answer before calling any tools.")

    if action.tool_name in used_tools:
        raise ValueError(f"Model repeated tool: {action.tool_name}")

    if action.tool_name == "lookup_profile":
        section = str(action.arguments.get("section", "current_goals"))
        if section not in PROFILE_SECTIONS:
            section = "current_goals"
        return Action("lookup_profile", {"section": section})

    if action.tool_name == "create_task":
        title = str(
            action.arguments.get("title")
            or "Prepare the next useful step for the request"
        )
        priority = str(action.arguments.get("priority") or "medium")
        return Action("create_task", {"title": title, "priority": priority})

    if action.tool_name == "draft_message":
        audience = str(action.arguments.get("audience") or "stakeholders")
        topic = str(action.arguments.get("topic") or state.request)
        return Action("draft_message", {"audience": audience, "topic": topic})

    raise ValueError(f"Model requested an unknown tool: {action.tool_name}")


def build_decision_messages(state: AgentState) -> list[dict[str, str]]:
    observations = [
        {"tool_name": observation.tool_name, "result": observation.result}
        for observation in state.observations
    ]
    prompt_data = {
        "request": state.request,
        "observations": observations,
        "available_tools": {
            "lookup_profile": {
                "description": "Read one section from the user profile.",
                "arguments": {"section": "current_goals"},
            },
            "create_task": {
                "description": "Create a draft task for the user.",
                "arguments": {
                    "title": "Task title",
                    "priority": "low, medium, or high",
                },
            },
            "draft_message": {
                "description": "Draft a message but do not send it.",
                "arguments": {
                    "audience": "Message audience",
                    "topic": "Message topic",
                },
            },
            "final_answer": {
                "description": "Stop when enough context has been collected.",
                "arguments": {},
            },
        },
    }

    system = (
        "You are the decision controller for a small AI agent. Choose exactly one "
        "next action. Return only a JSON object with this schema: "
        '{"tool_name": "tool_or_final_answer", "arguments": {}}. '
        "Use only the listed tool names. Do not repeat tools already present in "
        "observations. Before the final answer, use lookup_profile at least once. "
        "For planning or task requests, use create_task. For draft, message, "
        "update, or follow-up requests, use draft_message."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(prompt_data, indent=2)},
    ]


def decide_next_action_with_model(state: AgentState, config: ModelConfig) -> Action:
    content = chat_completion(config, build_decision_messages(state))
    try:
        return normalize_action(action_from_json(content), state)
    except ValueError as exc:
        raise RuntimeError(f"Model returned an invalid next action: {exc}") from exc


def build_model_final_answer(state: AgentState, config: ModelConfig) -> str:
    observations = [
        {"tool_name": observation.tool_name, "result": observation.result}
        for observation in state.observations
    ]
    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise work assistant. Use the tool observations to "
                "answer the user. Mention drafted tasks or messages clearly. Do "
                "not claim that external systems were updated beyond the provided "
                "observations."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {"request": state.request, "observations": observations},
                indent=2,
            ),
        },
    ]
    return chat_completion(config, messages).strip()


def run_agent(request: str) -> str:
    backend = get_backend()
    model_config = get_model_config(backend)
    profile = load_profile()
    state = AgentState(request=request)
    max_steps = int(os.getenv("AGENT_MAX_STEPS", "5"))

    print(f"backend: {backend}")
    print(f"request: {request}")

    for _ in range(max_steps):
        action = decide_next_action_with_model(state, model_config)

        if action.tool_name == "final_answer":
            return build_model_final_answer(state, model_config)

        if action.tool_name not in TOOLS:
            raise ValueError(f"Tool is not registered: {action.tool_name}")

        tool = TOOLS[action.tool_name]
        observation = tool(profile, **action.arguments)
        state.observations.append(
            Observation(tool_name=action.tool_name, result=observation)
        )

        print(f"tool: {action.tool_name}({action.arguments})")
        print(f"observation: {observation}")

    return "The agent stopped because it reached the maximum number of steps."


if __name__ == "__main__":
    user_request = " ".join(sys.argv[1:]) or DEFAULT_REQUEST
    print(run_agent(user_request))
