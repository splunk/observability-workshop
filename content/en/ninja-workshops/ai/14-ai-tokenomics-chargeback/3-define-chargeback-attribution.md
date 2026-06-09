---
title: 3. Define Chargeback Attribution
weight: 3
---

This section turns the workshop model into telemetry standards. The standard should be
small enough that application teams can implement it consistently, and strict enough
that platform and finance teams can trust the dashboards.

## Attribute Contract

Use the same attributes on spans, metrics, and logs wherever possible:

```text
ai.team
ai.cost_center
ai.tenant.id
ai.workload.name
ai.product_area
gen_ai.request.model
deployment.environment
k8s.cluster.name
service.name
```

For request traces, add the attributes to the current span before or immediately after
the LLM call. For metrics, use them as metric attributes on custom token and cost
counters.

## Metric Contract

The workshop companion files under `workshop/ai-tokenomics-chargeback` use these custom
metrics:

| Metric | Type | Unit | Purpose |
| --- | --- | --- | --- |
| `ai.tokens.input` | Counter | `{token}` | Prompt tokens attributed to owner dimensions |
| `ai.tokens.output` | Counter | `{token}` | Completion tokens attributed to owner dimensions |
| `ai.tokens.total` | Counter | `{token}` | Total tokens attributed to owner dimensions |
| `ai.request.estimated_cost_usd` | Counter | `USD` | Estimated request cost from the workshop rate card |
| `ai.request.count` | Counter | `{request}` | Requests included in chargeback |

{{% notice title="Exercise" style="green" icon="running" %}}

Create an attribution checklist for your application:

1. Confirm where tenant or business unit is known: request header, JWT claim, API key,
   route, namespace, or deployment.
2. Confirm where team and cost center are known: deployment metadata, environment
   variable, service catalog, or configuration file.
3. Confirm where model name is known: application configuration, LLM client response,
   span attributes, or NIM metric labels.
4. Confirm where token usage is known: LLM response metadata, framework callback,
   OpenTelemetry GenAI span attributes, or NIM metrics.
5. Mark any field that is unknown at request time. Unknown values must use a controlled
   value such as `unknown`, not a blank string.

{{% /notice %}}

## Cardinality Guardrails

Tokenomics data can become expensive if every request carries unique dimensions. Apply
these rules before sending metrics:

* Use `ai.tenant.id`, not `enduser.id`.
* Use a normalized workload name, not a URL path with IDs.
* Use model family and model name; avoid dynamic deployment IDs unless they are bounded.
* Keep prompt category if useful, but never send prompt text as a metric dimension.
* Put high-cardinality details in traces or logs only when security policy allows it.

{{% notice title="Production Note" style="info" %}}
The sample instrumentation records request cost in the application. In production, many
teams prefer to record raw token counters and calculate cost centrally so rate card
changes do not require application redeploys. Both patterns work; choose one owner for
the rate card.
{{% /notice %}}
