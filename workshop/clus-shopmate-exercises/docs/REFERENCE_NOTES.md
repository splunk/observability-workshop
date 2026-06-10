# Reference Notes

This file captures the main external references and research conclusions used to shape this project.

## Core Sources

- Splunk Cisco AI POD setup overview:
  [Set up data integrations for Cisco AI Pods](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cisco-ai-pods)
- Splunk Cisco AI POD monitoring guide:
  [Monitor the performance of Cisco AI PODs](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/monitor-and-troubleshoot-your-ai-infrastructure/monitor-the-performance-of-cisco-ai-pods)
- Splunk AI Agent Monitoring setup:
  [Set up AI Agent Monitoring](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring)
- Splunk AI Agent Monitoring zero-code instrumentation:
  [Zero-code instrumentation](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation)
- Splunk AI Agent Monitoring zero-code instrumentation:
  [Zero-code instrumentation](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation)
- Splunk AI Agent Monitoring evaluations:
  [Instrumentation-side evaluations](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/instrumentation-side-evaluations)
- Splunk AI Agent Monitoring Python agent configuration:
  [Configure the Python agent for AI applications 0.1.14 and higher](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/configure-ai-agent-monitoring/configure-the-python-agent-for-ai-applications-0.1.14-and-higher)
- Splunk Ninja Workshop #14 – Cisco AI Pods (no hardware required):
  [Monitoring Cisco AI Pods with Splunk Observability Cloud](https://splunk.github.io/observability-workshop/en/ninja-workshops/14-cisco-ai-pods/)
- Splunk OTel Collector example config (definitive metric allowlist):
  [otel-collector/values.yaml](https://raw.githubusercontent.com/signalfx/splunk-opentelemetry-examples/main/collector/cisco-ai-ready-pods/otel-collector/values.yaml)
- Splunk OTel Collector base config:
  [base-otel-collector-config/values.yaml](https://raw.githubusercontent.com/signalfx/splunk-opentelemetry-examples/main/collector/cisco-ai-ready-pods/base-otel-collector-config/values.yaml)
- Intersight OTel config:
  [intersight/values.yaml](https://raw.githubusercontent.com/signalfx/splunk-opentelemetry-examples/main/collector/cisco-ai-ready-pods/intersight/values.yaml)
- Cisco AI POD repository:
  [Cisco-AI-POD GitHub repository](https://github.com/ucs-compute-solutions/Cisco-AI-POD)
- Cisco AI PODs data sheet:
  [Cisco AI PODs: Pre-validated, Flexible and Modular Infrastructure for Cisco Secure AI Factory Data Sheet](https://www.cisco.com/c/en/us/products/collateral/servers-unified-computing/ucs-x-series-modular-system/ai-pods-ds.html)
- Cisco AI POD training and fine-tuning design guide:
  [Cisco AI POD for Enterprise Training and Fine-Tuning Design Guide](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/cisco_ai_pod_for_training_design.html)
- Cisco AI Defense reference architecture:
  [AI Defense on Cisco AI PODs Reference Architecture](https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/AI_defense_on_Cisco_AI_PODs_reference_architecture.html)
- MkDocs student-facing AI POD hardware appendix and visuals:
  [`workshop/appendix-ai-pod-hardware.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/workshop/appendix-ai-pod-hardware.md)

---

## Built-in Dashboard

There is exactly **one** named built-in dashboard for Cisco AI Pods in Splunk Observability Cloud:

- **Name:** `AI Pod overview`
- **How to find:** Dashboards menu → search "Cisco AI PODs" → select "AI Pod overview"
- The dashboard has multiple tabs. Not all tabs apply to every environment. Users can clone the dashboard and remove inapplicable tabs.
- Linked navigators also provide views for Intersight (UCS hardware) and Nexus (network switch) telemetry.
- The dashboard is **read-only and auto-created** when the integration is deployed.

---

## Supported Components and Data Integrations

The Cisco AI Pods monitoring integration collects telemetry from these components:

| Component | Method | Port / Path |
|---|---|---|
| Cisco UCS servers | Cisco Intersight API via `intersight-otel` tool | OTLP → collector port 4317 |
| Cisco Nexus switches | Cisco OS receiver (SSH) or legacy `cisco_exporter` | SSH / port 9362 |
| NVIDIA GPUs | NVIDIA DCGM Exporter (Prometheus) | 9400 |
| NVIDIA NIM (LLM/embedding) | NIM Prometheus endpoint | 8000 `/v1/metrics` |
| vLLM inference server | vLLM Prometheus endpoint | 8000 `/metrics` |
| NetApp Trident (storage) | Prometheus | 8001 `/metrics` |
| Pure Storage via Portworx | Prometheus | 17001, 17018 |
| Milvus vector database | Prometheus | 9091 |
| Redfish (hardware health) | Prometheus | 9210 `/health`, `/performance` |
| LiteLLM AI Gateway | OTLP (built-in) | — |

Current implementation target: **AWS EKS**. Treat other Kubernetes distributions as external reference material only, not as deployment targets for this lab.

The Helm chart name is `splunk-otel-collector-chart/splunk-otel-collector`. The Helm release is named `ucs-otel-collector`.

Intersight runs as a **separate Kubernetes deployment** using `ghcr.io/cgascoig/intersight-otel:v0.1.2`. It sends OTLP to the OTel Collector agent on port 4317. It is not an OTel receiver inside the collector.

---

## Exact Metric Names (from `filter/metrics_to_be_included` allowlist)

These are the metrics used by built-in charts and detectors. The allowlist is the authoritative source for what the datagen must emit to populate built-in Splunk experiences.

### Cisco Nexus — legacy `cisco_exporter` (Prometheus, port 9362)

```
cisco_collector_duration_seconds
cisco_interface_receive_broadcast
cisco_interface_receive_bytes
cisco_interface_receive_drops
cisco_interface_receive_errors
cisco_interface_receive_multicast
cisco_interface_transmit_bytes
cisco_interface_transmit_drops
cisco_interface_transmit_errors
cisco_interface_up
cisco_up
```

### Cisco Nexus — Cisco OS receiver (SSH-based, newer approach)

```
cisco.device.up
cisco.collector.duration.seconds
system.cpu.utilization
system.memory.utilization
system.network.io
system.network.errors
system.network.packet.dropped
system.network.packet.count
system.network.interface.status
```

### NVIDIA DCGM (GPU metrics, Prometheus port 9400)

```
DCGM_FI_DEV_FB_FREE
DCGM_FI_DEV_FB_USED
DCGM_FI_DEV_GPU_TEMP
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_MEM_CLOCK
DCGM_FI_DEV_MEM_COPY_UTIL
DCGM_FI_DEV_MEMORY_TEMP
DCGM_FI_DEV_POWER_USAGE
DCGM_FI_DEV_SM_CLOCK
DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION
DCGM_FI_PROF_DRAM_ACTIVE
DCGM_FI_PROF_GR_ENGINE_ACTIVE
DCGM_FI_PROF_PCIE_RX_BYTES
DCGM_FI_PROF_PCIE_TX_BYTES
DCGM_FI_PROF_PIPE_TENSOR_ACTIVE
gpu_cache_usage_perc
gpu_total_energy_consumption_joules
```

### NVIDIA NIM (LLM inference, port 8000 `/v1/metrics`)

```
num_request_max
num_requests_running
num_requests_waiting
prompt_tokens_total
generation_tokens_total
request_failure_total
request_finish_total
request_success_total
e2e_request_latency_seconds
time_to_first_token_seconds
time_per_output_token_seconds
request_prompt_tokens
request_generation_tokens
http.server.active_requests
```

### vLLM inference server (port 8000 `/metrics`)

Note: vLLM metrics use the `vllm:` prefix namespace.

```
vllm:num_requests_running
vllm:e2e_request_latency_seconds
vllm:time_to_first_token_seconds
vllm:time_per_output_token_seconds
vllm:request_failure_total
vllm:request_success_total
vllm:num_requests_waiting
vllm:prompt_tokens_total
vllm:generation_tokens_total
vllm:gpu_cache_usage_perc
vllm:request_finish_total
```

NIM and vLLM metrics overlap significantly. NIM uses unprefixed names; vLLM uses the `vllm:` prefix. Both sets are in the allowlist because the integration supports both inference backends.

### Cisco UCS via Intersight (custom OTel metrics)

```
intersight.advisories.nonsecurity.affected_objects
intersight.advisories.security.affected_objects
intersight.advisories.security.count
intersight.alarms.count                          # dimensions: severity=critical|warning
intersight.ucs.fan.speed                         # maps to hw.fan.speed
intersight.ucs.host.power                        # maps to hw.host.power
intersight.ucs.host.temperature                  # maps to hw.temperature
intersight.ucs.network.receive.rate              # derived: hw.network.io_receive / duration
intersight.ucs.network.transmit.rate             # derived: hw.network.io_transmit / duration
intersight.ucs.network.utilization.average       # maps to hw.network.bandwidth.utilization_all
intersight.vm_count
```

HyperFlex cluster metrics (from intersight config):

```
intersight.hyperflex.read.iops
intersight.hyperflex.write.iops
intersight.hyperflex.read.throughput
intersight.hyperflex.write.throughput
intersight.hyperflex.read.latency
intersight.hyperflex.write.latency
```

Key OTel attributes on Intersight metrics:
- `intersight.account.name` — POD name
- `intersight.fsotype` — `account`, `ucs_domain`, or `hyperflex_cluster`
- `intersight.host.name`
- `intersight.name`
- `severity` — on alarm count: `critical` or `warning`

### Pure Storage via Portworx (Prometheus ports 17001 and 17018)

```
px_cluster_cpu_percent
px_cluster_disk_total_bytes
px_cluster_disk_utilized_bytes
px_cluster_status_nodes_offline
px_cluster_status_nodes_online
px_volume_read_latency_seconds
px_volume_reads_total
px_volume_readthroughput
px_volume_write_latency_seconds
px_volume_writes_total
px_volume_writethroughput
```

### NetApp Trident (Prometheus port 8001 `/metrics`)

```
trident_backend_count
trident_node_count
trident_operation_duration_milliseconds_count
trident_operation_duration_milliseconds_quantile
trident_operation_duration_milliseconds_sum
trident_storageclass_count
trident_volume_allocated_bytes
trident_volume_count
trident_volume_total_bytes
```

### Milvus vector database (Prometheus port 9091)

```
milvus_proxy_cache_hit_count
milvus_proxy_req_count
milvus_proxy_req_in_queue_latency
milvus_querycoord_collection_num
milvus_rootcoord_ddl_req_count
milvus_rootcoord_ddl_req_latency_in_queue
milvus_rootcoord_dml_channel_num
milvus_rootcoord_id_alloc_count
```

### Redfish (hardware health, Prometheus port 9210)

```
redfish_performance_scrape_duration_seconds
redfish_thermal_fans_lower_threshold_critical
redfish_thermal_fans_upper_threshold_critical
redfish_thermal_temperatures_reading_celsius
```

### Kubernetes / Host (standard OTel)

```
system.cpu.time
```

---

## OTel Collector Pipeline Architecture

Key pipelines defined in the Helm values:

| Pipeline | Receivers | Purpose |
|---|---|---|
| `metrics/cisco-ai-pods` | `receiver_creator/cisco-ai-pods` | DCGM, NIM, storage, Redfish scrapers |
| `metrics/nvidia-metrics` | `receiver_creator/nvidia` | NVIDIA, vLLM, Milvus, Portworx, Trident, Redfish, legacy Nexus |
| `metrics/cisco-os-metrics` | `ciscoos/switch01`, `ciscoos/switch02` | Cisco OS receiver for Nexus (clusterReceiver) |
| `traces` | OTLP | Application traces |

All metrics pipelines export to the `signalfx` exporter with `send_otlp_histograms: true`.

The `filter/metrics_to_be_included` processor allowlists exactly the metrics used by built-in dashboards — anything not in the list is dropped before export.

Pod autodiscovery uses `receiver_creator` with `k8s_observer`.

---

## Feasibility Conclusion

It is feasible to create a datagen that simulates a Cisco AI Pods-style environment for lab purposes.

**Strongly feasible (high confidence):**
- Emit GPU metrics using exact DCGM metric names and dimensions — dashboards will populate
- Emit NIM or vLLM inference metrics using exact metric names — LLM inference dashboards will populate
- Emit storage metrics (Portworx `px_*` or Trident `trident_*`) — storage dashboards will populate
- Create realistic troubleshooting scenarios with correlated telemetry
- Populate lab-built dashboards and the majority of built-in experiences

**Medium confidence (needs validation):**
- Full parity with Cisco Nexus network tabs (two incompatible metric naming schemes exist: underscore vs. dot)
- Intersight/UCS hardware views (require the `intersight.fsotype` dimension and derived metrics)
- Exact chart queries inside the "AI Pod overview" dashboard tabs (queries not published in docs)

**Feasible via simulation (no real hardware required):**
- Redfish metrics — use the **DMTF Redfish Mockup Server** as a fake BMC (see below)
- Intersight metrics — emit the 12 `intersight.*` metrics directly via OTLP from the datagen, bypassing `intersight-otel` entirely

---

## Monitoring Scope Distinction

This project should keep two Splunk concepts separate:

- `AI Infrastructure Monitoring` — main target for this lab
- `AI Agent Monitoring` and application observability — supported through the ShopMate Sports app when it runs with Splunk zero-code OpenAI/OpenAI Agents instrumentation

AI Agent Monitoring requires application traces and metric types expected by Splunk's AI monitoring experiences. Infrastructure-only telemetry is not sufficient. The custom lab app should emit explicit agent spans, LLM spans, token attributes, cost estimates, and chargeback metadata.

---

## Practical Lab Implication

The lab should claim that it uses a Cisco AI POD-inspired environment and aims to teach the same operational monitoring concepts. It should not claim that attendees are operating a physical Cisco AI POD unless the environment changes.

If optional datagen work is implemented, it must emit metrics using the **exact names and dimensions** from the allowlist above in order for built-in Splunk dashboards to populate correctly. Generic or renamed metrics will not match built-in chart queries.

---

## Simulating Redfish (No Hardware Required)

**Tool:** [DMTF Redfish Mockup Server](https://github.com/DMTF/Redfish-Mockup-Server) — official DMTF project, Docker image `dmtf/redfish-mockup-server:latest`.

**How it works:** Serves a complete, standards-compliant Redfish BMC API from static JSON files. Ships with a built-in mockup (`public-rackmount1`) that includes temperature sensors, fan data, power readings, and threshold values — everything the Redfish Prometheus exporter needs.

**What the mockup includes:**
- Temperature sensors: `CPU1Temp` (37°C), `AmbientTemp` (22.5°C), `ExhaustTemp`, `IntakeTemp`, `DIMM1-3Temp`
- Fan sensors: `FanBay1`, `FanBay2`, `CPUFan1`, `CPUFan2`
- Thermal thresholds: `UpperCaution` 42°C, `UpperCritical` 45°C, `UpperFatal` 50°C
- Power: `PowerConsumedWatts: 344`, PSU health states

**Integration:**
```bash
docker run --rm -p 8000:8000 dmtf/redfish-mockup-server:latest
```
Point the Redfish Prometheus exporter at `http://mock-bmc:8000` as the `target`. The four Splunk metrics (`redfish_thermal_temperatures_reading_celsius`, `redfish_thermal_fans_*_threshold_critical`, `redfish_performance_scrape_duration_seconds`) will populate from the mockup data.

**Limitation:** Values are static (same reading on every scrape). For a lab this is acceptable. For scenario injection (e.g., thermal alert), mount a custom mockup directory and replace the JSON files at scenario trigger time.

**For a more dynamic option:** [DMTF Redfish Interface Emulator](https://github.com/DMTF/Redfish-Interface-Emulator) supports PATCH/POST, allowing values to be updated at runtime. Heavier to configure but enables stateful scenario changes.

---

## Simulating Intersight (No Hardware Required)

Two viable approaches, ordered by implementation effort:

### Option A: Emit Intersight metrics directly from the datagen (recommended)

Skip `intersight-otel` entirely. The datagen emits the 12 `intersight.*` metrics as OTLP gauges with the correct OTel resource attributes. No Intersight API, no auth, no stub server.

Required OTel resource attributes to match what Splunk expects:
- `intersight.account.name` — your POD/account name
- `intersight.fsotype` — one of: `account`, `ucs_domain`, `hyperflex_cluster`
- `intersight.host.name`
- `intersight.name`
- `severity` — on `intersight.alarms.count`: `critical` or `warning`

This is the simplest path and gives full control over scenario values (e.g., spike alarm count for an incident scenario).

### Option B: Custom stub server + `intersight-otel` redirect (architectural fidelity)

If the lab needs to demonstrate the actual `intersight-otel` binary running:

1. Build a small HTTPS stub server (Flask/FastAPI) that returns hardcoded Intersight-shaped JSON for the ~8 API paths the tool queries:
   - `GET /api/v1/virtualization/VirtualMachines` (count endpoint)
   - `GET /api/v1/cond/Alarms` (count by severity)
   - `GET /api/v1/advisor/LicenseAdvisories` (advisory counts)
   - Druid `GroupBys` endpoint for time-series UCS hardware metrics
2. Configure `intersight-otel` with:
   ```toml
   intersight_host = "your-stub:443"
   intersight_accept_invalid_certs = true
   ```
   (The stub can ignore the `Authorization` HTTP signature header.)

**Effort:** ~1–2 days to build the stub server. Produces the same OTLP metrics as a real Intersight account.

---

## Recommended Project Posture

- First build the `shopmate-ai` app, NIM path, GPU telemetry, OpenTelemetry traces, tokenomics metrics, and chargeback workflow.
- Validate app traces and zero-code GenAI metrics against a real Splunk Observability tenant before the lab.
- Add optional datagen only after the core app, GPU, NIM, and tokenomics workflow works end to end.
- If datagen is added, emit exact metric names from the allowlist above.
- If Redfish simulation is needed, use `dmtf/redfish-mockup-server`.
- If Intersight simulation is needed, emit direct OTLP `intersight.*` metrics first.
- Record any dashboard parity mismatches in build notes.
