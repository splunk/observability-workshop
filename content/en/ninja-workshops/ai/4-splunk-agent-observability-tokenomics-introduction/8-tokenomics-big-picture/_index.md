---
title: Tokenomics - The Big Picture
linkTitle: 8. Tokenomics - The Big Picture
weight: 8
time: 10 minutes
description: Understanding token utilization at a company level.
---

This workshop so far has optimized tokens for one agent: finding the right model, having a workflow without waste, 
getting evals costs under control,... but that one agent doesn't run in isolation. It runs inside a company where 
dozens of teams are also using AI; not just to run agents in production, but to build them. And to build all kinds
of applications. Claude Code, Cursor, GitHub Copilot, Codex: they are writing code, generating tests, and 
shipping features today, billed per seat or by usage, on an invoice that most engineering organizations are not 
watching as closely as they should.

### 1. The Risk is as Big as the Opportunity

Early in this workshop, we've seen a few horror tales of companies that learned the hard way that token 
spending can easily spiral out of control. The culture of *'Tokenmaxxing'*, short-lived as it was, established 
the idea that spending more tokens for the sake of spending more tokens was a good idea. Once the bill arrived, 
however, without any equally impressive increases in quality or speed, that notion was quickly reevaluated.

Per-token prices are expected to drop by **90%** in the next few years. However, agentic workloads (especially)
are expected to cause an increase in token consumption of **24x** through the end of the decade. Cheaper tokens do 
not mean cheaper AI; instead, it means more of it, used in more places, by more people, faster than most 
budgeting processes could track. This pervasive approach will generate a myriad of new opportunities, and 
a new type of cost that needs to be tracked, controlled and scrutinized: token spending.

Engineering organizations already started to identify this risk: in more extreme cases, teams that burn an entire year's
AI budget in a few months, or that at first pushing engineers towards more token spending, only to retract and having to 
cap spend per engineer. We've also seen companies pulling back the majority of their coding-assistant licenses after a 
period of unmetered use. Unfortunately, these are not edge cases anymore, and they're not isolated to high-tech 
companies. They're becoming common enough that a "FinOps for tokens" discipline is starting to get its own name in the 
industry.

### 2. The Same Three Questions, at Enterprise Level

This workshop has been asking three questions about our AI Shoping Assistant: 1. is the model right, 2. is the workflow 
optimized, 3. is the spend producing outcomes. Those questions also make sense at a high level, as we look into the
Enterprise AI coding assistants spread across the company:

* **Where is the spend going?** Attributed by tool, by team, by individual; not just a lump sum on a vendor invoice.
* **What spend is wasted?** Idle seats, abandoned sessions, expensive models used for simple tasks; the coding-assistant 
equivalent of the workflow waste you found with spans and Agent Efficiency earlier in this workshop.
* **What spend is working?** Which teams are shipping more, faster, with fewer regressions, because of the assistant 
they're paying for — not just how many tokens they burned.

A bill from the LLM provider answers none of these. It shows the total; it doesn't show whether the total was worth it.

Right now, most companies have siloed control over these cost aspects: the agents that are running live, being monitored
by an observability platform, while AI coding-assistant spend lives in a spreadsheet somewhere in finance or procurement, 
disconnected from any signal about whether that spend is producing good outcomes.

Tokenomics, powered by Splunk Agent Observability, aims to close that gap.

### 3. Introducing Tokenomics, Powered by Splunk Agent Observability

Tokenomics is a new solution, and as such, it will see rapid evolution over time.

It works by connecting to the billing API of the service providers, such as Claude, Codex, Cursor, Copilot, etc, 
to retrieve spending data. In parallel, it can leverage HR or organizational data to correlate users and orgs with 
token spending, providing ways to filter and segment investigation by provider, department, team, user etc.

Trends are also calculated in a *heatmap* view, allowing us to understand the spending habits of different organizations, 
departments and teams, with the ability to further segment by provider. For instance, the Advanced Research department
has increased their Codex spending by 20% this month, while lowering their Claude costs by 60% during the same period.

The vision and roadmap for this solution is very ambitious and exciting; we will share more information about it as
new releases approach.

Next, we'll see a quick walkthrough of the Tokenomics solution, provided by your presenter.


> The bill tells you what was spent. Tokenomics tells you whether it was worth it — for one agent,
> or for every AI tool the company runs.

{{< checkpoint title="Knowledge Check" >}}

If your engineering organization adopted three different AI coding assistants tomorrow, what's the
first question you'd want a company-level Tokenomics dashboard to answer?

{{< details summary="Click here to see the answer" >}}
There's no single right answer, but it should map to one of the three questions above: which team
or tool is driving the spend (attribution), whether any of that spend is going to idle seats or
abandoned sessions (waste), or whether the teams spending the most are also shipping the most
(outcomes). Most organizations start with attribution, because it's the one question a raw invoice
can't answer at all — but the real payoff comes from connecting spend to outcomes, the same way
you connected token cost to Action Completion earlier in this workshop.
{{< /details >}}

<hr>

We've gone all the way from a single trace to a company-wide ledger. Time to close the loop.