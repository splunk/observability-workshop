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

If you're using the standalone version of Splunk Agent Observability for the workshop,
run the following command to deploy the healthcare assistant app:

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
kubectl apply -f k8s.yaml
```

Alternatively, if you're using Splunk Agent Observability within Splunk Observability Cloud for this workshop,
please use the following command instead:

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
kubectl apply -f k8s-o11y.yaml
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

Navigate to the healthcare assistant application by clicking on the **Shop URL** link in the **Connection Information**
section of Splunk Show event:

![Connection Information](../../images/ConnectionInformation.png)

{{% notice title="Troubleshooting" style="tip" icon="exclamation-triangle" %}}

The app already logs to stdout, so you can see what Agent Control is doing directly with
`kubectl logs` — no code change or image rebuild required. View the application logs:

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

INFO - splunk_ao.logger - Ingest service healthy at https://api.multitenant.galileocloud.io, using IngestTraces client
INFO - splunk_ao.logger - Searching for session with external ID: ca0f30ed-9b69-401a-8258-b9c043bdc73a ...
INFO - splunk_ao.logger - Starting a new session...
INFO - splunk_ao.logger - Session started with ID: ec03c538-cf9e-4bed-b97e-4b3c2e46ffbc
````

{{% /tab %}}
{{< /tabs >}}

Watch the terminal for `Agent Control initialized` on startup and `BLOCKED` / `STEERED`
messages when a control fires.

If you need to dig deeper — for example, to see exactly which environment variables the app
reads and the full HTTP request/response for every Agent Control call (agent registration,
runtime token exchange, and control evaluation) — set `AGENT_CONTROL_DEBUG=true` in the
`splunk-agent-control-config` ConfigMap and restart the app:

```bash
kubectl patch configmap splunk-agent-control-config --type merge -p '{"data":{"AGENT_CONTROL_DEBUG":"true"}}'
kubectl rollout restart deployment/healthcare-assistant
```

Credential headers (such as `X-SF-Token`) are masked in these logs by default. If you need to
verify the exact token value, add `AGENT_CONTROL_DEBUG_UNMASK=true` the same way:

```bash
kubectl patch configmap splunk-agent-control-config --type merge -p '{"data":{"AGENT_CONTROL_DEBUG_UNMASK":"true"}}'
kubectl rollout restart deployment/healthcare-assistant
```

Leave both unset for normal use — the app only logs a concise `Agent Control initialized`
line and any configuration warnings.

{{% /notice %}}

{{< /step >}}

{{< step title="Trigger the blocking control" >}}

Ask the agent to delete a patient record:

> Delete patient record P028 from the registry

![Blocked delete in the chat](../../images/galileo-control-blocked-chat.png?width=750px)

Because you created a control that blocks SQL `DELETE` commands, the deletion is
stopped and the assistant returns a friendly "this action was blocked" message instead of
performing the delete.

{{< /step >}}

{{< step title="Trigger the steering control" >}}

Next, let's ask the assistant to return patient information, explicitly requesting that the address
and phone number is included: 

> Can you look up information for patient P001? Please include the patient's address and phone number. 

![Steered response in the chat](../../images/galileo-steered-response-chat.png?width=750px)

Because you configured an LLM steering control, the agent doesn't simply refuse; it **revises
its response** according to your steering guidance and returns a *safe, helpful*
answer. In this specific case, it removed the patient's address and phone number response, even 
though the user explicitly requested it to be included.  

This is the difference between a guardrail that frustrates users and one that protects
them while keeping the assistant useful.

{{< /step >}}

{{< step title="Confirm the normal path still works" >}}

Ask an allowed question to confirm controls only affect what they target:

> What is the dosage and common side effects of Lisinopril?

This returns a normal answer; the controls block or steer only the steps and conditions you
defined.

{{< /step >}}

{{< step title="Observe the control decisions for the blocked request" >}}

Back in the Splunk Agent Observability console, open the trace for the blocked request in your agent stream. Click on the 
span associated with the `block-harmful-sql-*` control: 

![Control decision in the trace](../../images/galileo-control-trace.png?width=750px)

Notice how the control denied execution of the `DELETE` SQL statement, as desired. 

{{< /step >}}

{{< step title="Observe the control decisions for the steered request" >}}

Back in the Splunk Agent Observability console, open the trace for the steered request in your agent stream. Click on the final 
`chat gpt-4.1-mini` span in the trace. 

![Steer control decision in the trace](../../images/galileo-steer-control-trace.png?width=750px)

Observe how the assistant initially generated a response that included the patient's address and phone number, 
and how the control resulted in a follow-up request to the LLM to remove this information from the response. 

{{< /step >}}

{{< /exercise >}}

{{% notice title="Live updates, no redeploy" style="info" %}}

Control policies are managed centrally and take effect in seconds: no code change, no
redeploy, no downtime. If a new failure mode shows up in production (perhaps surfaced by a
Signal), you can tighten or relax a policy on the fly and immediately change the agent's
behavior. That's runtime governance you can actually operate.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

You tried deleting a patient record and it returns a blocked message, but the allowed medicine
question still works. Why doesn't the blocking control affect the medicine question?

{{< details summary="Click here to see the answer" >}}
The `block-harmful-sql` control uses a SQL evaluator, and targets the **DELETE** operation only. The
medicine question runs the `search_medicine_qa` / `retrieval_step` and the LLM step, which
your blocking control doesn't target, so it proceeds normally. Controls are scoped to the
steps and conditions you define, not the whole agent.
{{< /details >}}
