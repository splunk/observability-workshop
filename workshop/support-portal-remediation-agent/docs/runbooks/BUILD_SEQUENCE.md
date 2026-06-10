# Build Sequence

## Current local build order

1. Install workspace dependencies with `npm install`.
2. Create the remediation-agent virtual environment and install it with `pip install --index-url https://pypi.org/simple -e .`.
3. Copy `.env.example` to `.env`.
4. Set a unique `INSTANCE`.
5. Start Docker so the local Splunk Collector can run.
6. Start the collector with `npm run dev:collector`.
7. Start the full stack with `npm run dev:all`.
8. Open the portal and operator console.
9. Trigger `cache-disk-pressure`.
10. Reproduce the incident in the portal.
11. Use the operator console to create the incident, explain evidence, propose action, approve, and validate.

## Verification order

1. Collector accepts host OTLP traffic on `14318`.
2. Portal loads on `18080`.
3. Operator console loads on `18081`.
4. API gateway responds on `18100`.
5. Scenario controller toggles state on `18104`.
6. Splunk receives APM service metrics and host filesystem metrics.
7. MCP evidence intake produces a policy result.
8. Agent evaluation produces `clean_claims_knowledge_cache`.
9. Approval executes and validates.
10. Terraform validates with `terraform -chdir=infra/terraform validate`.

## Remaining integration work

1. Validate SignalFlow queries against the target Splunk tenant.
2. Apply dashboards and detectors against live default signals.
3. Rehearse the shared-account `INSTANCE` filtering path with multiple student values.
