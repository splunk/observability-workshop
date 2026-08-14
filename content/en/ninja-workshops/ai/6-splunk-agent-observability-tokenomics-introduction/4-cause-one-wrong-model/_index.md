---
title: Cause 1 — The Wrong Model
linkTitle: 4. Choose the Right Model
weight: 4
time: 15 minutes
---

A fair bake-off controls the workload. If we change the model, prompt, dataset, and retrieval
settings at once, we cannot explain the result. In this comparison, both experiments receive the
same 18 product questions, retrieved context, and evaluators. The model is the variable.

Open **Experiment Groups > Product Model Comparison**, select the two experiments, and switch to
**Compare**.

### 1. Compare the response generations

Open the input asking whether the Femella Women Gold Shirt is eligible for exchange. Both models
receive product context that explicitly says `Exchangeable: yes`.

The inexpensive model answers:

> Yes, we offer exchanges on many of our items.

The expensive model answers the specific question directly, confirms that this shirt is eligible,
and adds the available return, try-and-buy, and store-pickup options.

What do you notice about the two answers? The first is concise but does not confirm the requested
product. The second is more useful, but it is also longer.

### 2. Compare quality

Expand **Trace Evaluators** for the two results:

| Evaluator | Inexpensive model | Expensive model |
|-----------|-------------------|-----------------|
| Context Adherence | 1.00 | 1.00 |
| Ground Truth Adherence | false | true |

Both responses are consistent with the retrieved context, but only one satisfies the expected
answer. Context adherence alone does not prove that the user's task was completed.

### 3. Compare tokens, latency, and cost

| System metric | Inexpensive model | Expensive model |
|---------------|-------------------|-----------------|
| Input tokens | 279 | 298 |
| Output tokens | 12 | 59 |
| Total tokens | 291 | 357 |
| Latency | 292 ms | 2.36 sec |
| Agent cost | less than $0.0001 | $0.0026 |

These values describe this single prepared comparison; they are not universal model benchmarks.
The inexpensive model is faster and cheaper here, but it fails Ground Truth Adherence. The
expensive model completes the task, but costs more and produces a longer answer.

> Token efficiency is not always proportional to price or token count. A response that uses fewer
> tokens but does not complete the task may create another user turn, an escalation, or an
> abandoned journey.

### 4. Decide how to route

Which choice would you make?

1. Send every request to the inexpensive model.
2. Send every request to the expensive model.
3. Route by task complexity and required quality.

A configuration should advance only when it:

1. Meets the defined quality and safety thresholds.
2. Improves cost, latency, or both for the target task.
3. Remains consistent across the dataset, not just one favorable example.

{{< checkpoint title="Knowledge Check" >}}

Why is the inexpensive response not the token-efficient winner, despite using fewer tokens and
costing less?

{{< details summary="Click here to see the answer" >}}
It does not complete the user's task. Ground Truth Adherence is false because the response talks
about exchanges generally without confirming whether the specific shirt is eligible. Efficiency
must include the outcome, not just consumption.
{{< /details >}}

Do not conclude that larger models are always better. The right model is workload-specific and
should be selected with controlled, repeatable evidence.

Next, suppose we selected the right model and the request is still expensive. The next suspect is
the workflow wrapped around it.
