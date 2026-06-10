# Datagen Plan

## Current Status

Datagen is no longer the primary lab workload.

The current primary workload is the `shopmate-ai` multi-agent retail application described in [`docs/AGENTIC_APP_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/AGENTIC_APP_PLAN.md) and [`PLANNING.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/PLANNING.md).

Use this datagen plan only for optional synthetic Cisco-specific telemetry, such as UCS, Nexus, Redfish, storage, or built-in Cisco AI POD dashboard compatibility work. Do not start here when implementing the main lab.

## Purpose

This document defines the optional role of the synthetic data generator for `CLUS-LTROBS-2001`.

The lab will not have access to a real Cisco AI POD. If Cisco-specific hardware, network, or storage dashboard compatibility is required, the project can include a datagen utility that simulates telemetry from a realistic AI/ML environment and feeds Splunk Observability with plausible infrastructure and workload signals.

## Primary Objective

Create a datagen, if needed, that emits correlated telemetry for a simulated Cisco AI Pods-style environment so lab attendees can:

- view realistic charts and dashboards
- learn key monitoring concepts
- practice troubleshooting workflows
- understand how application, GPU, platform, and infrastructure signals relate to each other

## Design Principle

The datagen should simulate the telemetry contract, not the physical hardware.

It does not need to reproduce a real Cisco AI POD deployment in full detail. It must instead provide enough realistic and internally consistent telemetry to drive the lab story and populate the target Splunk experiences as closely as possible.

## Feasibility Summary

Based on the referenced Splunk documentation and workshop material, a datagen approach is feasible for optional Cisco-specific telemetry.

High-confidence areas:

- synthetic GPU metrics
- synthetic storage metrics
- synthetic application and token metrics
- synthetic latency, queue depth, and throughput patterns

Medium-confidence areas:

- exact parity for all Cisco UCS dashboard views
- exact parity for all Cisco Nexus dashboard views

The project can target strong compatibility with Splunk's Cisco AI POD dashboards, but full parity should be treated as a validation exercise rather than an initial assumption.

## Recommended Simulated Workload

If datagen is implemented, use a `multi-tenant LLM inference environment` as the primary simulation model.

Recommended logical services:

- `customer-support-assistant`
- `document-summarizer`
- `code-assistant`
- optional background service: `nightly-embedding-batch`

This model gives the datagen enough richness to simulate:

- request traffic
- token generation
- queue depth
- latency
- GPU pressure
- storage pressure
- network behavior
- tenant contention

This is the preferred workload model for the project because it supports both infrastructure monitoring and application-level observability concepts in a realistic way.

## Telemetry Domains

The datagen should produce signals in these domains:

### Application and model-serving telemetry

- requests per second
- concurrent requests
- queued requests
- prompt tokens
- generation tokens
- token throughput
- time to first token
- end-to-end latency
- error rate
- model load or cold-start effects

### GPU telemetry

- GPU utilization
- GPU memory used
- temperature
- power draw
- throttling indicators

### Host and platform telemetry

- CPU utilization
- memory utilization
- pod restarts
- node saturation
- namespace or workload identity

### Network telemetry

- throughput
- errors
- drops
- burst conditions

### Storage telemetry

- IOPS
- bandwidth
- latency
- queue pressure

## Correlation Requirement

The datagen must not emit random, unrelated numbers.

It should implement causal behavior such as:

- higher request traffic causes queue depth to rise
- queue depth drives higher latency
- higher latency coincides with higher GPU utilization or contention
- infrastructure symptoms appear in the same time window as application degradation

This correlation is critical for teaching observability and troubleshooting.

## Suggested Scenarios

The datagen should support healthy baseline traffic plus scenario injections.

Minimum scenarios:

1. Normal operations
2. Traffic surge causing latency increase
3. Optional app-level agent loop causing token burn
4. Noisy-neighbor tenant causing GPU imbalance
5. Storage slowdown affecting workload responsiveness
6. Pod restart or service instability causing errors

The primary implementation of the agent-loop exercise belongs in `shopmate-ai`. Datagen should only simulate this scenario if the app is unavailable or if instructors need canned telemetry for dry runs.

## Dashboard Strategy

The datagen should be designed to light up built-in and lab-created dashboards as closely as possible.

Priority order:

1. metrics required for lab-created dashboard walkthroughs
2. metrics that support Splunk Cisco AI POD built-in dashboard experiences
3. optional metrics for AI Agent Monitoring extensions

Do not block the project on perfect built-in dashboard parity. Deliver a coherent and useful lab first, then iterate based on validation findings.

## AI Agent Monitoring Boundary

Infrastructure-style telemetry is not sufficient on its own for Splunk AI Agent Monitoring experiences.

If the project later includes AI Agent Monitoring, it should add:

- traces from an instrumented AI application
- metrics compatible with the Agents page
- any required histograms or metadata expected by that experience

Treat AI Agent Monitoring as separate from this optional datagen. The main app should provide agent traces and tokenomics telemetry; this datagen should not be required for those app-level experiences.

## Target Outcome

The synthetic environment should be strong enough to:

- make dashboards feel alive and believable
- support instructor-led troubleshooting exercises
- reinforce how signals across layers connect

## Validation Requirement

The project should assume iterative validation against a real Splunk Observability environment. If exact chart behavior depends on undocumented field or metadata expectations, record those findings in build notes and adapt the datagen accordingly.
