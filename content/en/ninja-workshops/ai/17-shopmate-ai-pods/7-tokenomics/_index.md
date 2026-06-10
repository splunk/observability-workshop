---
title: Tokenomics
linkTitle: 7. Tokenomics
weight: 7
archetype: chapter
time: 50 minutes
description: Investigate token usage, expensive conversations, and bounded agent-loop patterns.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **cost and reliability analyst**. Your goal is to explain which request pattern consumed the most tokens and why.
{{% /notice %}}

## Operator Question

Answer this by the end of the module:

```text
Which lab environment and request pattern consumed the most tokens, and why?
```

## Tokenomics Fields

Start with the standard filters:

```text
service.name=shopmate-ai
deployment.environment=<your student id>
```

Token metric names can vary by package version and tenant. Look for names such as:

- `gen_ai.client.token.usage`
- `gen_ai.usage.input_tokens`
- `gen_ai.usage.output_tokens`

Use the names visible in your Splunk tenant.

## Run A Baseline Conversation

Send two turns in the ShopMate assistant:

```text
Turn 1: Find a waterproof jacket under $200 for a weekend hiking trip.
Turn 2: Compare the top two options and check if medium is in stock.
```

Validate:

- Token fields exist in traces or metrics.
- `deployment.environment` is present.
- The trace appears under `service.name=shopmate-ai`.

## Run A Token Surge Conversation

Send a longer fictional retail conversation:

```text
Turn 1: Build a complete race-weekend gear kit for two runners with different budgets.
Turn 2: Compare road shoes, trail shoes, shorts, and hydration pack options.
Turn 3: Add delivery timing constraints, pickup options, and return policy requirements.
Turn 4: Rewrite the recommendation as a detailed email to a running club coach.
Turn 5: Summarize the decision in five bullets and include estimated savings.
```

Expected result:

- Token totals increase.
- The conversation is more expensive than the baseline.
- Traces show larger prompt or completion token values.

## Run The Expensive Agent Request

Send:

```text
Find waterproof trail running shoes under $40, available today, with carbon plate support, in every color, and explain all alternatives in detail.
```

Validate:

- The request returns instead of running indefinitely.
- The trace shows OpenAI Agents SDK activity.
- The trace shows NIM-backed LLM spans.
- Token totals are higher than the baseline.
- Repeated agent or NIM spans, latency, and token totals support any agent-loop conclusion.

## Build The Cost Explanation

In Splunk Observability Cloud:

1. Filter to `service.name=shopmate-ai`.
2. Filter to `deployment.environment=<your student id>`.
3. Find token usage for your environment.
4. Split prompt tokens and completion tokens if both are available.
5. Compare baseline, surge, and expensive-agent request traces.

Record:

| Scenario | Highest token signal | Trace evidence | Likely cause |
| --- | --- | --- | --- |
| Baseline | | | |
| Token surge | | | |
| Expensive agent request | | | |

## Recommendation

Write one operational recommendation:

```text
The highest token pattern was <scenario>. The evidence was <trace and metric signals>. The likely cause was <prompt size, completion size, repeated tool calls, retries, or bounded agent loop>. I recommend <guardrail, alert, budget, prompt change, or owner action>.
```
