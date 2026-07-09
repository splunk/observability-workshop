---
title: Review Metric Scores
linkTitle: 2. Review Metric Scores
weight: 2
time: 5 minutes
---

After a few moments, we'll see how the existing traces get automatically scored on the 
`Context Adherence` and `Correctness` metrics. 
This is where a hallucinated dosage or a wrong tool call stops being invisible.

{{< exercise title="Review metric scores" >}}

{{< step title="Wait for metrics to be computed" >}}

Looking at the log trace, we can see that metrics are being computed for our traces: 

![Log stream metrics computing](../../images/sao-metrics-computing.png?width=750px)

{{< /step >}}

{{< step title="Review the scores in the log stream" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the console, return to the **`local`** log stream and open the recent traces. Each trace
now carries metric scores alongside its spans. Scan for low **Context Adherence** or
**Correctness** scores; these flag answers that drifted from the retrieved medical content.

<!-- TODO screenshot: trace list / detail showing metric score columns (Context Adherence, Correctness, Tool Selection Quality, Prompt Injection) with at least one low score highlighted -->
![Metric scores on traces](../../images/sao-metric-scores.png?width=750px)

{{< /step >}}

{{< step title="Drill into a flagged trace" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact drilldown steps + screenshot once finalized -->

Open a trace with a low quality score and confirm the story in the spans: compare the
retrieved context against the model's answer to see exactly where it went wrong. You've now
turned "a patient complained" into "here is the specific request, the specific span, and the
specific metric that caught it."

<!-- TODO screenshot: flagged trace detail with the metric score and the offending span expanded -->
![Flagged trace detail](../../images/sao-metric-flagged-trace.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="The payoff" style="info" %}}

You now have an automated quality signal across all traffic. But metrics only catch the
problems you thought to measure. Next, you'll use **Signals** to surface failure patterns you
*didn't* know to look for.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

A medicine answer scores low on **Context Adherence** but the retrieval span shows the correct
information was retrieved. What kind of problem is that, and why does it matter for Careful
Health Provider?

{{< details summary="Click here to see the answer" >}}
It's a **hallucination / grounding** problem: the right context was available, but the model's
answer wasn't faithful to it. For a healthcare assistant that's high-stakes: it's exactly how
a "take double the dose" answer happens, which is why you'll add a runtime guardrail for it
later.
{{< /details >}}
