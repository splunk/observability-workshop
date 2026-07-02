---
title: Define Controls in the Console
linkTitle: 2. Define Controls in the Console
weight: 2
time: 7 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
{{% /notice %}}

The app now *registers* its controllable steps, but it's the Galileo console where you
*define the rules*: which steps are governed, what condition triggers them, and whether a
match should block or steer.

{{< exercise title="Define controls in Galileo" >}}

{{< step title="Open Agent Control in the console" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`ORGANIZATION_PLACEHOLDER`** org),
navigate to the **Agent Control** area and locate the agent matching your
`agent_control_agent_name` (for example, `agent-control-example`). The agent appears here
once the app has run at least once and registered its steps.

<!-- TODO screenshot: Agent Control landing page in the console showing the registered agent and its steps (Healthcare Assistant LLM step, get_patient_info, delete_patient_record, retrieval_step) -->
![Agent Control agent and steps](../../images/galileo-agent-control-agent.png?width=750px)

{{< /step >}}

{{< step title="Review the registered steps" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact step-list steps + screenshot once finalized -->

Confirm the steps the app registered are present:

* **Healthcare Assistant**: the LLM step.
* **get_patient_info**: patient lookup tool.
* **delete_patient_record**: patient deletion tool.
* **retrieval_step**: the shared step for search/retrieval tools.

These names come from the `@control(step_name=...)` decorators and the step registration in
the app, and are what your control rules target.

{{< /step >}}

{{< step title="Create a control that blocks deletions" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact control-creation steps + screenshot once finalized -->

Create a control targeting the **delete_patient_record** step that **blocks** the action.
Scope it to the **`local`** log stream (matching your `agent_control_target_type` of
`log_stream`). This prevents the agent from deleting patient records at run time.

<!-- TODO screenshot: control creation form targeting the delete_patient_record step, action set to Block, scoped to the local log stream -->
![Create a blocking control](../../images/galileo-agent-control-block.png?width=750px)

{{< /step >}}

{{< step title="Create a control that steers the LLM" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact control-creation steps + screenshot once finalized -->

Create a second control targeting the **Healthcare Assistant** LLM step that **steers** the
response, for example to keep answers within healthcare scope or to enforce a disclaimer.
Provide steering guidance the agent will use when it retries.

<!-- TODO screenshot: control creation form targeting the Healthcare Assistant LLM step, action set to Steer, with steering guidance text -->
![Create a steering control](../../images/galileo-agent-control-steer.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="Placeholders" style="info" %}}

The exact menu names, fields, and condition options in the Agent Control UI may differ from
what's shown above. Replace these placeholder steps and screenshots with your environment's
current navigation when you finalize the workshop.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

The step names in the console (`delete_patient_record`, `Healthcare Assistant`): where do
they come from?

{{< details summary="Click here to see the answer" >}}
They come from the application code: the `@control(step_name=...)` decorators (the LLM step is
`LLM_STEP_NAME = "Healthcare Assistant"`) and the tool step registration. The app registers
those steps with Agent Control on startup, which is why they appear in the console for you to
target with rules.
{{< /details >}}
