---
title: Govern Remediation
linkTitle: 5. Govern Remediation
weight: 5
archetype: chapter
time: 25 minutes
description: Gather evidence in the operator console, evaluate policy, approve the bounded action, and validate recovery.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **service owner** deciding whether a state-changing remediation is allowed. Your job is to keep model reasoning, policy, approval, execution, and validation separate.
{{% /notice %}}

## Gather Evidence

Open the operator console:

```text
http://127.0.0.1:18081
```

Use the primary path:

1. Leave `Evidence Intake` blank.
2. Click `Gather MCP Evidence`.
3. Click `Explain`.
4. Click `Propose`.
5. Review the evidence, policy, proposal, and validation panels.

Expected evidence package:

- Source is Splunk MCP when configured.
- Suspect service is `claims-knowledge`.
- Affected transaction is `claim_status_response`.
- Customer impact points to `/api/support/respond`.
- Backend impact shows elevated `claims-knowledge` latency.
- Infrastructure impact shows cache filesystem utilization above threshold.
- Confidence is high only when latency and cache pressure are both confirmed.
- Proposed action is `clean_claims_knowledge_cache`.
- Policy mode is `approval_required`.

## AI Assistant Fallback

If Splunk MCP is unavailable, use Splunk AI Assistant or manual investigation notes as a fallback. Paste a concise summary into `Evidence Intake`.

Use this prompt:

```text
Investigate the Cisco Live claims portal incident over the last 15 minutes.

Scope the investigation to:
- service.instance.id = $INSTANCE
- deployment.environment = demo
- affected journey or business transaction = AI Claim Status
- likely service = claims-knowledge
- cache mountpoint = /var/cache/claims-knowledge

Use default Splunk Observability signals only: RUM or browser experience, APM service latency/error evidence, and host filesystem metrics. Do not use logs and do not invent custom metrics.

Return a concise incident summary that includes:
- whether AI Claim Status is degraded
- whether Policy Coverage Lookup and Claims FAQ Search remain healthy
- the likely affected service
- the filesystem signal for the cache mount or student instance
- the APM evidence that supports the finding
- confidence level
- one narrow recommended remediation action

End with exactly this remediation recommendation if the evidence supports it:
Recommended action: clean_claims_knowledge_cache.
```

Fallback text for a workshop-day recovery path:

```text
High confidence that claims-knowledge cache filesystem pressure degraded the AI Claim Status transaction.
Host filesystem utilization for the student instance is above threshold, and APM shows elevated claims-knowledge request duration.
Policy Coverage Lookup and Claims FAQ Search remain healthy comparison journeys.
Recommended action: clean_claims_knowledge_cache.
```

## Review Policy

Before approving, answer:

| Question | Expected answer |
| --- | --- |
| What resource changes? | The lab cache-pressure scenario for `claims-knowledge`. |
| What action runs? | `clean_claims_knowledge_cache`. |
| Is the action bounded? | Yes, it targets only the lab cache scenario. |
| Is there a validation plan? | Yes, rerun `AI Claim Status` and check scenario state plus telemetry. |
| Is human approval required? | Yes, for the state-changing remediation path. |

{{% notice title="Governance Rule" style="warning" %}}
The model can recommend a bounded action, but deterministic policy and human approval decide what is allowed to execute.
{{% /notice %}}

## Approve and Execute

Approve the action in the operator console when:

- The evidence supports cache filesystem pressure.
- Policy mode allows approval.
- The proposed action is `clean_claims_knowledge_cache`.
- You can validate recovery after execution.

Expected result:

- The remediation agent executes the cleanup path.
- The scenario controller returns the scenario to healthy.
- The operator console updates the validation state.

## Validate Recovery

Run:

```bash
curl -s http://127.0.0.1:18104/scenario/state
SIMULATOR_SCENARIO=current SIMULATOR_DURATION_SECONDS=180 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

Then validate:

- Scenario state is `healthy`.
- `AI Claim Status` latency improves.
- Operator console validation status is `validated`.
- Filesystem utilization drops or stops rising.
- Comparison journeys remain healthy.

Remediation is complete only when the customer journey and telemetry recover, not when a command returns successfully.
