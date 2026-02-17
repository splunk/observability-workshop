---
title: Update Alert Message and Alert Rule
linkTitle: 4.2.3 Alert Message and Description
weight: 4
---

## Step 1 – Save the Detector

Click **Save** in the upper right corner.

---

## Step 2 – Edit Alert Rules

Navigate to the detector’s **Alert Rules**.
then go to **Alert Message** and click **Customize**

Notice: after editing the detector in SignalFlow, the wizard-generated message body is no longer automatically populated.

Replace the message body with the previous message:

```handlebars
{{#if anomalous}}
	Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
{{else}}
	Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
{{/if}}

{{#if anomalous}}
Triggering condition: {{{readableRule}}}
{{/if}}

Mean value of signal in the last {{event_annotations.current_window}}: {{inputs.summary.value}}
{{#if anomalous}}Trigger threshold: {{inputs.fire_top.value}}
{{else}}Clear threshold: {{inputs.clear_top.value}}.
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

--- 

Click **Done**

---

## Step 3 – Update the Alert Rule Description 

In the **Activate...*** step, Update the **Description** to:

```
The 10m moving average of system.cpu.utilization (assumed to be cyclical over 1d periods) is more than 2.5 standard deviation(s) above its historical norm and has exceeded 90% for 15 minutes.
```

Click **Update Alert Rule** to save changes.

---

## Wrap Up

You have now:

- Used the wizard to configure historical baseline parameters
- Refactored the generated SignalFlow to expose threshold streams
- Added multi-condition alert logic (historical anomaly + static guardrail)
- Updated the alert message and description to clearly communicate the conditions