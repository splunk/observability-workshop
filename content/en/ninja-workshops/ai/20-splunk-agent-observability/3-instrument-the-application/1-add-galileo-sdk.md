---
title: Add the Galileo SDK and Configuration
linkTitle: 1. Add the Galileo SDK
weight: 1
time: 5 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm the `galileo_console_url` and `galileo_project` that should be used for this workshop.
Will each user create a separate project or should the project be shared?
{{% /notice %}}

First, add the Galileo package and the configuration the SDK needs to know *where* to send
traces.

{{< exercise title="Add the SDK and configuration" >}}

{{< step title="Activate the environment" >}}

Change into the instrumentation stage and activate a virtual environment:

```bash
cd ~/workshop/healthcare-assistant/2-app-with-instrumentation
python3 -m venv venv
source venv/bin/activate
```

{{< /step >}}

{{< step title="Add the Galileo package" >}}

Galileo's LangChain callback ships in the `galileo` package. Confirm it's listed in
`requirements.txt`:

```bash
cat ~/workshop/healthcare-assistant/2-app-with-instrumentation/requirements.txt
```

You should see the `galileo` package included in the output.

Then install the dependencies:

```bash
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Add Galileo configuration to secrets" >}}

Copy the template if you haven't already, then add your Galileo settings to
`.streamlit/secrets.toml`:

```toml
# API Keys
# -----------------------------------------------------------------------------
galileo_api_key = "your-galileo-api-key"

# Galileo Configuration
# -----------------------------------------------------------------------------
# Console URL for your Galileo instance
galileo_console_url = "https://console.multitenant.galileocloud.io"
# Optional: omit to use Galileo's default project and log stream
galileo_project = "healthcare-assistant"
galileo_log_stream = "local"
```

{{% notice title="Project and log stream" style="info" %}}

`galileo_project` and `galileo_log_stream` decide where your traces appear in the Galileo
console. If you leave them blank, the SDK falls back to a project and log stream both named
`default`. For a shared workshop, consider suffixing the log stream with your instance name
(for example, `local-shw-1234`) so your traces are easy to find.

{{% /notice %}}

{{< /step >}}

{{< step title="Expose the Galileo variables to the app" >}}

The app loads secrets into environment variables in `setup_env.py`. Confirm the `env_vars`
dictionary includes the `GALILEO_*` entries so the SDK can read them:

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

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you comment out `galileo_project` and `galileo_log_stream` in `secrets.toml`. Where will
your traces show up?

{{< details summary="Click here to see the answer" >}}
In a project named `default` and a log stream named `default`. With those keys empty,
`setup_env.py` exports empty `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` values, and the Galileo
SDK falls back to its built-in `default` project and `default` log stream.
{{< /details >}}
