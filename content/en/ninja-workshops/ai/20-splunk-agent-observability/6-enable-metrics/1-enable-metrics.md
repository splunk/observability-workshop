---
title: Enable Metrics on the Log Stream
linkTitle: 1. Enable Metrics
weight: 1
time: 5 minutes
---

Metrics are configured on the **log stream**, so every new trace that lands is scored
automatically. You'll turn on a set of out-of-the-box metrics that matter for a healthcare
assistant.

{{< exercise title="Enable out-of-the-box metrics" >}}

{{< step title="Open your log stream settings" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`),
open your project and select the **`default`** log stream. 

Click the `Configure Metrics` button to open its metrics configuration.

![Log stream metrics configuration](../../images/sao-enable-metrics.png?width=750px)

{{< /step >}}

{{< step title="Enable the metrics that matter" >}}

Enable the following out-of-the-box metrics for your log stream: 

* **Context Adherence**: is the answer grounded in the retrieved medical content? (catches
  the "double the dose" style hallucination)
* **Correctness**: is the answer factually right?

![Log stream enable metrics](../../images/sao-enable-two-metrics.png?width=750px)

Save the configuration. From now on, new traces in this log stream are scored automatically.

{{< /step >}}

{{< step title="Apply the changes" >}}

Click `Apply` to apply the changes. We have the option to calculate metrics for traces that were already captured. 
Select the default option of `Last 1 day`: 

![Compute metrics](../../images/sao-compute-metrics.png?width=350px)

Click the `Compute` button to calculate metrics on existing traces. 

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

Why enable metrics on the **log stream** rather than scoring traces one by one?

{{< details summary="Click here to see the answer" >}}
Because log-stream metrics are applied **automatically to every new trace**, giving you
continuous, scaled evaluation instead of manual spot-checks. Combined with Luna's low-cost
scoring, you can evaluate all of your traffic rather than a small sample.
{{< /details >}}
