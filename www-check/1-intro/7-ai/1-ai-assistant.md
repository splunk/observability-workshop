---
title: 1. Ask the AI Assistant
weight: 1
---

The **AI Assistant** is a chat interface over your metrics, traces, logs and alerts. It understands plain English, cites the evidence behind its answers, and can even generate and run **SignalFlow** for you — no query language required.

{{% exercise title="Reproduce the investigation in plain English" %}}

* Open the ✨ **AI Assistant** from the toolbar on the **right-hand side** of any Splunk Observability Cloud page.
* Make sure your prompts mention the **service**, the **environment** (`[NAME OF WORKSHOP]-workshop`) and a **time window** — specificity gets you evidence-backed answers.
* Try the following prompts, one at a time:

  1. *"What are the issues in paymentservice in the workshop environment in the past hour?"*
  2. *"Investigate the sudden error increase in checkoutservice in the workshop environment in the past hour."*
  3. *"Analyze services upstream and downstream of paymentservice to root cause the high error rate."*
  4. *"Find error logs related to paymentservice in the workshop environment."*

{{< tabs >}}
{{% tab title="Question" %}}
**Does the AI Assistant identify the same culprit you found manually — and does it point at the bad version?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Yes.** The Assistant surfaces `paymentservice` as the source of the errors, correlates the `checkoutservice` errors as downstream/inherited, and — when you ask about the error logs — points to the failing version (`v350.10`) and the `Invalid request` / API-token error. It reaches the same conclusion as your RUM → APM → Logs investigation, in a fraction of the clicks.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

{{% notice title="Generate SignalFlow" style="info" icon="circle-info" %}}
The Assistant can also build charts for you. Try: *"Create a SignalFlow query for the error rate of paymentservice in the workshop environment"* — then add the result straight to a dashboard. We'll reuse this in the follow-up lessons.
{{% /notice %}}
