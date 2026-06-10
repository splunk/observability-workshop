# Install and Start

This page is the full bring-up runbook.

## Phase 1: install dependencies

### 1. Install Node workspace dependencies

```bash
npm install
```

Expected result:

- workspace dependencies install successfully
- frontend, backend, and TypeScript tooling are available

### 2. Create the remediation agent virtual environment

```bash
python3 -m venv apps/remediation-agent/.venv
apps/remediation-agent/.venv/bin/pip install --index-url https://pypi.org/simple -e apps/remediation-agent
```

Expected result:

- `apps/remediation-agent/.venv` exists
- the Python package installs in editable mode

## Phase 2: start optional telemetry support

### 3. Start Docker

Make sure the Docker daemon is running before you start the collector.

### 4. Start the Splunk OTel Collector

```bash
set -a
source .env
set +a
npm run dev:collector
```

Use this when:

- you want Splunk APM/RUM/host metrics export
- you want to validate the cache-pressure scenario with filesystem metrics

The host OTLP HTTP endpoint is `http://127.0.0.1:14318`.

## Phase 3: start the application stack

### 5. Start all services

```bash
set -a
source .env
set +a
npm run dev:all
```

This starts:

- knowledge service on `18103`
- assistant service on `18101`
- case service on `18102`
- scenario controller on `18104`
- API gateway on `18100`
- remediation orchestrator on `18110`
- remediation agent on `18800`
- claims portal on `18080`
- operator console on `18081`

### 6. Verify key local endpoints

Open these in your browser:

- `http://127.0.0.1:18080`
- `http://127.0.0.1:18081`

Optional API sanity checks:

```bash
curl -i http://127.0.0.1:18100
curl -i http://127.0.0.1:18104/scenario/state
curl -i http://127.0.0.1:18110/remediation/health
curl -i http://127.0.0.1:18800/agent/health
```

## Phase 4: establish a clean baseline

### 7. Exercise the healthy system

Before failure injection:

1. Open the claims portal.
2. Execute `AI Claim Status`.
3. Execute `Policy Coverage Lookup`.
4. Execute `Claims FAQ Search`.

What you want to prove:

- the app works at baseline
- the three journeys are distinct
- the audience can later understand that only one degraded

### 8. Check the operator console

Confirm:

- no stale incident is blocking the flow
- policy and remediation panes load
- scenario controls are visible

## Phase 5: trigger and remediate

### 9. Trigger cache pressure

Click `Trigger Cache Pressure`.

The scenario fills the claims-knowledge cache directory up to `CLAIMS_KNOWLEDGE_CACHE_QUOTA_BYTES`. In Docker Compose, that directory is also a shared bounded tmpfs volume mounted into the collector, so Splunk host filesystem metrics see real pressure without risking the host disk.

### 10. Reproduce the degraded transaction

Run `AI Claim Status` again.

Expected result:

- claim status response latency increases
- `claims-knowledge` APM duration increases
- filesystem utilization rises for the student instance
- the other two transactions remain usable

### 11. Drive remediation

1. move to the operator console
2. leave `Evidence Intake` blank unless using fallback operator notes
3. click `Gather MCP Evidence`
4. click `Explain`
5. click `Propose`
6. approve `clean_claims_knowledge_cache`
7. verify recovery

## Optional traffic simulators

For a manual Splunk investigation, start traffic first and leave the scenario in `current` mode. Then click `Trigger Cache Pressure` yourself from the portal or operator console.

Backend API traffic:

```bash
npm run simulate:traffic
```

Cache-pressure backend traffic:

```bash
SIMULATOR_SCENARIO=cache-disk-pressure SIMULATOR_RESET_AFTER_RUN=true npm run simulate:traffic
```

Browser traffic:

```bash
RUM_SIMULATOR_USERS=5 RUM_SIMULATOR_ROUNDS=10 npm run simulate:rum
```

Presenter-friendly background traffic:

```bash
SIMULATOR_DURATION_SECONDS=3600 SIMULATOR_INTERVAL_MS=750 SIMULATOR_MIX=balanced npm run simulate:traffic
```

```bash
RUM_SIMULATOR_USERS=2 RUM_SIMULATOR_ROUNDS=120 RUM_SIMULATOR_BROWSERS=chromium RUM_SIMULATOR_CONCURRENCY=1 npm run simulate:rum
```

## Stop conditions

Do not move into the live workshop until these are true:

- claims portal works
- operator console works
- baseline journeys run
- cache pressure can be triggered
- `clean_claims_knowledge_cache` can be approved and validated
