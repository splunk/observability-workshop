---
title: Update Alert Message and Alert Rule
linkTitle: 4.2.3 Alert Message and Description
weight: 4
---

## Objective

Customize the alert message to accurately reflect the multi-condition detection logic by:

- Explaining why the wizard-generated message is removed
- Referencing published threshold streams
- Explicitly communicating both the historical anomaly and static guardrail conditions

---

## Step 1 – Save the Detector

Click {{% button style="blue" %}}Save{{% /button %}} in the upper right corner.

---

## Step 2 – Edit Alert Message

Navigate to the detector’s **Alert Rules** tab.

Click {{% button style="blue" %}}Edit{{% /button %}} on the existing Alert Rule.

Select the **Alert message** tab and click **Customize**.

{{% notice icon="user" style="orange" title="Observe" %}}

Notice that the previously wizard-generated message body is no longer populated.

> Why did the default message disappear after editing the detector in SignalFlow?

{{% /notice %}}

{{% notice style="info" title="Why the Message Was Removed" %}}

Once you edited the detector in SignalFlow, you moved beyond the wizard-managed helper function.

Because the detection logic now uses custom streams and a manually composed `detect()` statement, the platform can no longer safely infer:

- What condition triggered the alert  
- Which threshold is authoritative  
- How to describe the detection logic  

When you take ownership of detection logic, you must also take ownership of the alert message.

{{% /notice %}}

Replace the message body with:

```handlebars
{{#if anomalous}}
	Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
{{else}}
	Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
{{/if}}

{{#if anomalous}}
Triggering condition: {{{readableRule}}}
{{/if}}

Mean value of signal in the last {{event_annotations.current_window}}: {{inputs.CPU.value}}

{{#if anomalous}}
Historical anomaly threshold: {{inputs.CPU_top_threshold.value}}
Static guardrail threshold: {{inputs.CPU_static_threshold.value}}
{{else}}
Clear threshold: {{inputs.clear_top.value}}
{{/if}}

{{#notEmpty dimensions}}
Signal details:
{{{dimensions}}}
{{/notEmpty}}

{{#if anomalous}}
{{#if runbookUrl}}Runbook: {{{runbookUrl}}}{{/if}}
{{#if tip}}Tip: {{{tip}}}{{/if}}
{{/if}}

{{#if detectorTags}}Tags: {{detectorTags}}{{/if}}

{{#if detectorTeams}}
Teams:{{#each detectorTeams}} {{name}}{{#unless @last}},{{/unless}}{{/each}}.
{{/if}}
```

You are now explicitly referencing:

- `{{inputs.CPU_top_threshold.value}}` → dynamic anomaly threshold  
- `{{inputs.CPU_static_threshold.value}}` → static 90% guardrail  

These variables are available because both streams were published in SignalFlow.

---

Click {{% button style="blue" %}}Done Editing{{% /button %}} to save the custom message.

Click {{% button style="blue" %}}ProceedAlert Recipients.{{% /button %}}.

---

## Step 3 – Update the Alert Rule Description 

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}}

In the **Activate...** step, update the **Description** to:

```
The 10m moving average of system.cpu.utilization (assumed to be cyclical over 1d periods) is more than 2.5 standard deviation(s) above its historical norm and has exceeded 90% for 15 minutes.
```

Click {{% button style="blue" %}}Update Alert Rule{{% /button %}} to save changes.

---

## Wrap Up

You have now:

- Used the wizard to configure historical baseline parameters  
- Refactored the generated SignalFlow to expose threshold streams  
- Added multi-condition alert logic (historical anomaly + static guardrail)  
- Published both anomaly and static thresholds for reuse  
- Updated the alert message and description to clearly communicate the detection logic