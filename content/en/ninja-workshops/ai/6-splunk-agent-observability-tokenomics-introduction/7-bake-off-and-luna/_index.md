---
title: Bake Off and Optimize with Luna
linkTitle: 7. Bake Off and Optimize
weight: 7
time: 15 minutes
---

Experiments let us compare candidate configurations before release. Evaluators let us continue
measuring their behavior after release.

### 1. Define the quality gate

Return to **Product Model Comparison**. Before selecting a winner, decide which measures are
required for the use case. In this example, Context Adherence and Ground Truth Adherence answer
different questions:

* **Context Adherence:** is the response supported by the supplied context?
* **Ground Truth Adherence:** does the response match the expected answer?

If thresholds are chosen after viewing the result, the team can fit the decision to the answer it
already wanted. Define the acceptance bar first.

### 2. Compare every input, not one example

Use the arrows above the comparison to move through all 18 inputs. A model should not be selected
from one favorable row or an average that hides important failures.

For each configuration:

1. Eliminate results that fail a required quality or safety threshold.
2. Compare tokens, latency, and cost among the remaining candidates.
3. Inspect failures by task type to decide whether routing is preferable to one global model.
4. Record what must be monitored after release.

### 3. Evaluate production sessions

Return to the **E-Commerce Customer Session** and open the Evaluators panel. The session-level
Agent Efficiency result includes a verdict, a rationale, the evaluator model, latency, and cost.
This makes a score explainable: we can see why the evaluator marked the session inefficient and
which behavior needs attention.

Evaluation creates its own economic challenge. Using a large general-purpose model as a judge for
every trace adds cost and latency, so teams often sample production traffic. Sampling can miss the
rare routes and new behaviors that matter most.

### 4. Optimize evaluation with Luna

Luna is a family of purpose-built small language models for evaluation. Its role is to make broad,
fast evaluation practical so quality can remain beside token, cost, and latency telemetry across
the application lifecycle.

The feedback cycle is:

1. **Experiment:** compare models, prompts, and workflows on a fixed dataset.
2. **Observe:** evaluate production traces and sessions.
3. **Investigate:** open failed or expensive traces and read the evaluator rationale.
4. **Improve:** change routing, prompts, tools, retrieval, or context.
5. **Repeat:** rerun the experiment before release.

> Luna does not directly reduce the application's generation tokens. It changes the economics of
> the evaluation layer, helping teams find generation waste without replacing it with an equally
> expensive evaluation problem.

Current product material states that Luna SLMs can run evaluations and guardrails on 100% of
traffic at **up to 98% lower cost than LLM-as-judge**. "Up to" is not an expected saving for every
workload; actual results depend on the evaluator and traffic.

{{< checkpoint title="Knowledge Check" >}}

Why should experiment results and production evaluators be used together?

{{< details summary="Click here to see the answer" >}}
Experiments provide a controlled comparison before release. Production evaluators reveal quality,
efficiency, and behavior as real traffic changes. Production findings then become new experiment
cases, creating a continuous feedback cycle.
{{< /details >}}

What would you monitor after releasing the winning configuration? Consider quality drift, cost per
completed action, token distribution, latency, route mix, retrieval size, loop frequency, and
evaluator coverage.

Optimization is a cycle, not a one-time model swap: instrument, attribute, evaluate, compare,
release, and continuously validate.
