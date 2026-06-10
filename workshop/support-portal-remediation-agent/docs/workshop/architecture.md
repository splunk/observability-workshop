# Architecture Summary

This page explains the repo in workshop terms instead of implementation-only terms.

## Core design

The system is split into two layers:

1. observability and evidence
2. action and governance

The separation keeps Splunk investigation, policy, model reasoning, approval, and execution easy to explain.

## User-facing layer

### `apps/frontend`

Customer-facing AI claims portal.

It demonstrates:

- AI claim status
- policy coverage lookup
- claims FAQ search

This is where the incident becomes visible first.

### `apps/operator-console`

Presenter-facing operations and approval interface.

It shows:

- incident intake
- Splunk evidence handoff
- policy mode
- proposed action
- approval state
- validation result

## Application services

### `apps/api-gateway`

Primary backend entrypoint for the portal.

### `apps/assistant-service`

Implements the claim status response workflow.

### `apps/case-service`

Implements policy coverage lookup. This remains a healthy comparison journey.

### `apps/knowledge-service`

Implements knowledge search and owns the bounded cache directory used by the incident scenario.

When `cache-disk-pressure` is active, it fills the cache directory and slows the claim status response path.

### `apps/scenario-controller`

Provides deterministic incident trigger and reset behavior.

## Remediation layer

### `apps/remediation-orchestrator`

Governance layer.

Responsibilities:

- receive detector or local demo incident context
- accept investigation summaries
- parse evidence
- enrich missing structured fields
- build the final evidence bundle
- apply deterministic policy
- manage approval and execution flow

### `apps/remediation-agent`

Python remediation agent with a bounded toolset and model-backed action selection.

The primary action is `clean_claims_knowledge_cache`.

## Observability layer

The workshop path is driven by default signals:

- Splunk RUM and browser spans for the portal
- Splunk APM service metrics for latency, count, and errors
- Splunk OTel Collector hostmetrics for filesystem utilization
- Splunk remediation service spans plus Galileo traces for agent and model visibility

The incident does not require custom app metrics or log analysis.

## Infrastructure

### `infra/docker`

Docker Compose development stack. The knowledge service gets a bounded tmpfs cache volume in this path.

### `infra/otel-collector`

Local collector configuration for OTLP, hostmetrics, traces, and infrastructure metrics.

### `infra/splunk`

Spec-driven authoring path for dashboards and detectors.

### `infra/terraform`

Terraform-managed Splunk dashboards, detectors, webhooks, and related objects.

## Architecture story to tell live

1. customer experience degrades
2. Splunk correlates browser, APM, and filesystem evidence
3. the orchestrator turns investigation output into structured evidence
4. deterministic policy decides what is allowed
5. the remediation agent proposes `clean_claims_knowledge_cache`
6. the operator approves
7. the system validates recovery
