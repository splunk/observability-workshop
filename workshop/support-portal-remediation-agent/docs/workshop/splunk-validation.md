# Splunk Validation

Use this page after the stack is running and before a live workshop rehearsal. The goal is to prove that Splunk Observability Cloud shows the same story the operator console uses for remediation.

## Preconditions

Set these values in `.env` before starting the stack:

```dotenv
INSTANCE=student-001
DEPLOYMENT_ENVIRONMENT=demo
SPLUNK_REALM=us1
SPLUNK_ACCESS_TOKEN=...
VITE_SPLUNK_RUM_TOKEN=...
GALILEO_API_KEY_FILE=/path/to/galileo_api_key
```

Use a unique `INSTANCE` per student. In Splunk, filter by:

- `service.instance.id=<INSTANCE>`
- `deployment.environment=demo`
- `lab.name=ciscolive26`
- `lab.student.id=<INSTANCE>`

The frontend RUM application name is `ibobs-claims-portal`.

## 1. Confirm local services

Check the local endpoints that have health or deterministic state routes:

```bash
curl -s http://127.0.0.1:18100/api/health
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18110/remediation/health
curl -s http://127.0.0.1:18800/agent/health
```

Open:

- claims portal: `http://127.0.0.1:18080`
- operator console: `http://127.0.0.1:18081`
- workshop docs: `http://127.0.0.1:18082`

## 2. Generate a healthy baseline

Run balanced backend traffic long enough for APM service metrics:

```bash
SIMULATOR_SCENARIO=healthy SIMULATOR_DURATION_SECONDS=300 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

Generate browser traffic when RUM is configured:

```bash
RUM_SIMULATOR_USERS=3 RUM_SIMULATOR_ROUNDS=4 RUM_SIMULATOR_BROWSERS=chromium npm run simulate:rum
```

In Splunk APM, confirm these services appear:

- `claims-portal-api`
- `claims-assistant`
- `claims-knowledge`
- `claims-policy-service`
- `scenario-controller`
- `remediation-orchestrator`
- `remediation-agent`

In Digital Experience, confirm RUM activity for `ibobs-claims-portal`.

## 3. Verify baseline Splunk signals

In APM, verify the three business transactions are visible through spans and service activity:

| Journey | API route | Attribute |
| --- | --- | --- |
| AI Claim Status | `/api/support/respond` | `app.business_transaction=claim_status_response` |
| Policy Coverage Lookup | `/api/cases/:caseId` | `app.business_transaction=policy_coverage_lookup` |
| Claims FAQ Search | `/api/articles/search` | `app.business_transaction=claims_faq_search` |

In Metric Finder or dashboards, check:

- `service.request.duration.ns` for `claims-knowledge`
- `service.request` for request volume
- `system.filesystem.utilization` for `/var/cache/claims-knowledge`
- `system.filesystem.usage` for `/var/cache/claims-knowledge`

Expected baseline:

- all three journeys return successful responses
- `claims-knowledge` latency is normal
- cache filesystem utilization is below the detector threshold
- RUM page and network activity exist for the portal if `VITE_SPLUNK_RUM_TOKEN` is set

## 4. Trigger the cache-pressure incident

Use the operator console or portal `Trigger Cache Pressure` button, or run:

```bash
curl -X POST http://127.0.0.1:18104/scenario/activate/cache-disk-pressure
```

Drive degraded claim-status traffic:

```bash
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=300 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=claim-heavy npm run simulate:traffic
```

Keep comparison traffic visible:

```bash
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=180 SIMULATOR_INTERVAL_MS=1000 SIMULATOR_MIX=balanced npm run simulate:traffic
```

## 5. Validate the incident in Splunk

In Splunk, prove the incident with these checks:

| Area | What to open | Expected evidence |
| --- | --- | --- |
| Digital Experience | `ibobs-claims-portal` pages and network requests | `/api/support/respond` is slower or shows degraded user activity |
| APM | `claims-knowledge` service | `service.request.duration.ns` increases for the claim status path |
| APM traces | a slow AI Claim Status trace | waterfall includes `claims-portal-api`, `claims-assistant`, and `claims-knowledge` |
| Infrastructure | host or container metrics filtered by `service.instance.id` | `system.filesystem.utilization` rises for `/var/cache/claims-knowledge` |
| Business comparison | Policy Coverage and FAQ paths | comparison journeys remain healthier than AI Claim Status |

Do not use logs as the required proof path. Logs are optional supporting context only.

## 6. Validate Splunk MCP evidence intake

Open the operator console:

1. Leave optional operator notes blank.
2. Click `Gather MCP Evidence`.
3. Click `Explain`.
4. Click `Propose`.

Expected evidence package:

- source is `splunk_mcp`
- suspect service is `claims-knowledge`
- affected transaction is `claim_status_response`
- customer impact shows the RUM/network endpoint `POST /api/support/respond` as slow
- backend impact shows `claims-knowledge` p95 latency above threshold and no apparent APM error spike
- infrastructure impact shows cache filesystem utilization for `/var/cache/claims-knowledge` above threshold
- impact chain connects `POST /api/support/respond` to `claims-portal-api`, `claims-assistant`, `claims-knowledge`, and cache filesystem pressure
- confidence is `high` when both latency and cache pressure are confirmed
- proposed action is `clean_claims_knowledge_cache`
- policy mode is `approval_required`

If MCP cannot reach Splunk, the policy should fall back to lower confidence or recommendation-only handling until signals are verified.

## 7. Validate remediation spans

Approve the proposed action from the operator console.

In Splunk APM, open `remediation-orchestrator` and `remediation-agent` traces. Confirm these spans or route-level operations appear:

- `remediation.agent_evaluate`
- `remediation.execute_action`
- `remediation.verify_action`
- `remediation.evaluate`
- `remediation.execute_action`
- `remediation.verify_recovery`

Expected attributes:

- `action.type=clean_claims_knowledge_cache`
- `action.target=claims-knowledge-cache`
- `app.business_transaction=remediation_decision`
- `agent.monitoring.provider=galileo` when Galileo is enabled

## 8. Validate Galileo monitoring

Check agent monitoring status:

```bash
curl -s http://127.0.0.1:18110/remediation/agent-monitoring
```

Run the Galileo showcase:

```bash
npm run simulate:galileo
```

In Galileo, open project `ciscolive26` and log stream `remediation-agent`.

Expected traces:

- `showcase.incident_intake`
- `showcase.retrieve_observability_context`
- `showcase.triage_agent`
- `showcase.hypothesis_agent`
- `showcase.guardrail_pre_action_check`
- `showcase.action_planning_agent`
- `showcase.human_approval`
- `showcase.execute_remediation`
- `showcase.verify_recovery`
- `showcase.postmortem_agent`

Open `showcase.guardrail_pre_action_check` and verify the unsafe restart instruction is blocked before the bounded cache cleanup is planned.

## 9. Validate recovery

After approval, run:

```bash
curl -s http://127.0.0.1:18104/scenario/state
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=180 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

Expected recovery:

- scenario state is `healthy`
- operator console validation status is `validated`
- AI Claim Status latency improves
- `system.filesystem.utilization` for `/var/cache/claims-knowledge` drops or stops rising
- comparison journeys remain healthy

## Splunk search checklist

Use these filters and names during rehearsal:

| Check | Filter or value |
| --- | --- |
| Student isolation | `service.instance.id=<INSTANCE>` |
| Environment | `deployment.environment=demo` |
| RUM app | `ibobs-claims-portal` |
| Degraded service | `claims-knowledge` |
| Cache mount | `/var/cache/claims-knowledge` |
| Claim transaction | `app.business_transaction=claim_status_response` |
| Policy transaction | `app.business_transaction=policy_coverage_lookup` |
| FAQ transaction | `app.business_transaction=claims_faq_search` |
| Remediation action | `clean_claims_knowledge_cache` |

## Pass criteria

The Splunk validation passes only when:

- RUM or browser traffic proves portal activity
- APM shows service latency for the degraded claim-status path
- Infrastructure metrics show cache filesystem pressure
- Splunk MCP evidence creates an approval-required action
- the remediation action executes and verifies recovery
- Galileo shows the agent, tool, and guardrail spans for the remediation story
