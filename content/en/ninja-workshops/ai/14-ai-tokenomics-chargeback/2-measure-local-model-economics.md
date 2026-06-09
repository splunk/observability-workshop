---
title: 2. Measure Local Model Economics
weight: 2
---

This is the core lab. You will run a local model, measure prompt and completion
throughput, and convert that throughput into an internal token rate card. No Kubernetes
cluster is required.

## Why Local Throughput Matters

Managed API providers publish token prices because they own the infrastructure and
already know their cost model. For local or self-hosted inference, you have to derive
the economics:

```text
token economics = hourly accelerator cost / observed token throughput
```

That hourly cost can be a public market proxy, an internal amortized hardware cost, an
energy-only lower bound, or a fully loaded platform cost.

## Run Ollama Locally

Ollama's API returns usage metrics that are useful for this lab, including
`prompt_eval_count`, `eval_count`, `prompt_eval_duration`, `eval_duration`, and
`total_duration`.

{{% notice title="Exercise" style="green" icon="running" %}}

Start a local model:

```bash
ollama pull llama3.2:1b
ollama serve
```

In another terminal, run the benchmark with a public GPU hourly proxy:

```bash
python3 workshop/ai-tokenomics-chargeback/scripts/benchmark_ollama.py \
  --model llama3.2:1b \
  --accelerator-hourly-usd 0.80 \
  --power-watts 65 \
  --electricity-usd-per-kwh 0.17 \
  --overhead-percent 15 \
  --iterations 3 \
  --json-out /tmp/local-llm-tokenomics.json
```

If you do not have Ollama installed, pair with another attendee or use the sample JSON
provided by the instructor. The economics model is the same.

{{% /notice %}}

## Choose the Hourly Cost Model

Use one of these models during the lab:

| Cost model | Formula | When to use |
| --- | --- | --- |
| Market proxy | Public GPU endpoint hourly price | Fast workshop estimate across mixed laptops |
| Hardware amortization | `((purchase_price * gpu_allocation_ratio) - residual_value) / useful_life_hours` | Owned laptop or workstation |
| Energy-only | `watts / 1000 * electricity_rate` | Demonstrating the absolute lower bound |
| Fully loaded platform | Hardware + energy + support + license + platform overhead | Production showback or chargeback |

{{% notice title="Exercise" style="green" icon="running" %}}

Run the benchmark again using hardware amortization:

```bash
python3 workshop/ai-tokenomics-chargeback/scripts/benchmark_ollama.py \
  --model llama3.2:1b \
  --accelerator-hourly-usd 0.125 \
  --support-hourly-usd 0.05 \
  --power-watts 65 \
  --electricity-usd-per-kwh 0.17 \
  --overhead-percent 15
```

Compare the derived input, output, and blended token rates with the market proxy run.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Why is energy-only cost usually too low for chargeback?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It ignores hardware purchase cost, useful life, support, licenses, idle capacity,
operations, and platform overhead. It is useful as a lower bound, not as a production
rate.**
{{% /tab %}}
{{< /tabs >}}

## Optional Shared GPU Path

If you have a monitored GPU cluster, you can supplement the local benchmark with
out-of-the-box telemetry:

* **GPU utilization and capacity** - `DCGM_FI_DEV_GPU_UTIL`, `DCGM_FI_DEV_FB_USED`,
  `DCGM_FI_DEV_FB_FREE`, `DCGM_FI_PROF_GR_ENGINE_ACTIVE`, and
  `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE`.
* **GPU power and energy** - `DCGM_FI_DEV_POWER_USAGE` and
  `DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION`.
* **NIM request and token metrics** - `prompt_tokens_total`,
  `generation_tokens_total`, `request_prompt_tokens`, `request_generation_tokens`,
  `time_to_first_token_seconds`, and `time_per_output_token_seconds`.
* **APM and AI traces** - spans that show LLM calls, model names, latency, and token
  details when AI instrumentation is enabled.

The local benchmark produces the rate card. The shared GPU telemetry helps validate
utilization and allocation at platform scale.
