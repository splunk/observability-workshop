# Test Strategy

This repo needs fast, deterministic tests around decision logic first, then a thin set of integration tests around service contracts.

## Immediate Baseline

- `npm test` runs TypeScript unit tests with `tsx --test`.
- Current coverage target:
  - evidence parsing heuristics
  - remediation policy decisions
  - in-memory incident and webhook receipt storage

These tests are intentionally offline and avoid Splunk, OpenAI, Docker, and Cloudflare dependencies.

## Recommended Test Pyramid

- Unit tests
  - `packages/evidence-parser`: parsing heuristics and fallback behavior
  - `packages/policy-engine`: eligibility and policy mode decisions
  - `packages/shared-types`: state-store behavior
  - `apps/remediation-agent`: fallback action selection, execute/verify flows with mocked HTTP
- Contract tests
  - `apps/api-gateway` to downstream services
  - `apps/remediation-orchestrator` to remediation agent and Splunk enrichment adapter
  - request and response fixtures for detector webhook payload variants
- Browser and workflow tests
  - Playwright happy path for frontend and operator console
  - one degraded-flow scenario covering incident intake, proposal, approval, execution, and verification

## What To Mock

- Mock OpenAI responses in all automated tests.
- Mock Splunk Observability API responses with checked-in fixtures.
- Mock webhook delivery instead of relying on a live Cloudflare tunnel.
- Keep scenario-controller interactions local and deterministic.

## Repo and Infra Changes That Make Testing Easier

- Treat the public webhook endpoint as a stable integration boundary, not a mutable local dev URL.
- Move Splunk object definitions to versioned JSON or Python templates and test those payload builders offline.
- Keep Terraform only for long-lived primitives if you still need it.
- Stop committing generated assets, Terraform state, local logs, and build output.

## Cloudflare URL Recommendation

The current `trycloudflare.com` flow is fragile because the URL rotates and then leaks into `.env`, detector runbook URLs, and Terraform state.

Better options:

- Best dev/prod parity: use a named Cloudflare Tunnel with a fixed hostname.
- Best testability: put a small public webhook ingress in front of the local orchestrator.

Recommended flow:

1. Splunk sends webhooks to a stable public ingress URL.
2. The ingress validates the shared secret and stores the raw payload.
3. In dev, the ingress can forward to a local tunnel when available.
4. In tests, the ingress payloads are replayed from fixtures without any tunnel dependency.

That separates “public endpoint identity” from “where my laptop is today,” which is the main source of friction now.

## Terraform Recommendation

Terraform is acceptable for stable, low-churn infrastructure objects, but it is a poor authoring loop for dashboards and detector tuning.

I would change this to:

- `infra/splunk/specs/*.json` or `*.yaml` as the source of truth for dashboards and detectors
- Python scripts that upsert those specs through the Splunk API
- fixture-based tests that snapshot the generated API payloads

That gives you:

- easier iteration
- smaller diffs
- better local validation
- no local Terraform state churn for dashboard edits
