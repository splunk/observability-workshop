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

Change into the agent controls folder: 

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
```

{{< /step >}}

{{< step title="Create an Agent Control Config Map" >}}

Run the following command to create a Kubernetes config map, which the application will use to
configure Agent Controls:

```bash
kubectl create configmap galileo-agent-control-config \
  --from-literal=GALILEO_API_URL="https://api.multitenant.galileocloud.io" \
  --from-literal=AGENT_CONTROL_URL="https://console.multitenant.galileocloud.io/api/agent-control" \
  --from-literal=AGENT_CONTROL_AGENT_NAME="agent-control-example" \
  --from-literal=AGENT_CONTROL_API_KEY_HEADER="Galileo-API-Key" \
  --from-literal=AGENT_CONTROL_RUNTIME_AUTH_MODE="jwt" \
  --from-literal=AGENT_CONTROL_TARGET_TYPE="log_stream"
```

{{< /step >}}

{{< step title="Add the Agent Control packages" >}}

Confirm `requirements.txt` includes the Agent Control SDK and evaluators:

```text
agent-control-sdk[galileo]>=7.10.0
agent-control-evaluators>=7.10.0
agent-control-evaluator-galileo>=7.10.0
```

{{% notice title="Note about the SDK" style="info" %}}

This workshop was built using the older `agent-control` packages. For new deployments, we recommend
using the following packages instead:

```text
agent-control-sdk[splunk-ao]>=7.10.0
agent-control-evaluators>=7.10.0
agent-control-evaluator-splunk-ao>=7.10.0
```

Refer to the
[Agent Control](https://agent-observability-docs.splunk.com/concepts/agent-control/overview) document
for details about this newer SDK.

{{% /notice %}}

{{< /step >}}

{{< step title="Add the imports and decorate the steps" >}}

In `agent.py`, we've added the Agent Control imports at the end of the import section: 

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

{{< checkpoint title="Knowledge Check" >}}

What's the difference between how the app handles a `ControlViolationError` and a
`ControlSteerError`?

{{< details summary="Click here to see the answer" >}}
A `ControlViolationError` **blocks** the step: the action is stopped and the user receives a
friendly blocked message. A `ControlSteerError` **steers** the step: the agent retries with
the steering guidance appended to the prompt (up to a few attempts) to produce a corrected
response, only falling back to a safe message if it still can't comply.
{{< /details >}}
