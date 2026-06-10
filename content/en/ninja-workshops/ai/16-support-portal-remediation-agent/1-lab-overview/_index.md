---
title: Lab Overview
linkTitle: 1. Lab Overview
weight: 1
archetype: chapter
time: 15 minutes
description: Understand the AI support portal, deterministic incident, service topology, and governed remediation path.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are an **incident commander** responsible for a customer-facing AI support experience. Your job is to connect customer impact to backend evidence, then decide whether a bounded remediation action is safe to approve.
{{% /notice %}}

## Use Case

The lab application is an AI claims support portal. A customer uses it to check claim status, look up policy coverage, or search support articles. During the incident, the cache volume used by the knowledge service fills up. The `AI Claim Status` journey slows down because it depends on that service, while `Policy Coverage Lookup` and `Claims FAQ Search` stay available as comparison journeys.

The goal is not full autonomous remediation. The goal is a governed workflow:

1. Detect customer impact.
2. Validate the affected service path.
3. Prove cache filesystem pressure with standard infrastructure metrics.
4. Build an evidence package.
5. Apply deterministic policy.
6. Require approval for the state-changing action.
7. Validate recovery after execution.

## Local Source Copy

The workshop app is copied into this repository:

```bash
cd workshop/support-portal-remediation-agent
```

Run all app commands from that directory unless a step says otherwise.

## App Components

| Component | Purpose |
| --- | --- |
| `apps/frontend` | Customer-facing AI claims portal. |
| `apps/operator-console` | Presenter and operator console for evidence, policy, approval, and validation. |
| `apps/api-gateway` | Main backend entry point for the portal. |
| `apps/assistant-service` | Claim status workflow. |
| `apps/case-service` | Policy coverage lookup workflow. |
| `apps/knowledge-service` | Knowledge search and bounded cache-pressure source. |
| `apps/scenario-controller` | Deterministic incident trigger and reset service. |
| `apps/remediation-orchestrator` | Evidence intake, enrichment, policy, proposal, approval, and validation coordinator. |
| `apps/remediation-agent` | Python remediation agent with a bounded toolset and model-backed action selection. |

## Observability Signals

The primary story uses default Splunk Observability signals:

- Splunk RUM and browser spans for the portal journey.
- Splunk APM service metrics for latency, count, and errors.
- Splunk OpenTelemetry Collector host metrics for filesystem utilization.
- Remediation orchestrator and remediation agent spans for action auditability.
- Galileo traces for agent, tool, guardrail, approval, and model-call visibility when configured.

{{% notice title="Key Rule" style="info" %}}
Do not make logs or custom demo metrics the required proof path. Use browser experience, APM service health, and host filesystem metrics as the main evidence chain.
{{% /notice %}}

## Remediation Boundary

The bounded action is:

```text
clean_claims_knowledge_cache
```

The action clears the cache-pressure scenario through the scenario controller and then verifies that the `AI Claim Status` path recovered. The operator console should show why the action was proposed, what policy mode applies, who approved it, and whether validation passed.
