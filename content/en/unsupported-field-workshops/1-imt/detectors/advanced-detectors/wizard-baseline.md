---
title: Historical Anomaly Detector
linkTitle: 4.2.1 Historical Anomaly with Detector Wizard
weight: 3
---

## Objective

Create a historical baseline anomaly detector using the detector wizard and examine the generated alert message.

---

## Step 1 – Create the Detector

Navigate to:

**Alerts & Detectors → {{% button style="blue" %}}Create Detector{{% /button %}} → Custom Detector**

**ADD YOUR INITIALS** before the proposed detector name.

{{% notice title="Naming the detector" style="info" %}}
It's important that you add your initials in front of the proposed detector name.

It should be something like this: **XYZ's Advanced Detector**.
{{% /notice %}}

{{% button style="blue" %}}Create Alert Rule{{% /button %}}

Configure the following in the alert signal:

- **Signal (A):** `system.cpu.utilization`

{{% button style="blue" %}}Add Filter{{% /button %}}
- **Filter:** `deployment.environment : astronomy-shop`

{{% button style="blue" %}}Proceed to Alert Condition{{% /button %}}, choose Historical Anomaly and then

{{% button style="blue" %}}Proceed to Alert Settings{{% /button %}}
- **Cycle length:** `1d`
- **Alert when:** `Too high`
- **Trigger Sensitivity:** `High`

Show advanced settings and review

{{% button style="blue" %}}Proceed to Alert Message{{% /button %}}.

---

## Step 2 – Examine the Default Alert Message

Under Message Preview, click **Customize** and review the generated message:

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

### What This Message Is Doing

This message uses conditional blocks to render different content depending on whether the detector is triggering or clearing.

- `{{#if anomalous}}` renders content only when the detector is firing.
- The `{{else}}` branch renders when the detector clears.

This allows one template to handle both trigger and clear notifications.

---

### Important Variables Available in Alert Messages

The following variables are automatically available:

- `{{ruleName}}` – Name of the alert rule  
- `{{detectorName}}` – Name of the detector  
- `{{timestamp}}` – Time of the event  
- `{{readableRule}}` – Human-readable firing condition  
- `{{event_annotations.current_window}}` – Evaluation window duration  
- `{{inputs.summary.value}}` – Aggregated metric value for the evaluation window  
- `{{inputs.fire_top.value}}` – Historical anomaly trigger threshold  
- `{{inputs.clear_top.value}}` – Historical anomaly clear threshold  
- `{{dimensions}}` – Dimension key/value pairs (host, environment, etc.)  
- `{{runbookUrl}}` – Configured runbook link (if set)  
- `{{tip}}` – Configured tip (if set)  
- `{{detectorTags}}` – Tags assigned to the detector  
- `{{detectorTeams}}` – Assigned teams  

Any stream that is published in SignalFlow becomes available as:
`{{inputs.<stream_name>.value}}`

Click {{% button style="blue" %}}Done Editing{{% /button %}} to close the custom message. 

{{% button style="blue" %}}Proceed to Alert Recipients{{% /button %}} and do not select anything, we don't actually want to send notifications for this scenario

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}}

{{% button style="blue" %}}Activate Alert Rule{{% /button %}}

When prompted about Missing Alert Notification Policy, choose {{% button style="blue" %}}Save{{% /button %}}