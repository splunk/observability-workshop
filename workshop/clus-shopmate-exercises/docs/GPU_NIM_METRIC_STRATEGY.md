# GPU and NIM Metric Strategy

## Purpose

This document defines which NVIDIA GPU and NVIDIA NIM metrics student collectors should scrape for the workshop.

The goal is to get as close as practical to the original Cisco AI Pods workshop behavior and to maximize the chance that Splunk out-of-the-box AI infrastructure dashboards populate.

## Decision

Use the original workshop-style NVIDIA metric allowlist as the default.

Reason:

- the original workshop states that the filter includes metrics used by dashboard charts or alert detectors
- the built-in dashboard experience is more likely to populate when the same metric names are sent
- reducing the list too early risks breaking unknown dashboard panels

Use a smaller allowlist only as a fallback if cost, ingest volume, or lab performance becomes a problem.

## Student Collector Pattern

Each student collector will scrape:

- shared NVIDIA DCGM exporter endpoint on port `9400`
- shared NVIDIA NIM metrics endpoint on port `8000` path `/v1/metrics`

Each student collector will add student-specific resource attributes:

- `student.id`
- `team.name`
- `k8s.namespace.name`
- `deployment.environment`
- `k8s.cluster.name`

Important:

- students do not get dedicated GPUs
- students get a logical metrics view from shared GPUs/NIM endpoints
- the instructor should explain that duplicate scraping is acceptable for a lab but not the preferred production design

## Default Metric Allowlist

Use this list first.

### DCGM GPU metrics

| Metric | Why collect it |
|---|---|
| `DCGM_FI_DEV_FB_FREE` | Shows available GPU framebuffer memory. Useful for memory pressure and capacity conversations. |
| `DCGM_FI_DEV_FB_USED` | Shows used GPU framebuffer memory. Critical for understanding model footprint and workload saturation. |
| `DCGM_FI_DEV_GPU_TEMP` | Shows GPU temperature. Useful for hardware health and thermal throttling discussion. |
| `DCGM_FI_DEV_GPU_UTIL` | Primary GPU utilization metric. Most important high-level signal for GPU workload pressure. |
| `DCGM_FI_DEV_MEM_CLOCK` | Shows memory clock behavior. Useful when explaining hardware-level GPU performance signals. |
| `DCGM_FI_DEV_MEM_COPY_UTIL` | Indicates memory copy activity. Helps distinguish compute pressure from memory-transfer pressure. |
| `DCGM_FI_DEV_MEMORY_TEMP` | Shows GPU memory temperature. Useful for thermal health. |
| `DCGM_FI_DEV_POWER_USAGE` | Shows GPU power draw. Useful for efficiency and capacity planning discussion. |
| `DCGM_FI_DEV_SM_CLOCK` | Shows streaming multiprocessor clock. Useful for performance and throttling context. |
| `DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION` | Shows cumulative GPU energy consumption. Useful for cost/efficiency conversation. |
| `DCGM_FI_PROF_DRAM_ACTIVE` | Indicates DRAM activity. Useful for memory-bound workload analysis. |
| `DCGM_FI_PROF_GR_ENGINE_ACTIVE` | Indicates graphics/compute engine activity. Useful for workload activity and saturation. |
| `DCGM_FI_PROF_PCIE_RX_BYTES` | Shows PCIe receive traffic. Useful for host-to-GPU data movement analysis. |
| `DCGM_FI_PROF_PCIE_TX_BYTES` | Shows PCIe transmit traffic. Useful for GPU-to-host data movement analysis. |
| `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` | Indicates tensor core activity. Important for AI workload acceleration visibility. |

### NIM inference metrics

| Metric | Why collect it |
|---|---|
| `num_request_max` | Shows configured/request capacity context for the model server. |
| `num_requests_running` | Shows active in-flight inference requests. Useful for concurrency and saturation. |
| `num_requests_waiting` | Shows queued inference requests. Critical for latency and overload analysis. |
| `prompt_tokens_total` | Cumulative prompt token count. Core tokenomics input. |
| `generation_tokens_total` | Cumulative generated token count. Core tokenomics input. |
| `request_finish_total` | Counts completed requests. Useful for throughput. |
| `request_success_total` | Counts successful requests. Useful for availability and success rate. |
| `request_failure_total` | Counts failed requests. Useful for error-rate and retry analysis. |
| `http.server.active_requests` | Shows active HTTP requests to the server. Useful for request pressure. |
| `e2e_request_latency_seconds` | End-to-end inference latency. Primary model-serving latency metric. |
| `time_to_first_token_seconds` | Measures first-token responsiveness. Important for user-perceived latency. |
| `time_per_output_token_seconds` | Measures generation speed. Useful for model throughput and user experience. |
| `request_prompt_tokens` | Per-request prompt token distribution. Useful for expensive prompt analysis. |
| `request_generation_tokens` | Per-request generated token distribution. Useful for expensive completion analysis. |
| `gpu_cache_usage_perc` | Shows model-server GPU cache pressure. Useful for NIM/vLLM-style serving behavior. |
| `gpu_total_energy_consumption_joules` | Supports energy/cost-efficiency discussion where available. |

### Runtime/process metrics from the workshop allowlist

| Metric group | Why collect it |
|---|---|
| `go_*` | Runtime metrics for Go-based exporters or model-serving components. Keep for dashboard compatibility. |
| `python_*` | Runtime metrics for Python components. Keep for dashboard compatibility where relevant. |
| `process_*` | Process CPU, memory, file descriptor, and uptime signals. Useful for service health. |
| `promhttp_metric_handler_*` | Prometheus scrape endpoint health. Useful for scrape troubleshooting. |
| `system.cpu.time` | Standard host/system metric included by the workshop allowlist. |

## Metrics We Are Not Collecting In The First Build

We are not collecting Cisco UCS, Cisco Nexus, Redfish, Pure Storage, NetApp Trident, Milvus, or Weaviate metrics in the first build.

Reason:

- the user decision is to park synthetic Cisco UCS/Nexus work
- the workshop should first prove GPU, NIM, app instrumentation, tokenomics, and chargeback
- adding storage/network simulation increases build scope and dashboard ambiguity

Parked items:

- Cisco UCS/Intersight metrics
- Cisco Nexus metrics
- Redfish hardware metrics
- Pure/Portworx metrics
- NetApp Trident metrics
- Milvus/Weaviate metrics

If time permits, revisit these as optional enrichment after the core lab works.

## Fallback Reduced Allowlist

Use this only if the full workshop-compatible allowlist creates too much ingest or collector pressure.

### Keep

```text
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
DCGM_FI_DEV_FB_FREE
DCGM_FI_DEV_GPU_TEMP
DCGM_FI_DEV_POWER_USAGE
DCGM_FI_PROF_GR_ENGINE_ACTIVE
DCGM_FI_PROF_PIPE_TENSOR_ACTIVE
num_requests_running
num_requests_waiting
prompt_tokens_total
generation_tokens_total
request_success_total
request_failure_total
e2e_request_latency_seconds
time_to_first_token_seconds
time_per_output_token_seconds
request_prompt_tokens
request_generation_tokens
http.server.active_requests
```

### Why These Survive The Cut

- GPU utilization and memory show saturation.
- GPU temperature and power show hardware health and efficiency.
- tensor/engine activity shows AI acceleration behavior.
- running and waiting requests show serving pressure.
- token counters support tokenomics and chargeback.
- latency histograms support performance analysis.
- success/failure counters support reliability analysis.

### What We Drop In The Fallback

- Go/Python runtime internals.
- most process-level metrics.
- detailed PCIe and clock metrics.
- energy metrics if not needed.

Why:

- useful but not essential for the 4-hour learning outcome
- less directly tied to the student exercises
- lower priority than GPU pressure, NIM latency, and tokenomics

## Scrape Interval

Default:

- `60s`

Fallback if ingest pressure is high:

- `120s`

Do not use aggressive intervals like `10s` for 20 student collectors unless the environment has been tested.

## Dashboard Expectation

The workshop-compatible allowlist is the best attempt to light up out-of-the-box NVIDIA and AI infrastructure dashboard panels.

Expected to work:

- GPU utilization
- GPU memory
- GPU temperature and power
- NIM request pressure
- NIM latency
- prompt and generation token charts

May not fully work without more integrations:

- complete Cisco AI POD overview
- UCS hardware tabs
- Nexus network tabs
- Pure/NetApp storage tabs
- vector database tabs

State this clearly in the lab guide.
