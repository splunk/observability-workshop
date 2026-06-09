---
title: 1. Define the Chargeback Model
weight: 1
---

Chargeback works only when the telemetry answers the same questions that finance,
platform engineering, and application teams are asking. Before opening a dashboard,
define the dimensions and cost rules that every chart will use.

## Tokenomics vs. Chargeback

**Tokenomics** explains how tokens are consumed: prompt tokens, completion tokens,
requests, model mix, latency, context size, and user or tenant behavior.

**Chargeback** maps that consumption to an owner and a rate card. In this workshop, that
owner is a team, tenant, cost center, workload, and model. Your organization might use
different names, but the pattern is the same.

## Required Dimensions

Use low-cardinality, stable dimensions. Do not put prompt text, user email addresses,
session IDs, request IDs, or raw account names on metrics.

| Dimension | Purpose | Example |
| --- | --- | --- |
| `ai.team` | Team accountable for cost | `support-ai` |
| `ai.cost_center` | Finance allocation code | `cc-ml-1200` |
| `ai.tenant.id` | Customer, business unit, or internal tenant | `tenant-enterprise` |
| `ai.workload.name` | AI application or workflow | `support-rag` |
| `ai.product_area` | Product or business capability | `customer-support` |
| `gen_ai.request.model` | Model used for the request | `meta/llama-3.2-1b-instruct` |
| `deployment.environment` | Environment boundary | `production` |
| `k8s.cluster.name` | Infrastructure boundary | `ai-pod-workshop-participant-1` |

## Cost Pools

Separate cost pools by how the cost is created:

* **Token cost** - input and output tokens multiplied by a model rate card.
* **GPU capacity cost** - GPU-hours, reservation cost, or internal platform rate.
* **GPU energy cost** - optional energy allocation from DCGM power or energy metrics.
* **Platform overhead** - shared collector, vector database, storage, networking, and
  operational overhead.

## Where Rate Card Values Come From

A workshop rate card should be simple, but it should not be random. Use one of these
sources depending on how the AI workload is hosted:

| Hosting model | Where to get the rate | Workshop use |
| --- | --- | --- |
| Managed API model | Provider pricing page with input, cached input, output, tool, and request rates | Direct token cost |
| GitHub Copilot-style usage | Model token rates converted into credits or dollars | Example of token-based internal billing |
| Hugging Face Inference Providers | Provider pass-through token rates and usage breakdown | Managed model showback |
| Hugging Face Inference Endpoints | GPU instance hourly rates, billed by running endpoint time | Dedicated GPU pool cost |
| Self-hosted NIM or vLLM | Cloud GPU hourly cost, reserved capacity cost, license cost, and platform overhead | Internal GPU allocation |

The workshop includes a starter file you can copy and edit:

```text
workshop/ai-tokenomics-chargeback/rate-card-example.yaml
```

{{% notice title="Exercise" style="green" icon="running" %}}

Create a simple workshop rate card before continuing:

1. Pick one token model example from the rate-card file.
2. Pick one GPU hourly example from the rate-card file.
3. Confirm the currency is `USD`.
4. Confirm the rate-card version, for example `workshop-2026-06`.
5. Decide whether shared platform overhead is included. The workshop uses `15%`.

For a short lab, this is enough:

| Cost element | Workshop value |
| --- | --- |
| Input token rate | `$0.20` per 1,000,000 tokens |
| Output token rate | `$1.25` per 1,000,000 tokens |
| GPU platform rate | `$5.00` per GPU-hour |
| Shared platform overhead | `15%` of token plus GPU cost |

Then decide which attribution dimensions are mandatory for your lab:

1. Choose one primary owner dimension: `ai.team` or `ai.tenant.id`.
2. Choose one finance dimension: `ai.cost_center`.
3. Choose one workload dimension: `ai.workload.name`.
4. Choose the model dimension: `gen_ai.request.model`.
5. Write down the default value you will use when an application does not provide one.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Why not use `user.id` as the main chargeback dimension?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It usually creates high-cardinality metrics and weak finance ownership. Use stable
team, tenant, workload, and cost center dimensions for chargeback.**
{{% /tab %}}
{{< /tabs >}}
