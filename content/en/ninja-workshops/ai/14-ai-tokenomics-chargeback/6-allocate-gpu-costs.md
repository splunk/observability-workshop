---
title: 6. Allocate GPU Costs
weight: 6
---

Token cost is directly attributable when the application reports owner dimensions.
GPU cost is usually a shared pool. A single GPU might serve many teams through one NIM
deployment, or a team might reserve GPUs that sit idle. Your allocation model must match
how the platform is operated.

## Allocation Options

| Model | Best for | Tradeoff |
| --- | --- | --- |
| Reservation-based | Dedicated GPU quotas or namespaces | Simple, but charges idle capacity to the owner |
| Token-weighted | Shared model serving with good token telemetry | Fair for LLM serving, but ignores non-token GPU work |
| Request-time weighted | Request traces include model latency and owner | Better for mixed request cost, but needs consistent traces |
| Energy-weighted | DCGM power or energy data is trusted | Good for sustainability reporting, but still needs attribution |

For a workshop, use token-weighted allocation:

```text
team_gpu_cost = gpu_pool_cost * team_tokens / all_tokens
```

For production, decide whether idle GPU capacity is platform overhead, charged to
reserved tenants, or allocated proportionally across active consumers.

## GPU Metrics to Review

The Cisco AI Pods collector examples already include the GPU metrics used for
allocation and efficiency:

* `DCGM_FI_DEV_GPU_UTIL`
* `DCGM_FI_DEV_FB_USED`
* `DCGM_FI_DEV_POWER_USAGE`
* `DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION`
* `DCGM_FI_PROF_GR_ENGINE_ACTIVE`
* `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE`

{{% notice title="Exercise" style="green" icon="running" %}}

Build a GPU pool view:

1. Open the `Cisco AI PODs Dashboard`.
2. Filter to your cluster.
3. Note the number of GPUs and average GPU utilization.
4. In Metric Finder, open `DCGM_FI_DEV_GPU_UTIL` and group by node or GPU identifier.
5. Open `DCGM_FI_DEV_POWER_USAGE` and compare power use with utilization.
6. Record the workshop GPU platform rate from your rate card.

<!-- TODO screenshot: GPU utilization and power usage grouped by GPU or node. -->
![GPU utilization and power grouped by GPU](images/gpu-utilization-power.png)

{{% /notice %}}

## Allocate the Cost

In a dashboard, show the allocation in two steps:

1. GPU pool cost:

```text
gpu_pool_cost = gpu_count * gpu_hourly_rate * hours
```

2. Team allocation:

```text
team_gpu_cost = gpu_pool_cost * team_tokens / sum(all_team_tokens)
```

The first value can come from an internal rate card, a custom metric, or a dashboard
constant. The second value comes from the custom token metrics you added in the previous
section.

{{% notice title="Exercise" style="green" icon="running" %}}

Add GPU allocation charts to the dashboard:

1. Add a single value for GPU pool cost over the selected time range.
2. Add a chart for token share by team.
3. Add a chart for allocated GPU cost by team.
4. Add a chart for GPU utilization next to allocated cost.
5. Add a table that shows `ai.team`, tokens, token cost, allocated GPU cost, and total
   estimated cost.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
**Why show GPU utilization next to chargeback cost?**
{{% /tab %}}
{{% tab title="Answer" %}}
**It separates cost ownership from efficiency. A team can be charged for usage while the
platform team still sees idle or saturated GPU capacity.**
{{% /tab %}}
{{< /tabs >}}
