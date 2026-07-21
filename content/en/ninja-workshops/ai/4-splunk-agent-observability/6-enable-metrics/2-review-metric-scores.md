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

In Splunk Agent Observability, return to the **`default`** log stream and review the recent traces. Each trace
now carries metric scores alongside its spans. 

![Metric scores on traces](../../images/sao-metric-scores.png?width=750px)

We can see that one of the traces evaluated to `False` for both `Context Adherence` and `Correctness`. 
This is the trace that we sent earlier using the `Log Hallucination` button. 

Let's click on this trace and take a closer look. 

{{< /step >}}

{{< step title="Drill into a flagged trace" >}}

Click on the `LLM Response` span, and notice there are two new metric categories on the right-hand side 
of the screen: `Output Quality`, which includes the `Correctness` metric, and `RAG Quality`, which includes 
the `Context Adherence` metric. 

If we hover over `false` beside the `Context Adherence` metric, we can see the rationale for why this span 
received this score. 

In this case, it explains that the assistant gave a dosage of 100 mg daily
and side effects of rashes, itching, and swelling, which directly contradicts the context 
and adds unsupported information.

![Flagged trace detail](../../images/sao-metric-flagged-trace.png?width=750px)

This type of finding turns "a patient complained" into "here is the specific request, the specific span, and the
specific metric that caught it."

{{< /step >}}

{{< step title="Autotune Feedback" >}}

You may be wondering: what if a metric gets the evaluation wrong? 

We can provide feedback on any metric by clicking the `Add feedback` button: 

![Add Feedback Button](../../images/sao-add-feedback-button.png?width=750px)

And providing the `Corrected value` and `Rationale`:

![Autotune Feedback](../../images/sao-autotune-feedback.png?width=750px)

This human feedback helps improve how the metric evaluates similar cases over time, which ultimately 
ensures that the scoring becomes more aligned to our real standards. 

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
