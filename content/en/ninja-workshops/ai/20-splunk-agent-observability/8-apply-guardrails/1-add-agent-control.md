---
title: Add Agent Control to the App
linkTitle: 1. Add Agent Control to the App
weight: 1
time: 8 minutes
---

First, wire the Agent Control SDK into the app: add the configuration, install the packages,
and register the controllable steps.

{{< exercise title="Add Agent Control" >}}

{{< step title="Set up the environment" >}}

Change into the controls stage and activate a virtual environment:

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
python3 -m venv venv
source venv/bin/activate
```

{{< /step >}}

{{< step title="Add Agent Control configuration to secrets" >}}

Add the Agent Control settings to `.streamlit/secrets.toml` (in addition to your existing
OpenAI, PostgreSQL, and Galileo settings). Note the additional `galileo_api_url` used by the
control runtime:

```toml
# Galileo Configuration
# -----------------------------------------------------------------------------
galileo_console_url = "https://console.multitenant.galileocloud.io"
galileo_api_url = "https://api.multitenant.galileocloud.io"
galileo_project = "healthcare-assistant"
galileo_log_stream = "local"

# Agent Controls
# -----------------------------------------------------------------------------
agent_control_url = "https://console.multitenant.galileocloud.io/api/agent-control"
agent_control_agent_name = "agent-control-example"
agent_control_runtime_auth_mode = "jwt"
agent_control_api_key_header = "Galileo-API-Key"
agent_control_target_type = "log_stream"
```

{{% notice title="Match your environment" style="tip" icon="exclamation-triangle" %}}

Update `agent_control_url` and `agent_control_agent_name` to match your environment. The
`agent_control_agent_name` you set here must match the agent you create in the Galileo
console in the next section.

{{% /notice %}}

{{< /step >}}

{{< step title="Expose the new variables to the app" >}}

Confirm `setup_env.py` populates the `GALILEO_API_URL` and `AGENT_CONTROL_*` variables:

```python
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
```

{{< /step >}}

{{< step title="Add the Agent Control packages" >}}

Confirm `requirements.txt` includes the Agent Control SDK and the Galileo evaluators, then
install:

```text
agent-control-sdk[galileo]>=7.10.0
agent-control-evaluators>=7.10.0
agent-control-evaluator-galileo>=7.10.0
```

```bash
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Add the imports and decorate the steps" >}}

In `agent.py`, add the Agent Control imports at the end of the import section, before
`class State(TypedDict)`:

```python
from agent_control import ControlSteerError, ControlViolationError, control
```

The controls stage uses these in three places (already wired up in this folder):

* The LLM call is wrapped with `@control(step_name=LLM_STEP_NAME)`, where
  `LLM_STEP_NAME = "Healthcare Assistant"`, so the model's responses can be evaluated,
  blocked, or steered.
* Each tool is registered as a controllable step (`get_patient_info`,
  `delete_patient_record`, and a shared `retrieval_step` for search tools) via the helpers in
  `helpers/agent_control_helpers.py`.
* The agent enables control spans on the Galileo logger
  (`galileo_logger.enable_agent_control()`) and registers the steps with `init_agent_control(...)`
  so the console knows which steps exist for this agent.

{{% notice title="How block and steer are handled in code" style="info" %}}

When a control fires, the SDK raises an exception that the agent catches:

* `ControlViolationError` → the step is **blocked**; the user gets a friendly blocked
  message.
* `ControlSteerError` → the step is **steered**; the agent rebuilds the prompt with the
  steering guidance and retries (up to `MAX_STEER_RETRIES`) before falling back to a safe
  message.

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{% notice title="Troubleshooting" style="tip" icon="exclamation-triangle" %}}

To see what Agent Control is doing, enable console logging in `agent.py`:

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

Watch the terminal for `Agent Control initialized` on startup and `BLOCKED` / `STEERED`
messages when a control fires.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

What's the difference between how the app handles a `ControlViolationError` and a
`ControlSteerError`?

{{< details summary="Click here to see the answer" >}}
A `ControlViolationError` **blocks** the step: the action is stopped and the user receives a
friendly blocked message. A `ControlSteerError` **steers** the step: the agent retries with
the steering guidance appended to the prompt (up to a few attempts) to produce a corrected
response, only falling back to a safe message if it still can't comply.
{{< /details >}}
