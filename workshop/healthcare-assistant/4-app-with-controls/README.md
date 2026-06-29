# Add Agent Controls

## Add Agent Control Config

Edit the `.streamlit/secrets.toml` file and add the following environment variables: 

> Note: update the URL and agent name as appropriate for your environment 

```yaml
# Agent Controls
# -----------------------------------------------------------------------------
agent_control_url = "https://console.multitenant.galileocloud.io/api/agent-control" 
agent_control_agent_name = "agent-control-example"
agent_control_runtime_auth_mode="jwt"
agent_control_api_key_header = "Galileo-API-Key"
agent_control_target_type="log_stream"
```

## Read New Config

Update the [setup_env.py](./setup_env.py) file to ensure it populates 
the `AGENT_CONTROL` environment variables: 

```python
        env_vars = {
            "OPENAI_API_KEY": secrets.get("openai_api_key", ""),
            "OPENAI_BASE_URL": secrets.get("openai_base_url", "https://api.openai.com/v1"),
            "GALILEO_API_KEY": secrets.get("galileo_api_key", ""),
            "GALILEO_CONSOLE_URL": secrets.get("galileo_console_url", ""),
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

## Add Agent Control Packages 

Open the [requirements.txt](./requirements.txt) file for editing. Add the following packages: 

````
agent-control-sdk[galileo]>=7.10.0
agent-control-evaluators>=7.10.0
agent-control-evaluator-galileo>=7.10.0
````

## Add Agent Control Code 

Open the [agent.py](./agent.py) file for editing. 

Add the following imports, at the end of the import section and before `class State(TypedDict)`: 

```python
from agent_control import ControlSteerError, ControlViolationError, control
```


## Troubleshooting 

If you need to troubleshoot, add the following to the `agent.py` file: 

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```
