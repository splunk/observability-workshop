# Final Review

## Goal

Turn your investigation into an operator-ready conclusion.

You are done when you can explain what happened, which signals prove it, and what you would change in production.

## Final Evidence Checklist

Confirm you have evidence for each item:

| Evidence | Found? |
| --- | --- |
| Your `deployment.environment` filter works |  |
| ShopMate Sports trace is visible |  |
| Agent spans are visible |  |
| NIM LLM spans are visible |  |
| Token metrics are visible |  |
| GPU metrics are visible |  |
| NIM metrics are visible |  |
| Kubernetes namespace filter works |  |
| Agent-loop scenario is visible |  |

## Final Answer Template

Use this structure for your final answer:

```text
The highest token environment was:

The highest-token conversation was:

The scenario was:

The trace evidence was:

The metric evidence was:

The likely cause was:

The operational recommendation is:
```

## Production Discussion

Think about how this maps to a real AI platform:

- What alert would catch this earlier?
- Should token budget be enforced per request, conversation, or environment?
- Which team owns the fix: app team, platform team, or model-serving team?
- What would Cisco UCS, Nexus, or storage telemetry add if this were a physical AI POD?

## Short Quiz

??? question "A conversation has normal request count but very high token spend. What should you inspect first?"
    Inspect the trace for large prompts, large completions, repeated LLM calls, agent loops, retries, and scenario labels.

??? question "GPU utilization is normal, but one request is very expensive. What does that suggest?"
    The issue may be app orchestration or prompt behavior rather than a GPU capacity problem.

??? question "What is the safest way to capture prompts in this lab?"
    Use only synthetic retail prompts and capture content only in the validated lab mode.

## Exit Criteria

You can leave the lab with three practical skills:

1. Follow one AI request across app, model, GPU, and platform telemetry.
2. Use token metrics to explain AI cost.
3. Diagnose a bounded agent-loop token burn from trace evidence.
