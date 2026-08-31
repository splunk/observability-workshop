# Add Splunk Agent Observability Instrumentation

## Add Splunk Agent Observability Config

Edit the `.streamlit/secrets.toml` file and add your Galileo API key and console URL: 

```yaml
# API Keys
# -----------------------------------------------------------------------------
...
galileo_api_key = "..."  

# Galileo Configuration
# -----------------------------------------------------------------------------
# Console URL for your Galileo instance
galileo_console_url = "http://app.galileo.ai/" 
# Optional: omit to use Galileo's default project and log stream
galileo_project = "healthcare-assistant"
galileo_log_stream = "local"
```

## Read New Config

Update the [setup_env.py](./setup_env.py) file to ensure it populates 
the `GALILEO` environment variables: 

```python
        env_vars = {
            "OPENAI_API_KEY": secrets.get("openai_api_key", ""),
            "OPENAI_BASE_URL": secrets.get("openai_base_url", "https://api.openai.com/v1"),
            "GALILEO_API_KEY": secrets.get("galileo_api_key", ""),
            "GALILEO_CONSOLE_URL": secrets.get("galileo_console_url", ""),
            "GALILEO_PROJECT": secrets.get("galileo_project", ""),
            "GALILEO_LOG_STREAM": secrets.get("galileo_log_stream", ""),
            "POSTGRES_HOST": secrets.get("postgres_host", "localhost"),
            "POSTGRES_PORT": secrets.get("postgres_port", "5432"),
            "POSTGRES_USER": secrets.get("postgres_user", "postgres"),
            "POSTGRES_PASSWORD": secrets.get("postgres_password", ""),
            "POSTGRES_DB": secrets.get("postgres_db", "vectordb"),
            "ENVIRONMENT": secrets.get("environment", "local"),
        }
```

## Add Galileo Packages 

Open the [requirements.txt](./requirements.txt) file for editing. Add the following packages: 

````
galileo
````

## Add Instrumentation 

Open the [agent.py](./agent.py) file for editing. 

Add the following imports, at the end of the import section and before `class State(TypedDict)`: 

```python
import os
from galileo import galileo_context
from galileo.handlers.langchain import GalileoAsyncCallback
```

The initial definition of `_process_query_async` is as follows: 

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            self.langgraph_config,
        )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

Update it to use the `GalileoAsyncCallback` class as follows: 

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        with galileo_context(
            project=os.getenv("GALILEO_PROJECT"),
            log_stream=os.getenv("GALILEO_LOG_STREAM"),
        ):
            galileo_context.start_session(external_id=self.session_id)

            # One callback per request keeps each user turn in its own trace.
            callback = GalileoAsyncCallback()
            run_config = {**self.langgraph_config, "callbacks": [callback]}

            result = await self.graph.ainvoke(
                {"messages": langchain_messages},
                run_config,
            )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

## Troubleshooting 

If you need to troubleshoot instrumentation, add the following to the `agent.py` file: 

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```
