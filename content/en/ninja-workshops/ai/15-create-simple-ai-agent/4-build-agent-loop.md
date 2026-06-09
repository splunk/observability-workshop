---
title: 5. Build the Agent Loop
linkTitle: 5. Build the Agent Loop
weight: 5
time: 15 minutes
---

The agent loop lives in `run_agent`.

Find this section in `agent_starter.py`:

```python
# TODO: call the selected tool, store the observation, and continue the loop.
```

Replace the placeholder with the following logic:

```python
tool = TOOLS[action.tool_name]
observation = tool(profile, **action.arguments)
state.observations.append(
    Observation(tool_name=action.tool_name, result=observation)
)
print(f"tool: {action.tool_name}({action.arguments})")
print(f"observation: {observation}")
```

Here is what each line does:

* `tool = TOOLS[action.tool_name]` finds the Python function selected by
  `decide_next_action`.
* `tool(profile, **action.arguments)` calls that function. The `**` operator turns the
  action's argument dictionary into named Python arguments.
* `state.observations.append(...)` records the tool result so future decisions and the
  final answer can use it.
* The two `print` lines make the agent trace visible in the terminal.

The loop should now:

1. Ask `decide_next_action` what to do next.
2. Stop when the action is `final_answer`.
3. Call the selected tool.
4. Store the observation.
5. Continue until a final answer is ready.

## Run the Starter

Run:

```bash
python3 agent_starter.py "Plan my day and draft a customer follow-up"
```

Expected behavior:

* The agent looks up your goals or communication style.
* The agent creates at least one task.
* The agent drafts a message.
* The agent returns a final answer that summarizes the work.

## Why the Loop Has a Step Limit

The loop uses:

```python
for _ in range(5):
```

That maximum protects the program from running forever. Real AI agents should always have
limits such as maximum steps, maximum tool calls, maximum cost, or maximum runtime.

## Why Observations Are Stored

After each tool call, the result is appended to `state.observations`. This serves three
purposes:

* The decision function can see which tools already ran.
* The final answer can summarize the work performed.
* In a monitored system, each observation can become trace, log, or evaluation data.

{{% notice title="Troubleshooting" style="info" %}}
If the starter does not run, compare your file with
`workshop/simple-ai-agent/agent_solution.py`. The solution is intentionally compact so
you can inspect the complete loop in one place.
{{% /notice %}}
