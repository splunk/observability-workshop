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
| `gen_ai.request.model` | Model used for the request | `llama3.2:1b` |
| `deployment.environment` | Environment boundary | `local-workshop` |
| `host.name` or `k8s.cluster.name` | Infrastructure boundary | `mk-laptop` |

## Cost Pools

Separate cost pools by how the cost is created:

* **Token cost** - input and output tokens multiplied by a model rate card.
* **Accelerator capacity cost** - GPU-hours, laptop/workstation amortization,
  reservation cost, or internal platform rate.
* **Energy cost** - optional energy allocation from measured or estimated power draw.
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
| Local Ollama, llama.cpp, vLLM, or NIM | Observed token throughput plus an hourly accelerator cost model | Internal token economics |
| Self-hosted NIM or vLLM on a cluster | Cloud GPU hourly cost, reserved capacity cost, license cost, and platform overhead | Shared GPU allocation |

The workshop includes a starter file you can copy and edit:

```text
workshop/ai-tokenomics-chargeback/rate-card-example.yaml
```

{{% notice title="Exercise" style="green" icon="running" %}}

Create a simple workshop rate card before continuing. For this lab, derive the token
rates from local throughput instead of copying a managed API token price:

1. Pick a local model, for example `llama3.2:1b`.
2. Pick an hourly cost model:
   * **Market proxy** - use a public GPU hourly price for a comparable endpoint.
   * **Hardware amortization** - use laptop/workstation purchase price, useful life,
     and residual value.
   * **Energy-only** - use power draw and electricity cost to show the lower bound.
3. Confirm the currency is `USD`.
4. Confirm the rate-card version, for example `workshop-2026-06`.
5. Decide whether shared platform overhead is included. The workshop uses `15%`.

For a short lab, this is enough:

| Cost element | Workshop value |
| --- | --- |
| Local model | `llama3.2:1b` |
| Hourly accelerator proxy | `$0.80` per GPU-hour |
| Energy estimate | `65 W` at `$0.17` per kWh |
| Shared platform overhead | `15%` |
| Derived input token rate | Calculated by the benchmark |
| Derived output token rate | Calculated by the benchmark |

The benchmark uses this formula:

```text
effective_hourly_cost =
  (accelerator_hourly_usd + support_hourly_usd + energy_hourly_usd)
  * (1 + overhead_percent / 100)

input_usd_per_1m =
  effective_hourly_cost * (prompt_eval_seconds / 3600)
  / prompt_tokens * 1,000,000

output_usd_per_1m =
  effective_hourly_cost * (completion_eval_seconds / 3600)
  / completion_tokens * 1,000,000
```

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
