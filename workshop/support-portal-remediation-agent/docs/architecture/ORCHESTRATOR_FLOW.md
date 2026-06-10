# Orchestrator Flow

## Purpose

The remediation orchestrator is the governance layer between Splunk investigation and bounded action.

## Flow

1. Cache pressure degrades `AI Claim Status`.
2. Presenter investigates in Splunk using RUM, APM, and host filesystem signals when needed.
3. Operator clicks `Gather MCP Evidence`.
4. Operator console opens the incident through `POST /remediation/demo/incidents`.
5. Orchestrator queries Splunk Observability Cloud MCP for alert, APM, trace, dependency, and metric evidence.
6. Optional operator notes are attached if provided.
7. Orchestrator enriches missing structured fields when Splunk API endpoint templates are also configured.
8. Orchestrator maps the gathered evidence into the final `EvidenceBundle`.
9. Policy engine determines whether remediation is eligible and which policy mode applies.
10. Remediation agent evaluates bounded actions.
11. Operator approves `clean_claims_knowledge_cache`.
12. Action executes and recovery is verified.

The live detector webhook endpoint, `POST /webhooks/splunk/detector`, remains available as an optional automation path. The core lab does not depend on it.

## Why this design

- visible human trust checkpoint
- clear boundary between evidence and action
- deterministic policy outside the model
- bounded toolset for the agent
- validation after execution
