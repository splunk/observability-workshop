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

Change the working directory and activate a virtual environment:

```bash
cd ~/workshop/healthcare-assistant/2-app-with-instrumentation
python3 -m venv venv
source venv/bin/activate
```

{{< /step >}}

{{< step title="Add the Galileo package" >}}

Galileo's LangChain callback ships in the `galileo` package. Open the `~/workshop/healthcare-assistant/2-app-with-instrumentation/requirements.txt` 
file for editing and add `galileo` as the last line of the file. 

Then install the dependencies:

```bash
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Add Galileo configuration to secrets" >}}

Next, we need to add the Galileo configuration to the `secrets.toml` file, to tell Galileo 
which environment to send traces to. 

Make a copy of the `secrets.toml` file we used in the previous step of the workshop: 

```bash
cp ../1-base-app/.streamlit/secrets.toml ./.streamlit/secrets.toml
```

Next, open the `~/workshop/healthcare-assistant/2-app-with-instrumentation/.streamlit/secrets.toml` 
file for editing and add the Galileo API key and configuration provided by the workshop instructor to 
the top of the file: 

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

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you comment out `galileo_project` and `galileo_log_stream` in `secrets.toml`. Where will
your traces show up?

{{< details summary="Click here to see the answer" >}}
In a project named `default` and a log stream named `default`. With those keys empty,
`setup_env.py` exports empty `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` values, and the Galileo
SDK falls back to its built-in `default` project and `default` log stream.
{{< /details >}}
