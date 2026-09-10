---
title: Review Experiment Results
linkTitle: 3. Review Experiment Results
weight: 3
time: 5 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
{{% /notice %}}

Now review the experiment in the Galileo console: inspect the per-row scores, drill into an
individual trace, and compare two runs.

{{< exercise title="Review your experiment in Galileo" >}}

{{< step title="Open the Experiments view" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

In the Galileo console (`https://console.multitenant.galileocloud.io`, **`ORGANIZATION_PLACEHOLDER`** org),
open the **`healthcare-assistant`** project and navigate to the **Experiments** view. You
should see the experiment you just ran (for example, `healthcare-experiment` or
`lisinopril-eval`).

<!-- TODO screenshot: Experiments list in the healthcare-assistant project showing the experiment run(s) with aggregate metric columns -->
![Experiments list](../../images/galileo-experiments-list.png?width=750px)

{{< /step >}}

{{< step title="Review aggregate metrics" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact metric-panel steps + screenshot once finalized -->

Open the experiment and review the aggregate scores for each metric: Ground Truth
Adherence, Prompt Injection, Chunk Attribution Utilization, and Context Adherence. These
summarize how the agent performed across the whole dataset.

<!-- TODO screenshot: experiment summary showing aggregate metric scores across the dataset -->
![Experiment aggregate metrics](../../images/galileo-experiment-metrics.png?width=750px)

{{< /step >}}

{{< step title="Drill into a single row" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact row-drilldown steps + screenshot once finalized -->

Select an individual row to see its input, the agent's generated output, the reference
output, and the per-row metric scores. From here you can open the underlying trace and see
the same nested spans you explored in Chapter 4, now tied to a scored experiment row.

<!-- TODO screenshot: single experiment row detail showing input, generated output, reference output, per-row metric scores, and a link to the underlying trace -->
![Experiment row detail](../../images/galileo-experiment-row-detail.png?width=750px)

{{< /step >}}

{{< step title="Compare two runs" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact comparison steps + screenshot once finalized -->

If you ran the experiment with two different models, compare the runs side by side to see
which configuration scored better on each metric. This is the objective comparison you set
out to get at the start of the chapter.

<!-- TODO screenshot: side-by-side comparison of two experiment runs (e.g., gpt-4o vs gpt-4o-mini) with metric deltas highlighted -->
![Experiment comparison](../../images/galileo-experiment-comparison.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="Experiments as a release gate (CI/CD)" style="info" %}}

Because experiments run from code (`python experiments/run_experiment.py`), they drop straight
into a CI/CD pipeline. Run the experiment on every pull request or pre-release build, then
**fail the build** if a key metric, say *Context Adherence* or *Correctness*, regresses
below a threshold. That turns "we think this prompt change is fine" into an automated,
evidence-based quality gate, so a regression never reaches patients in the first place.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

A row shows a high *Prompt Injection* score. What does that indicate, and where would you
look next?

{{< details summary="Click here to see the answer" >}}
A high *Prompt Injection* score flags that the **input** looks like an attempt to override
the agent's instructions. You'd open that row's trace to see how the agent handled it,
whether it followed the injected instruction or stayed on task, which is exactly the kind of
behavior you'll guard against with **agent controls** in the next chapter.
{{< /details >}}
