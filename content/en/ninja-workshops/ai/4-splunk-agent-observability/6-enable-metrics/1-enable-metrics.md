---
title: Enable Evaluators on the Agent Stream
linkTitle: 1. Enable Evaluators
weight: 1
time: 5 minutes
---

Evaluators are configured on the **agent stream**, so every new trace that lands is scored
automatically. You'll turn on a set of out-of-the-box evaluators that matter for a healthcare
assistant.

{{< exercise title="Enable out-of-the-box evaluators" >}}

{{< step title="Open your agent stream settings" >}}

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`workshop`** org),
open your project and select the **`default`** agent stream. 

Click the `Configure Evaluators` button to open its evaluators configuration.

![Agent stream evaluators configuration](../../images/sao-enable-metrics.png?width=750px)

{{< /step >}}

{{< step title="Enable the evaluators that matter" >}}

Enable the following out-of-the-box evaluators for your agent stream: 

* **Context Adherence**: is the answer grounded in the retrieved medical content? (catches
  the "double the dose" style hallucination)
* **Correctness**: is the answer factually right?

![Agent stream enable evaluators](../../images/sao-enable-two-metrics.png?width=750px)

Save the configuration. From now on, new traces in this agent stream are scored automatically.

{{< /step >}}

{{< step title="Apply the changes" >}}

Click `Apply` to apply the changes. We have the option to exercise evaluators for traces that were already captured. 
Select the default option of `Last 1 day`: 

![Compute metrics](../../images/sao-compute-metrics.png?width=350px)

Click the `Compute` button to exercise evaluators on existing traces. 

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

Why enable evaluators on the **agent stream** rather than scoring traces one by one?

{{< details summary="Click here to see the answer" >}}
Because agent-stream evaluators are applied **automatically to every new trace**, giving you
continuous, scaled evaluation instead of manual spot-checks. Combined with Luna's low-cost
scoring, you can evaluate all of your traffic rather than a small sample.
{{< /details >}}
