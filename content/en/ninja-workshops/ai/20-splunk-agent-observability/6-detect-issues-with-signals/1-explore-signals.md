---
title: Explore Signals
linkTitle: 1. Explore Signals
weight: 1
time: 10 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
{{% /notice %}}

Open Signals for your log stream and let the platform show you what's trending wrong.

{{< exercise title="Review Signals" >}}

{{< step title="Open the Signals view" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`ORGANIZATION_PLACEHOLDER`** org),
open the **`healthcare-assistant`** project / **`local`** log stream and navigate to the
**Signals** view.

<!-- TODO screenshot: Signals view listing detected failure patterns for the healthcare assistant log stream -->
![Signals overview](../../images/sao-signals-overview.png?width=750px)

{{< /step >}}

{{< step title="Open a signal for context" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact signal-detail steps + screenshot once finalized -->

Select a signal and read its actionable context: what the pattern is, why it's happening, and
the recommended next step. Note how it groups many individual traces into a single, named
issue.

<!-- TODO screenshot: signal detail showing the pattern description, root-cause explanation, and recommended remediation -->
![Signal detail](../../images/sao-signal-detail.png?width=750px)

{{< /step >}}

{{< step title="Jump to the underlying traces" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact pivot steps + screenshot once finalized -->

From the signal, pivot into the specific traces that make up the pattern. You go from "there's
a recurring problem" to "here are the exact requests behind it" in a couple of clicks,
exactly the targeted remediation Signals are designed to enable.

<!-- TODO screenshot: a signal expanded to its contributing traces, with one trace opened -->
![Signal to traces](../../images/sao-signal-traces.png?width=750px)

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
{{< /details >}}
