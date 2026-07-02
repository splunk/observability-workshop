---
title: Run Experiments Before Release
linkTitle: 7. Run Experiments
weight: 7
time: 20 minutes
---

So far you've observed the agent in production. **Experiments** flip that around: they let you
evaluate the agent *before* you ship, against a fixed dataset, so you catch regressions before
your users do.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you're about to change a prompt and try a
different model. You need objective proof that quality improved, not a gut feel from a few
sample answers. Experiments give you a repeatable, scored benchmark you can stand behind.

{{% /notice %}}

> [!splunk] Without systematic evaluation, every deployment is a leap of faith and regressions
> stay invisible until a user complains. **Experiments replace intuition with evidence**:
> consistent, reproducible, and comparable. Use them as a release gate, or to compare variants
> (prompt, model, configuration) and pick the best combination.

{{% notice title="Where to work" style="info" %}}

This chapter works in `~/workshop/healthcare-assistant/3-app-with-experiments`. It builds on
the instrumented app and adds an `experiments/` package plus a `dataset.csv`. The experiment
runner uses the **same `HealthcareAgent`** as the chat app, so the spans you've been exploring
also appear under each experiment run. The folder ships complete, so it doubles as the
reference for this chapter.

{{% /notice %}}

Continue to the subsections to create a dataset, run an experiment, and review the results.
