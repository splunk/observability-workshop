---
title: 4. Add Tools
linkTitle: 4. Add Tools
weight: 4
time: 10 minutes
---

Open:

```text
workshop/simple-ai-agent/agent.py
```

The first task is to understand the tools the local LLM can request.

## Tool Contract

Each tool receives simple inputs and returns a string observation:

```python
def lookup_profile(profile: dict, section: str) -> str:
    ...
```

The agent does not need to know how the tool works internally. It only needs a stable
tool name, inputs, and an observation it can add to state.

In this exercise, every tool accepts `profile` as its first argument. That is a simple way
to give tools shared context without using global variables. The remaining arguments are
specific to the tool:

* `lookup_profile` needs a `section`, such as `current_goals`.
* `create_task` needs a `title` and optionally a `priority`.
* `draft_message` needs an `audience` and a `topic`.

## Register the Tools

Find the `TOOLS` dictionary and add the three provided tools:

```python
TOOLS = {
    "lookup_profile": lookup_profile,
    "create_task": create_task,
    "draft_message": draft_message,
}
```

This registry is the list of actions the agent is allowed to take.

The string keys matter. `decide_next_action` returns names such as `lookup_profile`, and
the loop uses those names to find the matching function in `TOOLS`. If the name returned
by the decision function is not registered, the script raises an error instead of calling
unknown code.

{{% notice title="Exercise" style="green" icon="running" %}}
Review the `TOOLS` registry in `agent.py`, then run:

```bash
python3 agent.py "Plan my day and draft a customer follow-up"
```

Confirm the model can request only the tools listed in `TOOLS`.
{{% /notice %}}

## What the Registry Protects

The registry is intentionally simple, but the pattern is important. A production agent
should never be able to call any function in the application process. It should only call
tools that were deliberately registered, reviewed, and instrumented.

## Tool Design Guidelines

Good agent tools are:

* **Specific**: one tool does one clear thing.
* **Typed**: inputs are predictable and easy to validate.
* **Observable**: each call can be logged, traced, and measured.
* **Bounded**: dangerous actions require approval or are not exposed to the agent.
