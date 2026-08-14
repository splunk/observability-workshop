---
title: Cause 3 — Spend Without Outcomes
linkTitle: 6. Connect Spend to Outcomes
weight: 6
time: 15 minutes
---

Individual traces explain one interaction. Trends show whether the same behavior is isolated or
repeated across production traffic.

Open the `workshop` agent stream and select **Trends**.

### 1. Compare consumption with demand

Under **System Metrics**, review:

* Total Tokens
* Input Tokens and Output Tokens
* Agent Cost
* Latency
* Traces Count
* API Failures

The prepared environment contains 290 traces and large synthetic token and cost spikes. Treat
these values as workshop data, not as typical production volumes or costs.

Start with the relationship between metrics rather than the total alone:

* Did tokens rise because trace volume rose?
* Did cost increase faster than traffic?
* Was the spike driven by input tokens, output tokens, or both?
* Did latency or failures change at the same time?

A bill can show the cost spike. These trends show whether it came from healthy demand or a change
in cost per interaction.

### 2. Segment the trend

Use **Group by** and **Filters** to narrow the time window and isolate the dimensions present in
the telemetry, such as model, project, agent stream, environment, or application attributes.

The objective is to move from:

> Token usage increased.

To a statement that can be acted on:

> Input tokens increased for one route after a version change, while trace volume remained stable.

### 3. Add custom and agent-quality metrics

Scroll to **Custom Metrics** and **Agent Quality**. The prepared stream includes:

* `model_selection_match`, showing whether the selected model matched the expected route.
* **Agent Efficiency**, showing whether the agent took an effective path.
* **Action Completion**, showing whether the user's requested action was completed.

These metrics connect consumption to behavior and outcome. For example, a token spike accompanied
by lower `model_selection_match` suggests a routing problem. Stable Action Completion with falling
Agent Efficiency suggests that tasks still finish, but with more work than necessary.

### 4. Drill into evidence

Select a period with a cost or token spike, filter the trace list to that interval, and open a
representative trace. The trend identifies the population; the trace explains the cause.

Consider four combinations:

| Cost | Quality or outcome | Interpretation |
|------|--------------------|----------------|
| High | High | May be justified for difficult or high-risk work |
| High | Low | Investigate first |
| Low | High | Candidate to scale after validating consistency |
| Low | Low | Fails cheaply; not an optimization success |

{{< checkpoint title="Knowledge Check" >}}

A token spike appears, but Traces Count is unchanged. What should you inspect next?

{{< details summary="Click here to see the answer" >}}
Compare input and output tokens, group by model or route, and inspect Agent Efficiency and
`model_selection_match`. Then open traces from the spike to look for larger context, verbose
outputs, retries, loops, or an unexpected model choice.
{{< /details >}}

Attribution tells us where to focus. The next step is to evaluate alternatives before release and
continue checking their quality in production.
