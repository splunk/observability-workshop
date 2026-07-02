---
title: Enable Quality Metrics
linkTitle: 5. Enable Quality Metrics
weight: 5
time: 10 minutes
---

Reading traces one at a time is great for an incident, but it doesn't scale. **Quality
metrics** automatically evaluate your agent's interactions so problems (hallucinations,
tool-selection errors, prompt injections) surface on their own.

{{% notice title="Persona" style="orange" icon="user" %}}

As Careful Health Provider's **AI engineer**, you want to know the moment the assistant
produces an ungrounded medical answer, not when it trends on social media. Out-of-the-box
metrics give you that early-warning system across every request.

{{% /notice %}}

> [!splunk] **Accurate evaluations.** Splunk Agent Observability ships out-of-the-box metrics
> that evaluate agent, output, and RAG quality, so you can quickly spot problems, track
> improvements, and make your agentic applications work better for your users.

{{% notice title="Evaluations that scale, powered by Luna" style="info" %}}

Using a large general-purpose LLM as a judge gets expensive and slow fast, so most teams
sample a fraction of traffic and leave the rest unscored. Splunk Agent Observability uses
**Luna** Small Language Models, purpose-built and fine-tuned for evaluation, to score quality
at a fraction of the cost and latency. That means you can evaluate *all* of your production
traffic (not a 5–10% sample) and even run evaluations fast enough for real-time guardrails.

{{% /notice %}}

Continue to enable metrics on your log stream and review the scores.
