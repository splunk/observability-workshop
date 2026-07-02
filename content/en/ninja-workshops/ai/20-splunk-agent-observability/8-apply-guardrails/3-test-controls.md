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

From `4-app-with-controls` (virtual environment active, database loaded), start the app:

```bash
streamlit run app.py
```

On startup, watch the terminal for confirmation that Agent Control initialized and
registered its steps.

{{< /step >}}

{{< step title="Trigger the blocking control" >}}

Ask the agent to delete a patient record:

> Delete patient record P029 from the registry

Because you created a control that blocks the `delete_patient_record` step, the deletion is
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
