# Galileo Showcase

Use this path when you want to demonstrate agent observability, evidence grounding,
guardrails, human approval, action, and verification in Galileo.

## Generate the session

From the repository root, with the app stack and credentials loaded:

```bash
npm run simulate:galileo
```

You can also use the operator console:

1. Open `http://127.0.0.1:18081`.
2. In **Galileo Agent Monitoring**, select **Run Showcase**.
3. Keep the JSON result open; it includes the Galileo session id and trace names.

## Galileo console path

1. Open Galileo.
2. Select project `ciscolive26`.
3. Select log stream `remediation-agent`.
4. Switch grouping to **Sessions**.
5. Open the newest session named `AI Claim Status incident ...`.

## Presenter walkthrough

Open the traces in this order:

1. `showcase.incident_intake`
   - Establish the affected journey and customer impact.
2. `showcase.retrieve_observability_context`
   - Show retriever output with RUM, APM, infrastructure, and operator-note sources.
3. `showcase.triage_agent`
   - Show the agent separating trusted observability evidence from untrusted notes.
4. `showcase.hypothesis_agent`
   - Compare cache pressure, provider latency, downstream dependency, and restart hypotheses.
5. `showcase.guardrail_pre_action_check`
   - Show the synthetic unsafe restart instruction and fake PII being blocked.
6. `showcase.action_planning_agent`
   - Show the selected bounded action: `clean_claims_knowledge_cache`.
7. `showcase.human_approval`
   - Show human approval captured as a tool span.
8. `showcase.execute_remediation`
   - Show action execution and the nested remediation tool span.
9. `showcase.verify_recovery`
   - Show validation latency and healthy scenario state.
10. `showcase.postmortem_agent`
   - Close with the audit summary and governance highlights.

## Talk track

The point is not that the agent chose a cache cleanup. The point is that the
team can inspect why the agent chose it, which evidence it trusted, which input
it rejected, who approved it, what action ran, and whether recovery was verified.

## Useful variants

```bash
# Generate traces without executing cleanup or validation.
GALILEO_SHOWCASE_EXECUTE_REMEDIATION=false npm run simulate:galileo

# Generate a cleaner path without the unsafe synthetic operator note.
GALILEO_SHOWCASE_UNSAFE_NOTE=false npm run simulate:galileo

# Use a presenter-friendly incident id.
GALILEO_SHOWCASE_INCIDENT_ID=cl26-galileo-demo npm run simulate:galileo
```
