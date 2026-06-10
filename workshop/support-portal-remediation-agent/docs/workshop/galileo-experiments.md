# Galileo Experiments

Use this section after the live operator-console flow. The experiment story is:

> The console shows one incident working end to end; Galileo Experiments show whether the app handles Splunk MCP evidence quality and remediation tool failures consistently.

These experiments are deterministic harnesses around app behavior. They use the same domain objects, MCP tool names, policy modes, action names, and verification states as the app. They do not call live Splunk for every row because the goal is repeatable evaluation; use the operator console for the live MCP call.

## What The Dataset Contains

Each dataset row is one realistic app case, not a file in the repo.

The default dataset row has these fields:

- `incident`: human-readable incident description
- `mcp_tools`: expected outcome from Splunk MCP tools used by the app
- `operator_note`: optional presenter note
- `expected`: the expected app behavior

The important MCP tools are the same tools referenced by `apps/remediation-orchestrator/src/splunk-mcp-client.ts`:

- `tools/list`
- `search_alerts_or_incidents`
- `get_apm_service_latency`
- `get_apm_service_errors_and_requests`
- `get_apm_exemplar_traces`
- `execute_signalflow_program` for cache utilization
- `execute_signalflow_program` for AI Claim Status latency

## Run The MCP Experiment

```bash
npm run experiment:galileo
```

or:

```bash
npm run experiment:galileo:mcp
```

This creates a run named like:

```text
cl26-splunk-mcp-handoff-1780000000000
```

Rows:

- `mcp-complete-cache-pressure`: MCP confirms cache pressure and elevated latency.
- `mcp-cache-signalflow-empty`: latency is high but cache SignalFlow does not confirm pressure.
- `mcp-latency-tool-timeout`: cache pressure is confirmed but the latency tool fails.
- `mcp-tools-list-failed`: MCP tools are unavailable.
- `mcp-no-pressure-confirmed`: MCP responds but does not confirm pressure or latency.
- `mcp-exemplar-trace-attached`: MCP confirms the issue and attaches an exemplar trace id.

Metrics:

- `mcp_confidence_match`
- `mcp_policy_match`
- `mcp_proposal_match`
- `mcp_warning_match`
- `overall_mcp_handoff`

## What The Steps Mean

The spans are experiment functions, not separate deployed agents:

- `splunk_mcp.tools_list`: simulates the app discovering MCP tools.
- `splunk_mcp.get_apm_service_latency`: represents the MCP latency tool.
- `splunk_mcp.execute_signalflow_program.cache`: represents the cache utilization SignalFlow query.
- `splunk_mcp.execute_signalflow_program.latency`: represents the latency SignalFlow query.
- `remediation.build_evidence_bundle`: mirrors the orchestrator building the `EvidenceBundle`.
- `remediation.policy_check`: mirrors the policy engine.
- `remediation.agent_evaluate`: mirrors the remediation agent proposal step.

The deployed app services are still the orchestrator, remediation agent, scenario controller, and operator console. The experiment runner uses deterministic functions so every row is repeatable.

## Demo Click Path

1. Open Galileo project `ciscolive26`.
2. Click **Experiments**.
3. Open the newest `cl26-splunk-mcp-handoff...` run.
4. Start on the metrics table.
5. Say: "Each row is a Splunk MCP evidence handoff case."
6. Open `mcp-complete-cache-pressure`.
7. Click the trace.
8. Open `splunk_mcp.execute_signalflow_program.cache`.
9. Show cache utilization above threshold.
10. Open `splunk_mcp.get_apm_service_latency`.
11. Show latency above threshold.
12. Open `remediation.build_evidence_bundle`.
13. Show `confidence_band = high`.
14. Open `remediation.policy_check`.
15. Show `policy_mode = approval_required`.
16. Open `remediation.agent_evaluate`.
17. Show `proposed_action = clean_claims_knowledge_cache`.

Then open `mcp-tools-list-failed`:

1. Open `splunk_mcp.tools_list`.
2. Show the MCP tool failure.
3. Open `remediation.build_evidence_bundle`.
4. Show `confidence_band = low`.
5. Open `remediation.policy_check`.
6. Show `policy_mode = recommend_only`.

Then open `mcp-cache-signalflow-empty`:

1. Open the cache SignalFlow span.
2. Show it did not confirm cache utilization.
3. Open `remediation.build_evidence_bundle`.
4. Show the warning count and `confidence_band = medium`.

## Run The Tool-Flow Experiment

```bash
npm run experiment:galileo:tools
```

This creates a run named like:

```text
cl26-remediation-tool-flow-1780000000000
```

Rows:

- `approval-required-not-clicked`: proposal exists but presenter has not clicked Approve.
- `clean-cache-executes-and-validates`: bounded cache cleanup executes and verification validates recovery.
- `remediation-agent-execute-fails`: execution fails, so verification is skipped.
- `verification-sees-scenario-still-active`: execution returns but scenario controller still reports pressure.
- `recommend-only-blocks-approval`: low-confidence policy blocks approval execution.

Metrics:

- `approval_gate_match`
- `execution_status_match`
- `verification_status_match`
- `incident_status_match`
- `overall_tool_flow`

## Tool-Flow Click Path

1. Open the newest `cl26-remediation-tool-flow...` experiment.
2. Open `clean-cache-executes-and-validates`.
3. Walk `remediation.approval_endpoint` to `remediation.execute_action` to `remediation.verify_action`.
4. Show `validated`.
5. Open `remediation-agent-execute-fails`.
6. Show `execute_action` failed and `verify_action` is skipped.
7. Open `recommend-only-blocks-approval`.
8. Show the approval endpoint blocks execution because policy mode is `recommend_only`.

## Honest Positioning

Say this clearly if asked:

> The live console flow calls Splunk MCP and the remediation services. The experiment uses deterministic rows that mirror the same MCP tool names, EvidenceBundle fields, policy modes, and remediation statuses so we can test edge cases like MCP failure and verification failure on demand.

## Run All App-Aligned Experiments

```bash
npm run experiment:galileo:all
```

Use a stable name for rehearsal:

```bash
npm run experiment:galileo:mcp -- --name cl26-rehearsal-mcp-handoff
```
