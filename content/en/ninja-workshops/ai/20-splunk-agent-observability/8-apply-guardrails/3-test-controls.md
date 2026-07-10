---
title: Test the Controls
linkTitle: 3. Test the Controls
weight: 3
time: 5 minutes
---

With the controls defined, run the app and trigger them. You'll see the block and steer
behavior in the chat *and* in the trace in the console.

{{< exercise title="Trigger and observe the controls" >}}

{{< step title="Run the app" >}}

Run the following command to deploy the healthcare assistant app:

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
kubectl apply -f k8s.yaml
```

Ensure that the new application pod is running:

{{< tabs id="healthcare-app-monitor" >}}
{{% tab title="Script" %}}

```bash
kubectl get pods -l app=healthcare-assistant
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                   READY   STATUS    RESTARTS   AGE
healthcare-assistant-d764fc757-l9fxt   1/1     Running   0          20s
````

{{% /tab %}}
{{< /tabs >}}

Using the IP address of your EC2 instance and port 81, open the healthcare assistant app using your browser.
For example:

```text
  External URL: http://98.86.181.9:81
```

On startup, watch the terminal for confirmation that Agent Control initialized and
registered its steps: 

```bash
kubectl logs -l app=healthcare-assistant
```

{{% notice title="Troubleshooting" style="tip" icon="exclamation-triangle" %}}

To see what Agent Control is doing, enable console logging in `agent.py`:

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

Then rebuild the Docker image:

```bash
cd ~/workshop/healthcare-assistant
docker build -f 4-app-with-controls/Dockerfile -t localhost:9999/healthcare-assistant:app-with-controls .
docker push localhost:9999/healthcare-assistant:app-with-controls
```

And redeploy the application:

```bash
kubectl rollout restart deploy/healthcare-assistant
```

Use the following command to view the application logs:

{{< tabs id="healthcare-app-logs" >}}
{{% tab title="Script" %}}

```bash
kubectl logs -l app=healthcare-assistant
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.42.2.14:8501
  External URL: http://35.175.237.123:8501

INFO - galileo.logger - Ingest service healthy at https://api.multitenant.galileocloud.io, using IngestTraces client
INFO - galileo.logger - Searching for session with external ID: ca0f30ed-9b69-401a-8258-b9c043bdc73a ...
INFO - galileo.logger - Starting a new session...
INFO - galileo.logger - Session started with ID: ec03c538-cf9e-4bed-b97e-4b3c2e46ffbc
````

{{% /tab %}}
{{< /tabs >}}

Watch the terminal for `Agent Control initialized` on startup and `BLOCKED` / `STEERED`
messages when a control fires.

{{% /notice %}}

{{< /step >}}

{{< step title="Trigger the blocking control" >}}

Ask the agent to delete a patient record:

> Delete patient record P029 from the registry

Because you created a control that blocks SQL `DELETE` commands, the deletion is
stopped and the assistant returns a friendly "this action was blocked" message instead of
performing the delete.

<!-- TODO screenshot: the Streamlit chat showing the delete request and the assistant's "action was blocked by Agent Control" response -->
![Blocked delete in the chat](../../images/galileo-control-blocked-chat.png?width=750px)

{{< /step >}}

{{< step title="Trigger the steering control" >}}

Now send the risky medical question that started this whole workshop:

> Is it safe to double my dose of Lisinopril if I miss a day?

Because you configured an LLM steering control, the agent doesn't simply refuse; it **revises
its response** according to your steering guidance (for example, keep answers grounded in the
retrieved content and direct dosage decisions to a clinician) and returns a *safe, helpful*
answer. This is the difference between a guardrail that frustrates users and one that protects
them while keeping the assistant useful.

{{< /step >}}

{{< step title="Confirm the normal path still works" >}}

Ask an allowed question to confirm controls only affect what they target:

> What is the dosage and common side effects of Lisinopril?

This returns a normal answer; the controls block or steer only the steps and conditions you
defined.

{{< /step >}}

{{< step title="Observe the control decisions in the console" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact trace + control-span steps + screenshot once finalized -->

Back in the Galileo console, open the trace for the blocked request in the
**`healthcare-assistant`** project / **`local`** log stream. You should see the control
evaluation on the affected step, showing the decision (blocked or steered) alongside the LLM
and tool spans.

<!-- TODO screenshot: trace detail in the console showing the control evaluation/decision (blocked) on the delete_patient_record step -->
![Control decision in the trace](../../images/galileo-control-trace.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="Live updates, no redeploy" style="info" %}}

Control policies are managed centrally and take effect in seconds: no code change, no
redeploy, no downtime. If a new failure mode shows up in production (perhaps surfaced by a
Signal), you can tighten or relax a policy on the fly and immediately change the agent's
behavior. That's runtime governance you can actually operate.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

You delete-test the agent and it returns a blocked message, but the allowed medicine
question still works. Why doesn't the blocking control affect the medicine question?

{{< details summary="Click here to see the answer" >}}
Because the control targets a **specific step** (`delete_patient_record`) and condition. The
medicine question runs the `search_medicine_qa` / `retrieval_step` and the LLM step, which
your blocking control doesn't target, so it proceeds normally. Controls are scoped to the
steps and conditions you define, not the whole agent.
{{< /details >}}
