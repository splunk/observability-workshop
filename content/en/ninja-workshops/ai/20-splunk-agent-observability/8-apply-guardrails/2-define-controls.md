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

{{< step title="Open the Controls tab" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`workshop`** org),
open your project / **`default`** log stream then click on the **Controls** tab.

![Log Stream Controls](../../images/galileo-log-stream-controls.png?width=750px)

{{< /step >}}

{{< step title="Browse and add controls to your agent" >}}

Click the `Add control` button to add a control to your log stream. 
You'll be presented with a list of controls to clone and attach to your log stream, 
as well as the option to create a new control. 

![Log Stream Add Controls](../../images/galileo-log-stream-add-controls.png?width=750px)

{{< /step >}}

{{< step title="Add the Block Harmful SQL Control" >}}

Next, let's add an existing control called `Block-harmful-sql` to our log stream. 
To do this, click the `Clone and attach` button beside the `Block-harmful-sql` control: 

![Create a blocking control](../../images/galileo-agent-control-block.png?width=750px)

Click on the control name to see the details of the control: 

![Block Control Details](../../images/galileo-block-control-details.png?width=750px)

This control is used to detect and block any `DELETE` SQL operations. It's executed 
**before** the associated tool call, to prevent the agent from deleting patient 
records at run time.

Click `Discard Edits` to return to the list of controls for your log stream. 

{{< /step >}}

{{< step title="Create a control that steers the LLM" >}}

Let's add a second control targeting the **Healthcare Assistant** LLM step that **steers** the
response, for example to keep answers within healthcare scope or to enforce a disclaimer.

To do this, click on the `Add control` button and then click `Clone and attach` beside the 
`steer-output-pii` control. 

Once the control is added, click on it to view the details: 

![Create a steering control](../../images/galileo-agent-control-steer.png?width=750px)

This control runs **after** LLM calls, and when a phone number or address are detected in the LLM response, 
the agent is "steered" towards removing these fields from the final response. 

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

The step names in the console (`delete_patient_record`, `Healthcare Assistant`): where do
they come from?

{{< details summary="Click here to see the answer" >}}
They come from the application code: the `@control(step_name=...)` decorators (the LLM step is
`LLM_STEP_NAME = "Healthcare Assistant"`) and the tool step registration. The app registers
those steps with Agent Control on startup, which is why they appear in the console for you to
target with rules.
{{< /details >}}
