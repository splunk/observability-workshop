# Splunk API Integration

This document defines the tenant-specific values the remediation orchestrator expects when live Splunk enrichment is enabled.

## Environment variables

- `SPLUNK_ACCESS_TOKEN`
- `SPLUNK_REALM`
- `SPLUNK_API_BASE_URL`
- `SPLUNK_MCP_ENABLED`
- `SPLUNK_MCP_URL`
- `SPLUNK_MCP_AUTH_TOKEN`
- `SPLUNK_MCP_TENANT`
- `SPLUNK_MCP_TIMEOUT_MS`
- `SPLUNK_DETECTOR_ENDPOINT_TEMPLATE`
- `SPLUNK_IMPACT_ENDPOINT_TEMPLATE`
- `SPLUNK_TOPOLOGY_ENDPOINT_TEMPLATE`

## MCP evidence path

The preferred manual lab flow now uses Splunk Observability Cloud MCP to gather evidence directly from Splunk instead of requiring pasted AI Assistant text.

When `SPLUNK_MCP_ENABLED` is not `false` and `SPLUNK_ACCESS_TOKEN` is present, the orchestrator calls the configured MCP endpoint during incident intake. If `SPLUNK_MCP_URL` is blank, the orchestrator defaults to:

```text
https://api.${SPLUNK_REALM}.signalfx.com/v2/mcp
```

The MCP client lists available tools and then calls the supported evidence tools it finds:

- `search_alerts_or_incidents`
- `get_apm_services`
- `get_apm_service_dependencies`
- `get_apm_service_latency`
- `get_apm_service_errors_and_requests`
- `get_apm_exemplar_traces`
- `execute_signalflow_program`

The resulting evidence is mapped into the existing `EvidenceBundle`. Pasted operator notes are optional and only override the generated MCP summary when provided.

`SPLUNK_MCP_AUTH_TOKEN` and `SPLUNK_MCP_TENANT` are optional gateway fields for hosted MCP Gateway deployments. The direct Observability endpoint uses `SPLUNK_ACCESS_TOKEN` and `SPLUNK_REALM`.

The endpoint templates support these placeholders:

- `{detectorId}`
- `{incidentId}`
- `{severity}`

## Expected response shapes

The orchestrator does not require exact Splunk-native payloads. It looks for a small set of fields and falls back to demo defaults when they are absent.

### Detector / Change Context

Accepted fields:

- `recentChange`
- `recent_change`
- `event.recentChange`

### Impact / Digital Experience / APM

Accepted fields:

- `affectedSessions`
- `affected_sessions`
- `rum.affectedSessions`
- `p95LatencyMs`
- `latency.p95`
- `apm.p95LatencyMs`
- `errorRate`
- `error_rate`
- `apm.errorRate`
- `sessionReplayUrl`
- `session_replay_url`

### Topology / Service Context

Accepted fields:

- `affectedServices`
- `services`
- `apm.affectedServices`
- `suspectService`
- `suspect_service`
- `apm.suspectService`
- `affectedTransactions`
- `transactions`

## Current behavior

When API or MCP enrichment succeeds:

- `evidence.sourceNotes.enrichmentApplied` becomes `true`
- `evidence.sourceNotes.apiEnrichmentSources` lists contributing endpoints
- `evidence.sourceNotes.enrichmentWarnings` contains partial failures
- `evidence.sourceNotes.observabilityResources` lists service, dependency, metric, alert, and trace resources gathered from MCP when available
- `evidence.approvalEvidence` lists the metric-backed approval proof: customer endpoint latency, APM service latency, APM error-rate context, cache filesystem utilization, and the impact chain that connects the slow customer request to the bounded cache cleanup action

When enrichment is unavailable:

- the orchestrator still produces a complete evidence bundle
- the evidence is marked as fallback/default data
- warnings remain visible in the operator console

## Signal strategy

The current lab intentionally does not query custom demo metrics from the orchestrator.

Use Splunk UI, detectors, and dashboards for default signals:

- APM service request metrics such as `service.request` and `service.request.duration.ns`
- host filesystem metrics such as `disk.utilization`
- RUM and browser spans for the claims portal
- remediation service spans in Splunk APM, with agent/model visibility in Galileo

The MCP and API integrations remain lightweight enrichment hooks. They enrich context, but policy evaluation and remediation execution still use the bounded `EvidenceBundle` contract.
