---
title: Bring It Home
linkTitle: 9. Bring It Home
weight: 9
time: 5 minutes
description: Close the tokenomics tour with a final, company-wide takeaway.
---

At the beginning of this workshop, we had a bill from our LLM provider that told us how much was spent, 
but not whether those expensive tokens created value.

Now we arrive at the end with a ledger that does both — for the agents we build, and for the AI code 
assistants spread across the company.

## The Journey

* **Instrument** everything: spans and traces are the raw material for the visibility we want to have.
* **Ask what outcomes you got for the tokens spent**, not just how many were used.
* **Find the three usual culprits**: the wrong model, an over-engineered workflow, spend that
  isn't tied to outcomes.
* **Use Proactive tools to find new culprits**: not every wasteful and damaging behavior will be
predictable; looking for a needle in the haystack is not an efficient proposition; instead, leverage 
the out-of-the-box capabilities of Splunk Agent Observability to automatically surface trends and
behaviors that could be compromising the cost and quality of your AI agents.
* **Evaluate at scale without going broke** — Luna makes 100% eval coverage affordable. Agents simply
should not go into Production with anything less than full eval visibility.
* **Zoom out**: uncontrolled AI spending only benefits the LLM providers. The same questions we ask of
an agent (where's it going, what's wasted, what's working) apply just as well to every AI coding assistant 
across the company. Centralizing and correlating this data is the cherry on top.

## Closing Remarks

AI agents and AI coding assistants are, without exaggeration, some of the most useful tools ever handed to 
engineering teams. They are also one of the easiest ways to lose control of a budget without anyone noticing 
until the invoice arrives. Those two facts aren't in tension, they are the same fact. The tools are worth 
using *because* they're powerful, and worth watching *because* they're powerful.

Splunk Agent Observability and Tokenomics exist so nobody has to choose between adopting AI and controlling 
its cost. One trace, one dashboard, one system of record: for the agents you build, and for the assistants 
that are being used by the teams to build everything else.

{{< checkpoint title="Final Reflection" >}}

Of everything in this workshop, what's the first thing you'll go instrument, evaluate, or ask your
team about, when you get back to your desk?

{{< details summary="Here's a starting point" >}}
Pick whichever is closest to a real gap you already suspect: a trace showing where an agent's
tokens actually go, an eval that would catch a quality regression before a customer does, or a
straight answer to "how much are we spending on AI coding assistants, and which teams are the
top spenders?"
{{< /details >}}

> Do not optimize tokens in isolation. Optimize the outcomes you get for them — one agent at a
> time, or one company at a time.

## References

* [Splunk Agent Observability documentation](https://agent-observability-docs.splunk.com/)
* [Splunk Agent Observability Quickstart](https://agent-observability-docs.splunk.com/what-is-splunk-agent-observability)
* [Splunk Agent Observability - Luna Model](https://agent-observability-docs.splunk.com/concepts/luna/luna)

{{< checkpoint title="This is the end of the workshop! Thank you for participating!" >}}