---
title: 2. Set Up the Exercise
linkTitle: 2. Set Up the Exercise
weight: 2
time: 5 minutes
---

The companion files are in:

```text
workshop/simple-ai-agent
```

Open a terminal at the root of the workshop repository and run:

```bash
cd workshop/simple-ai-agent
python3 --version
python3 agent_solution.py "Plan my day and draft a customer follow-up"
```

You should see:

* the user request,
* each tool call,
* each tool observation,
* and a final answer.

## Exercise Files

The directory contains four files:

```text
README.md
agent_starter.py
agent_solution.py
profile.json
```

Use `agent_solution.py` to see the completed behavior. Use `agent_starter.py` for the
hands-on edits. Both files use the same structure so you can compare them section by
section:

* `profile.json` is the local data source for the agent.
* `Action`, `Observation`, and `AgentState` define the small data objects used by the loop.
* `lookup_profile`, `create_task`, and `draft_message` are tools.
* `TOOLS` is the allowlist of tools the agent may call.
* `decide_next_action` chooses the next tool or returns `final_answer`.
* `run_agent` connects everything into the agent loop.

## Personalize the Agent

Open `profile.json` and change the sample values so the agent is useful for you:

```json
{
  "name": "Workshop Participant",
  "role": "Site reliability engineer",
  "current_goals": [
    "Reduce alert noise",
    "Prepare a customer reliability review"
  ],
  "communication_style": "clear, direct, and concise",
  "working_hours": "9:00 AM to 5:00 PM"
}
```

Run the solution again after editing the file. The output should reflect your profile.

{{% notice title="Exercise" style="green" icon="running" %}}
Write one request you would want a personal work agent to handle, such as:

```text
Plan my day around a customer incident review and draft a status update.
```

Keep the request specific. Agents work better when the goal and audience are clear.
{{% /notice %}}
