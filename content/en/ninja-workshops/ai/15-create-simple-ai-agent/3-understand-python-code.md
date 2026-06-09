---
title: 3. Understand the Python Code
linkTitle: 3. Understand the Python Code
weight: 3
time: 10 minutes
---

Before editing the agent, review how the Python code is organized. The example is small,
but it uses the same building blocks as larger agent applications.

## Imports and Profile Path

At the top of the file, Python imports standard library modules only:

```python
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
```

These imports do the following:

* `json` reads `profile.json`.
* `os` reads backend and model configuration from environment variables.
* `sys` reads the request passed on the command line.
* `urllib` sends HTTP requests to the local or hosted model endpoint.
* `dataclass` creates small state objects with less boilerplate.
* `Path` builds a file path that works from any current directory.
* `Any` and `Callable` describe flexible tool inputs and callable tool functions.

The profile path is anchored to the Python file:

```python
PROFILE_PATH = Path(__file__).with_name("profile.json")
```

This means the script can find `profile.json` even if you run it from the repository root
or from inside `workshop/simple-ai-agent`.

## State Objects

The agent uses three small data classes:

```python
@dataclass
class Action:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
```

`Action` is the decision returned by the controller. It says which tool to call and which
arguments to pass.

```python
@dataclass
class Observation:
    tool_name: str
    result: str
```

`Observation` stores the result of one tool call. Keeping observations in state lets the
agent avoid repeating the same tool and lets the final answer explain what happened.

```python
@dataclass
class AgentState:
    request: str
    observations: list[Observation] = field(default_factory=list)
```

`AgentState` is the shared memory for one run. In this workshop, state contains the user
request and the tool observations. Larger agents often add conversation history,
retrieved documents, user identity, approvals, and trace identifiers.

## Profile Loading

The profile loader reads local JSON into a Python dictionary:

```python
def load_profile() -> dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
```

The return type is `dict[str, Any]` because profile values can be strings, lists, or other
JSON-compatible values. This keeps the exercise simple while still showing how an agent
can use external context.

## Tools

Tools are normal Python functions. For example:

```python
def lookup_profile(profile: dict[str, Any], section: str) -> str:
    value = profile.get(section, "unknown")
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)
```

This tool reads one section from the profile and returns a string. The agent does not
directly read `profile.json`; it asks a tool to do that work.

```python
def create_task(profile: dict[str, Any], title: str, priority: str = "medium") -> str:
    return f"Created {priority}-priority task for {profile['name']}: {title}"
```

This tool simulates task creation. In a real agent, this might call Jira, ServiceNow,
GitHub Issues, or another task system. In this workshop, it returns a string so the
exercise is safe and repeatable.

```python
def draft_message(profile: dict[str, Any], audience: str, topic: str) -> str:
    style = profile.get("communication_style", "clear and concise")
    return (
        f"Draft for {audience}: Here is a {style} update about {topic}. "
        "I will share current status, next action, and any decision needed."
    )
```

This tool uses the profile's communication style to draft text. It does not send the
message. Draft-only tools are a good beginner pattern because the human remains in
control of what gets shared.

## Tool Registry

The `TOOLS` dictionary maps tool names to Python functions:

```python
TOOLS = {
    "lookup_profile": lookup_profile,
    "create_task": create_task,
    "draft_message": draft_message,
}
```

This registry is an allowlist. If a tool is not in `TOOLS`, the agent cannot call it.
That makes the boundary of the agent explicit.

## Model Configuration

The agent uses Ollama by default:

```python
backend = os.getenv("AGENT_BACKEND", "ollama").strip().lower()
```

When `AGENT_BACKEND=ollama`, the default endpoint is:

```text
http://localhost:11434/v1
```

When `AGENT_BACKEND=openai`, the agent reads `OPENAI_API_KEY`, `OPENAI_MODEL`, and
optionally `OPENAI_BASE_URL`.

## Model Request

The `chat_completion` function sends an OpenAI-compatible request:

```python
payload = {
    "model": config.model,
    "messages": messages,
    "temperature": 0,
}
```

The model response is read from:

```python
data["choices"][0]["message"]["content"]
```

This keeps the local LLM path and hosted API path on the same request shape.

## Decision Function

`decide_next_action_with_model` is the controller:

```python
def decide_next_action_with_model(state: AgentState, config: ModelConfig) -> Action:
    content = chat_completion(config, build_decision_messages(state))
```

The function sends the request, observations, and tool descriptions to the model. The
model must return JSON describing the next action.

For example:

```json
{
  "tool_name": "lookup_profile",
  "arguments": {
    "section": "current_goals"
  }
}
```

Python parses that JSON into an `Action`.

When no more tools are needed, the controller returns:

```python
return Action("final_answer")
```

`final_answer` is not a tool. It is a sentinel value that tells the loop to stop and
build the response.

## Action Validation

The model does not get to call arbitrary code. `normalize_action` validates the requested
tool:

* `lookup_profile` can only read known profile sections.
* `create_task` receives a title and priority.
* `draft_message` receives an audience and topic.
* Unknown tools, repeated tools, and invalid final answers stop the run with a clear
  error.

## Agent Loop

`run_agent` connects the pieces:

```python
backend = get_backend()
model_config = get_model_config(backend)
profile = load_profile()
state = AgentState(request=request)
```

First, it chooses the backend, loads model configuration, loads profile context, and
creates state for this request.

```python
for _ in range(5):
    action = decide_next_action_with_model(state, model_config)
```

The loop has a maximum of five steps. Step limits are important because real agents can
otherwise get stuck calling tools repeatedly.

```python
if action.tool_name == "final_answer":
    return build_model_final_answer(state, model_config)
```

If the controller says the work is done, the loop returns the final answer.

```python
tool = TOOLS[action.tool_name]
observation = tool(profile, **action.arguments)
```

If more work is needed, the loop looks up the selected tool and calls it. The
`**action.arguments` syntax expands a dictionary into named function arguments. For
example:

```python
{"section": "current_goals"}
```

becomes:

```python
lookup_profile(profile, section="current_goals")
```

Finally, the observation is stored:

```python
state.observations.append(
    Observation(tool_name=action.tool_name, result=observation)
)
```

This is the agent's working memory for the current run.

## Command-Line Entry Point

The bottom of the file makes the script runnable:

```python
if __name__ == "__main__":
    user_request = " ".join(sys.argv[1:]) or "Plan my day and draft a customer follow-up"
    print(run_agent(user_request))
```

When you run `python3 agent.py "Plan my day"`, everything after the filename is
joined into one request string. If you do not pass a request, the script uses a default
example.
