---
title: Explore Signals
linkTitle: 1. Explore Signals
weight: 1
time: 5 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
{{% /notice %}}

Generate Signals for your log stream and let the platform show you what's trending wrong.

{{< exercise title="Review Signals" >}}

{{< step title="Generate Signals" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`workshop`** org),
open your project / **`default`** log stream then click the **Signals** button.

![Generate Signals](../../images/sao-generate-signals.png?width=250px)

It will take a few moments to analyze the traces in this log stream and generate signals. 

{{< /step >}}

{{< step title="Review Signals" >}}

We can see that several signals have been generated for our log stream (the specific signals will vary from 
one log stream to the next): 

<!-- TODO screenshot: Signals view listing detected failure patterns for the healthcare assistant log stream -->
![Signals overview](../../images/sao-signals-overview.png?width=750px)

{{< /step >}}

{{< step title="Open a signal for context" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact signal-detail steps + screenshot once finalized -->

Select a signal and read its actionable context: what the pattern is, why it's happening, and
the recommended next step. 

For example, let's click on the signal named `Database Metadata Leakage Risk`:

<!-- TODO screenshot: signal detail showing the pattern description, root-cause explanation, and recommended remediation -->
![Signal detail](../../images/sao-signal-detail.png?width=250px)

This signals explains how the `get_patient_info` tool output includes raw SQL queries, database source, 
and table names, which could be leaked to end users if the LLM echoes this metadata.

It provides a suggestion action to remediate the issue, which is to strip database metadata 
(SQL queries, table names, source info) from tool outputs before returning them to the LLM.

{{< /step >}}

{{< step title="Jump to the underlying traces" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact pivot steps + screenshot once finalized -->

From the signal, we can pivot into the specific traces that make up the pattern by clicking on the 
`View Affected Spans in Table` button: 

<!-- TODO screenshot: a signal expanded to its contributing traces, with one trace opened -->
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

How do Signals complement the metrics you enabled in the previous chapter?

{{< details summary="Click here to see the answer" >}}

Metrics score **known** quality dimensions you choose to measure (e.g., Context Adherence).
Signals automatically surface **unknown** recurring failure patterns (planning loops, tool
errors, routing failures) that you didn't write a metric for. Together they cover both the
problems you anticipated and the ones you didn't.

We have the option to create a new metric from a specific signal, which allows us to 
track when the underlying issue happens again in the future so we can take appropriate action. 

{{< /details >}}
