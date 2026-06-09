---
title: 6. Test and Extend
linkTitle: 6. Test and Extend
weight: 6
time: 10 minutes
---

Try a few different requests:

```bash
python3 agent_starter.py "Draft a concise update for my manager"
python3 agent_starter.py "Create a task to review alert noise tomorrow"
python3 agent_starter.py "Plan my day around a reliability review"
```

Watch which tools the agent chooses. The point of the exercise is to make the decision
logic visible.

## Add One More Tool

Add a new tool named `summarize_priorities`.

Suggested behavior:

* Read `current_goals` from the profile.
* Return the top two priorities as a short sentence.
* Register the tool in `TOOLS`.
* Update `decide_next_action` so planning requests call it.

{{% notice title="Stretch Exercise" style="green" icon="running" %}}
Add a fourth tool that is useful for your role. Examples:

* `estimate_meeting_prep`
* `summarize_incident`
* `create_runbook_outline`
* `draft_customer_update`

Keep the tool read-only or draft-only. Do not expose destructive actions in a beginner
agent.
{{% /notice %}}

## Where to Change the Code

To add the new tool, make three small edits:

1. Define the function near the existing tool functions.
2. Add it to the `TOOLS` dictionary.
3. Add a branch in `decide_next_action` that returns `Action("summarize_priorities")`
   when the request asks for planning or priorities.

The pattern is the same for every new tool: define, register, decide when to call it,
then observe the result.

## Production Readiness Checklist

Before using this pattern in a real system, add:

* Authentication and authorization for every tool.
* Input validation and output filtering.
* Approval gates for risky actions.
* Logs, metrics, and traces for agent decisions and tool calls.
* Evaluation tests for expected, unexpected, and adversarial requests.
* Clear retention rules for prompts, responses, and tool observations.
