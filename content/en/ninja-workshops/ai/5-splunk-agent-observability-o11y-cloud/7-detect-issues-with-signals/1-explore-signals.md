---
title: Explore Signals
linkTitle: 1. Explore Signals
weight: 1
time: 5 minutes
---

{{% notice style="warning" title="Caution" %}}
**Generating Signals requires multiple prompts to an LLM, which can result in significant usage costs 
if every workshop participant runs the process individually. For this reason, please observe as the 
workshop instructor completes the steps in this section, rather than performing them yourself.**
{{% /notice %}}

Generate Signals for your agent stream and let the platform show you what's trending wrong.

{{< exercise title="Review Signals" >}}

{{< step title="Generate Signals" >}}

In your browser, go to the Splunk Agent Observability console at `https://console.multitenant.sao.splunkcloud.com`
and **`workshop`** org

Open the `Splunk Agent Observability Workshop` project, and select the agent stream that
matches the Instance ID you found above (such as `shw-51ea`).

Click on the **Signals** tab: 

![Signals Page](../../images/sao-signals-page.png?width=750px)

Ensure the LLM is set to `gpt-5 (Azure)`, then click the **Generate Signals** button.

![Generate Signals](../../images/sao-generate-signals.png?width=500px)

It will take a few moments to analyze the traces in this agent stream and generate signals. 

{{< /step >}}

{{< step title="Review Signals" >}}

We can see that several signals have been generated for our agent stream (the specific signals will vary from 
one agent stream to the next): 

![Signals overview](../../images/sao-signals-overview.png?width=750px)

{{< /step >}}

{{< step title="Open a signal for context" >}}

Select a signal and read its actionable context: what the pattern is, why it's happening, and
the recommended next step. 

For example, let's click on the signal named `PII in tool outputs`:

![Signal detail](../../images/sao-signal-detail.png?width=250px)

This signal explains that the `get_patient_info` tool response contains full patient PII (address and phone) 
and database/SQL metadata, even though the assistant response to the user only exposes limited fields 
(name, patient_type, prescription). This still creates a privacy and compliance risk because the sensitive 
data is present in tool outputs and therefore in your observability logs and in the model context.

It provides a suggested action to remediate the issue, which is to
minimize and/or redact PII in `get_patient_info` tool outputs (and logs) 
to prevent sensitive data exposure.

{{< /step >}}

{{< step title="Jump to the underlying traces" >}}

From the signal, we can pivot into the specific traces that make up the pattern: 

![Signal to traces](../../images/sao-signal-traces.png?width=750px)

This allows us to go from "there's a recurring problem" to "here are the exact requests behind it" in a couple of clicks,
exactly the targeted remediation Signals are designed to enable.

{{< /step >}}

{{< /exercise >}}

{{% notice title="Why this matters" style="info" %}}

Without Signals, this kind of analysis means an engineer manually combing through traces after
an incident, often for weeks. Signals compress that into minutes, and catch issues before they
become incidents at all.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

How do Signals complement the evaluators you enabled in the previous chapter?

{{< details summary="Click here to see the answer" >}}

Evaluators score **known** quality dimensions you choose to measure (e.g., Context Adherence).
Signals automatically surface **unknown** recurring failure patterns (planning loops, tool
errors, routing failures) that you didn't write an evaluator for. Together they cover both the
problems you anticipated and the ones you didn't.

We have the option to create a new evaluator from a specific signal, which allows us to 
track when the underlying issue happens again in the future so we can take appropriate action. 

{{< /details >}}
