---
title: Enable Metrics on the Log Stream
linkTitle: 1. Enable Metrics
weight: 1
time: 5 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
{{% /notice %}}

Metrics are configured on the **log stream**, so every new trace that lands is scored
automatically. You'll turn on a set of out-of-the-box metrics that matter for a healthcare
assistant.

{{< exercise title="Enable out-of-the-box metrics" >}}

{{< step title="Open your log stream settings" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`ORGANIZATION_PLACEHOLDER`** org),
open the **`healthcare-assistant`** project and select the **`local`** log stream. Open its
metrics configuration.

<!-- TODO screenshot: log stream metrics configuration panel with the list of available out-of-the-box metrics -->
![Log stream metrics configuration](../../images/sao-enable-metrics.png?width=750px)

{{< /step >}}

{{< step title="Enable the metrics that matter here" >}}

<!-- PLACEHOLDER UI NAVIGATION: confirm exact metric names available in the UI and update this list -->

Enable a set of out-of-the-box metrics relevant to this assistant, for example:

* **Context Adherence**: is the answer grounded in the retrieved medical content? (catches
  the "double the dose" style hallucination)
* **Correctness**: is the answer factually right?
* **Tool Selection Quality**: did the agent pick the right tool with the right arguments?
* **Prompt Injection**: did the input try to subvert the agent's instructions?

Save the configuration. From now on, new traces in this log stream are scored automatically.

{{% notice title="Placeholder" style="info" %}}

The exact metric names and toggles in the UI may differ. Replace this list and the screenshot
with your environment's current options when you finalize the workshop.

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

Why enable metrics on the **log stream** rather than scoring traces one by one?

{{< details summary="Click here to see the answer" >}}
Because log-stream metrics are applied **automatically to every new trace**, giving you
continuous, scaled evaluation instead of manual spot-checks. Combined with Luna's low-cost
scoring, you can evaluate all of your traffic rather than a small sample.
{{< /details >}}
