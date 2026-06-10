# Datagen Build Guide

## Current Status

This is optional extension guidance.

The main lab workload is now `shopmate-ai`, the instrumented multi-agent retail app defined in [`docs/AGENTIC_APP_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/AGENTIC_APP_PLAN.md). Use this guide only if the project needs synthetic Cisco-specific telemetry for UCS, Nexus, storage, Redfish, or Cisco AI POD dashboard compatibility.

This guide provides step-by-step instructions for designing and implementing the synthetic telemetry generator used by the lab project.

## Goal

Build a utility that simulates a Cisco AI Pods-style AI/ML environment and emits believable telemetry for Splunk Observability.

The utility should be suitable for generating:

- baseline health telemetry
- workload demand patterns
- incident scenarios for troubleshooting exercises

This guide assumes there is no access to a physical Cisco AI POD in the lab environment.

## Build Strategy

Use a layered simulation model.

Instead of generating isolated metrics directly, model a small virtual system with:

- tenants
- services
- workloads
- nodes
- GPUs
- storage
- network paths

Then derive telemetry from the state of that system.

The recommended workload model is a multi-tenant LLM inference platform with three primary services and one optional background batch workload.

## Step 1: Define the simulated environment

Create a topology description for the synthetic environment.

Minimum recommended entities:

- `1` logical cluster
- `3` AI application services
- `3-6` worker nodes
- `4-8` GPUs
- `1-2` storage backends
- `1` ingress or API tier

Suggested service identities:

- `customer-support-assistant`
- `document-summarizer`
- `code-assistant`

Suggested node identities:

- `ai-node-01`
- `ai-node-02`
- `ai-node-03`

Suggested GPU identities:

- `gpu-0`
- `gpu-1`
- `gpu-2`
- `gpu-3`

Output for this step:

- a topology model file or in-code object describing entities and relationships

## Step 2: Define the telemetry schema

List the metrics and metadata the simulator will emit.

At minimum, define:

- metric name
- description
- unit
- metric type: gauge, counter, histogram, summary
- dimensions or resource attributes
- source entity

Suggested metric groups:

- application requests and errors
- token metrics
- latency metrics
- queue metrics
- GPU metrics
- host metrics
- storage metrics
- network metrics

If the project wants to support optional AI Agent Monitoring later, keep room in the schema for traces and histogram-style metrics, but do not make them part of the minimum viable datagen.

Output for this step:

- a schema document or config file mapping each metric to entities and attributes

## Step 3: Define the state model

Implement internal state for each layer.

Examples:

- per-service request rate
- per-service concurrency
- per-node CPU and memory pressure
- per-GPU utilization and memory consumption
- storage latency and queue depth
- network burst level

State should evolve over time in small intervals such as every `5s` or `10s`.

Output for this step:

- state objects and update rules

## Step 4: Define causal rules

Implement rules that connect telemetry domains.

Examples:

- if request rate rises, queue depth increases
- if queue depth increases, latency rises
- if latency rises, time to first token also degrades
- if one service dominates traffic, one node or GPU can become imbalanced
- if storage latency rises, inference or model-loading latency may worsen

This is the most important step for realism.

Output for this step:

- documented equations or logic rules for telemetry generation

## Step 5: Implement scenario injection

Allow the datagen to run in at least two modes:

- steady-state baseline mode
- scenario mode

Scenario mode should support controlled injections such as:

- traffic surge
- app-level agent loop token burn, only as fallback synthetic telemetry
- noisy neighbor
- storage slowdown
- restart storm

Recommended initial scenario list:

- `normal-operations`
- `traffic-surge`
- `agent-loop-token-burn`
- `noisy-neighbor`
- `storage-slowdown`
- `restart-storm`

Each scenario should:

- have a name
- define start and end timing
- affect specific services or nodes
- modify the normal state evolution rules

Output for this step:

- scenario configuration files or code modules

## Step 6: Choose the export method

Select the telemetry output path that best fits the lab environment.

Preferred options:

1. Prometheus exporter endpoints for metric scraping
2. OTLP metric export directly to the Splunk OpenTelemetry Collector

If both are practical, support both.

Prefer OTLP when testing direct compatibility with Splunk ingest paths. Prefer Prometheus exporters when mirroring the behavior of component exporters used in example architectures.

Output for this step:

- exporter interface selection
- configuration documentation

## Step 7: Define resource attributes and dimensions

Attach meaningful attributes so dashboards and filters can segment data.

Examples:

- `service.name`
- `deployment.environment`
- `k8s.cluster.name`
- `k8s.namespace.name`
- `host.name`
- `host.ip`
- `gpu.id`
- `model.name`
- `tenant`
- `storage.backend`
- `ai_pod.name`
- `vendor.integration`

Use consistent naming across all emitted telemetry.

Output for this step:

- a shared attribute dictionary or conventions file

## Step 8: Build a time controller

Implement a scheduler that updates state and emits metrics on a fixed cadence.

Recommended cadence:

- update simulation state every `5s`
- emit gauges every `5s`
- increment counters continuously or on each cycle
- emit latency or token histograms on each request batch

Output for this step:

- simulation loop with configurable interval

## Step 9: Add data profiles

Create multiple traffic profiles so instructors can switch behavior quickly.

Recommended profiles:

- `quiet`
- `normal`
- `peak`
- `incident-demo`

Each profile should modify:

- base request rate
- burstiness
- concurrency
- probability of errors
- GPU utilization envelope

Output for this step:

- profile configuration file or command-line switches

## Step 10: Add instructor controls

Provide simple controls for live lab use.

Recommended controls:

- start and stop the simulator
- select a traffic profile
- trigger a scenario manually
- set a random seed
- choose export target

Prefer command-line flags or a small config file.

Output for this step:

- operator-friendly runtime interface

## Step 11: Validate against Splunk

Verify that telemetry appears as expected in Splunk Observability.

Validation checklist:

1. Confirm metrics are ingested.
2. Confirm resource attributes appear correctly.
3. Confirm dashboards populate with non-empty charts.
4. Confirm scenario injections create visible changes.
5. Confirm multiple services and nodes can be filtered independently.
6. Confirm synthetic data looks plausible over time rather than purely random.
7. Confirm built-in Cisco AI POD experiences populate as expected where supported.

Record any mismatches between expected and observed chart behavior.

Output for this step:

- validation notes
- required schema adjustments

## Step 12: Document the simulator

Create documentation for future contributors and AI agents.

Minimum topics:

- architecture
- runtime prerequisites
- how to start the datagen
- how to switch scenarios
- what metrics it emits
- what each scenario demonstrates

Output for this step:

- datagen README
- metric schema reference
- scenario guide

## Recommended Repo Layout

Suggested structure for future implementation:

```text
datagen/
  README.md
  config/
    topology.yaml
    metrics.yaml
    profiles.yaml
    scenarios.yaml
  src/
    main.(py|ts|go)
    simulator/
    exporters/
    scenarios/
  docs/
    metric-schema.md
    scenario-guide.md
```

## Implementation Priorities

Build in this order:

1. static healthy metrics
2. correlated baseline simulation
3. scenario injection
4. export hardening
5. validation against Splunk dashboards

## Minimum Viable Datagen

The first working version should:

- simulate `3` services
- simulate `3` nodes and `4` GPUs
- emit application, GPU, host, and latency metrics
- support one traffic surge scenario
- export data into Splunk through one supported path

It should also expose enough metadata to segment by service, node, and tenant.

## Known Limits

- Public documentation does not guarantee every chart query used by built-in dashboards.
- Cisco UCS and Cisco Nexus built-in views may require metric names or dimensions that must be discovered through validation.
- AI Agent Monitoring requires application instrumentation beyond infrastructure metrics.

Do not wait for perfect realism before producing a working version.

## Definition of Done

The datagen is useful when:

- the simulator can run unattended for the lab
- data looks coherent over time
- instructors can trigger scenario changes
- attendees can see clear telemetry shifts and discuss root cause
- documentation is sufficient for another contributor or AI agent to extend it
