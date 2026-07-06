---
title: Run an Experiment
linkTitle: 2. Run an Experiment
weight: 2
time: 5 minutes
---

With the dataset uploaded, run an experiment. For each row, the script sends the `input` to
the `HealthcareAgent`, collects the response, and scores it with the default metrics.

{{< exercise title="Run a Galileo experiment" >}}

{{< step title="Run with defaults" >}}

From `3-app-with-experiments`, run the experiment against the dataset you just created:

```bash
python experiments/run_experiment.py
```

The script prints the dataset it found, the metrics it will apply, and progress as it works
through the rows. When it finishes, it prints a link/summary for the completed experiment.

{{< /step >}}

{{< step title="Run with a custom name and model" >}}

To compare configurations, give the run a descriptive name and override the model. Running
two experiments, one per model, gives you a side-by-side comparison in the console:

```bash
python experiments/run_experiment.py --experiment-name "lisinopril-eval" --model gpt-4o-mini
```

{{< /step >}}

{{< /exercise >}}

{{% notice title="Default metrics" style="info" %}}

Each experiment scores responses with these built-in Galileo metrics:

* **Ground Truth Adherence**: how closely the response matches the reference `output`.
* **Prompt Injection**: whether the input attempts to subvert the agent's instructions.
* **Chunk Attribution Utilization**: how well retrieved chunks were actually used in the
  answer.
* **Context Adherence**: whether the answer stays grounded in the provided context.

{{% /notice %}}

{{% notice title="How experiments and tracing fit together" style="info" %}}

The experiment runner reuses the **same `HealthcareAgent`** as the chat app. When it provides
an experiment trace context, the agent nests its LangGraph spans under the experiment trace
instead of opening a separate log-stream trace, so each scored row keeps its full span tree.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}

You run the experiment twice with `--model gpt-4o-mini` and `--model gpt-4o`, keeping the
dataset the same. What does this let you conclude?

{{< details summary="Click here to see the answer" >}}
Because the **inputs and metrics are identical** across both runs, any difference in the
scores can be attributed to the **model change**. That's the whole point of an experiment:
hold everything constant except the one variable you're testing.
{{< /details >}}
