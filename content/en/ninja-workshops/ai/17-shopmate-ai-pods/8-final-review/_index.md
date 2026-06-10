---
title: Final Review
linkTitle: 8. Final Review
weight: 8
archetype: chapter
time: 15 minutes
description: Convert your trace, metric, GPU, NIM, and tokenomics findings into an operator-ready conclusion.
---

You are done when you can explain what happened, which signals prove it, and what you would change in production.

## Final Evidence Checklist

Confirm you have evidence for each item:

| Evidence | Found? |
| --- | --- |
| Your `deployment.environment` filter works | |
| ShopMate Sports trace is visible | |
| Agent spans are visible | |
| NIM LLM spans are visible | |
| Token metrics are visible | |
| GPU metrics are visible | |
| NIM metrics are visible | |
| Kubernetes namespace filter works | |
| Expensive or repeated-agent scenario is visible | |

## Final Answer Template

Use this structure:

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

Discuss:

- What alert would catch this earlier?
- Should token budget be enforced per request, conversation, or environment?
- Which team owns the fix: app team, platform team, or model-serving team?
- What would Cisco UCS, Nexus, storage, or AI Defense telemetry add if this were a full physical AI POD deployment?

## Exit Criteria

You leave the lab with three practical skills:

1. Follow one AI request across app, model, GPU, and platform telemetry.
2. Use token metrics to explain AI cost.
3. Diagnose bounded agent-loop token burn from trace evidence.
