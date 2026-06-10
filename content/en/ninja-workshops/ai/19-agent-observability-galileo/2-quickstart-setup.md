---
title: Quickstart Setup
linkTitle: 2. Quickstart Setup
weight: 2
time: 5 minutes
---

Start by adding the Galileo SDK to the travel planner's environment and initializing Galileo tracing.

{{< exercise title="Quickstart setup" >}}

{{< step title="Activate Environment"  >}}

Navigate to the app directory and create a new virtual environment:

```bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
```

{{< /step >}}

{{< step title="Install Galileo SDK"  >}}

The app already installs `langchain`, `langchain-openai`, `langgraph`, and `flask` via its
`requirements.txt`. Galileo's LangChain callback ships with the `galileo` package, so 
let's add it here. 

Open the `~/workshop/agentic-ai/base-app/requirements.txt` file for editing 
and add the following packages: 

```bash
galileo
python-dotenv
```

Then add all of the packages to the virtual environment: 

```bash
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Configure Galileo credentials"  >}}

Your EC2 instance comes pre-configured with `OPENAI_API_KEY` and 
`OPENAI_BASE_URL` environment variables, which will be used by the application. 

To define additional environment variables, create a new file named
`~/workshop/agentic-ai/base-app/.env` and add your credentials: 

```ini
GALILEO_API_KEY="your-galileo-api-key"
GALILEO_CONSOLE_URL="https://console.multitenant.galileocloud.io"
# If you comment out the next two uncommented lines, Galileo uses a project and log
# stream both named "default".
GALILEO_PROJECT="Workshop19Galileo"
GALILEO_LOG_STREAM="TravelPlanner-${INSTANCE}"
```

{{< /step >}}

{{< step title="Initialize Galileo in the app"  >}}
Initialize Galileo near the top of `~/workshop/agentic-ai/base-app/main.py`, right before `import logging`. Passing the environment variables through means the project and log stream come from your `.env` when set, and fall back to Galileo's `default`/`default` when not:

```python
import os
from dotenv import load_dotenv
from galileo import galileo_context

load_dotenv()

galileo_context.init(project=os.getenv("GALILEO_PROJECT"),
                     log_stream=os.getenv("GALILEO_LOG_STREAM"))
```

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

If you comment out the `GALILEO_PROJECT` and `GALILEO_LOG_STREAM` variables in your `.env`, where will
your traces show up in Galileo?

{{< details summary="Click here to see the answer" >}}
They'll land in a project named `default` and a log stream named `default`. Because `main.py`
passes `os.getenv("GALILEO_PROJECT")` and `os.getenv("GALILEO_LOG_STREAM")`, those values are
`None` when the variables are unset, and the Galileo SDK falls back to its built-in `default`
project and `default` log stream.
{{< /details >}}
