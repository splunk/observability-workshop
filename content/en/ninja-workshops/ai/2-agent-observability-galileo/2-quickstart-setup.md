---
title: Quickstart Setup
linkTitle: 2. Quickstart Setup
weight: 2
time: 5 minutes
---

Start by adding the Galileo SDK to the travel planner's environment and initializing Splunk Agent Observability tracing.

{{< exercise title="Quickstart setup" >}}

{{< step title="Activate Environment"  >}}

Navigate to the app directory and activate the virtual environment you created in [Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) (or create a fresh one):

```bash
cd ~/workshop/agentic-ai/base-app
source .venv/bin/activate
```

{{< /step >}}

{{< step title="Install Galileo SDK"  >}}

Install the Galileo SDK alongside the app's existing dependencies:

```bash
pip install galileo python-dotenv
```

The app already installs `langchain`, `langchain-openai`, `langgraph`, and `flask` via its
`requirements.txt`. The Galileo LangChain callback ships with the `galileo` package.

{{< /step >}}

{{< step title="Configure Galileo credentials"  >}}

Add your credentials to the app's `.env` file.

```ini
OPENAI_API_KEY="your-openai-api-key"
OPENAI_BASE_URL="https://lite-llm-proxy.splunko11y.com/v1"
GALILEO_API_KEY="your-galileo-api-key"
GALILEO_CONSOLE_URL="https://console.multitenant.galileocloud.io"
# Recommended: uncomment to group this workshop's traces under their own project
# and log stream. If you leave these commented out, Splunk Agent Observability uses a project and log
# stream both named "default".
# GALILEO_PROJECT="Workshop19"
# GALILEO_LOG_STREAM="TravelPlanner"
```

Uncommenting `GALILEO_PROJECT` and `GALILEO_LOG_STREAM` keeps the workshop traces easy to find.
Leaving them commented is fine too — your traces will just land in the `default` project and
`default` log stream.

4. Initialize Splunk Agent Observability near the top of `main.py`, right after the existing imports and
   `load_dotenv()` call. Passing the environment variables through means the project and log
   stream come from your `.env` when set, and fall back to Splunk Agent Observability's `default`/`default` when not:

```python
import os
from galileo import galileo_context

galileo_context.init(project=os.getenv("GALILEO_PROJECT"),
                     log_stream=os.getenv("GALILEO_LOG_STREAM"))
```

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you leave `GALILEO_PROJECT` and `GALILEO_LOG_STREAM` commented out in your `.env`, where will
your traces show up in Splunk Agent Observability?

{{< details summary="Click here to see the answer" >}}
They'll land in a project named `default` and a log stream named `default`. Because `main.py`
passes `os.getenv("GALILEO_PROJECT")` and `os.getenv("GALILEO_LOG_STREAM")`, those values are
None` when the variables are unset, and the Galileo SDK falls back to its built-in `default`
project and `default` log stream.
{{< /details >}}
