---
title: Introduction
linkTitle: 2. Introduction
weight: 2
time: 10 minutes
---

Before you instrument anything, it helps to understand the problem agentic systems create,
what Splunk Agent Observability gives you to solve it, and the application you'll be working
with for the rest of the workshop.

{{% notice title="Persona" style="orange" icon="user" %}}

You're an **AI engineer at Careful Health Provider**. Your team is launching an agentic AI
healthcare assistant that answers patient questions about medications and looks up patient
records. Leadership loves the demo, but they're nervous about what happens in production,
where a single hallucinated dosage or leaked record can become a safety incident *and* a
headline. Your job: make the agent's behavior observable, measurable, and safe before and
after it ships.

{{% /notice %}}

> [!splunk] You already have great observability for infrastructure and application
> performance. Agentic AI is different: the failures are about *reasoning, quality, and
> safety*, not just latency and errors. This workshop gives you the tools to see and govern
> that new layer.


Continue to the subsections to understand the challenge, the key concepts, and the
application.
