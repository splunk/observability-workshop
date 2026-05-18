---
title: 1. Scenario 1 — Log-First Triage
weight: 1
---

In many real-world incidents, the first signal is an alert or a report from a user — not a trace or a dashboard. The responder opens their logging tool and starts investigating. This is the **log-first** approach, and it's how this scenario works.

Unlike a sequential RUM → APM → Logs path where you arrive at logs with context already established, here you start with a blank slate in Log Observer. No prior trace context. No service map. Just logs and your investigative skills.

## The 3 Pillars — Inverted

In a typical observability workflow, you might follow this order:

| Metrics | Traces | Logs |
| :---: | :---: | :---: |
| _**Do I have a problem?**_ | _**Where is the problem?**_ | _**What is the problem?**_ |

In this scenario, we **start at the end** — directly in logs — and work backwards:

1. **What is the problem?** — Filter and inspect log entries to find the error
2. **Where is the problem?** — Identify which service and version is responsible
3. **Do I have a problem?** — Confirm the scope and timeline of the issue

## Investigation Flow

You will follow these steps:

1. Open Log Observer and set your filters
2. Group by severity and filter to errors
3. Identify the failing service
4. Analyze the error timeline and patterns
5. Inspect a log entry to determine the root cause
