# Troubleshooting

This page is optimized for workshop-day failures.

## `npm install` fails

Check:

- internet access or package registry access
- Node version compatibility
- whether a previous partial install left a corrupted `node_modules`

Action:

1. re-run `npm install`
2. capture the first real error
3. resolve that root issue before changing application code

## Python agent setup fails

```bash
cd apps/remediation-agent
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install --index-url https://pypi.org/simple -e .
```

Use the delete step only when you intend to recreate the virtual environment.

## Collector will not start

Check:

- Docker daemon is running
- `.env` is loaded
- host port `14318` is free

Action:

```bash
docker info
grep -E '^OTEL_EXPORTER_OTLP_ENDPOINT=' .env
npm run dev:collector
```

Expected local value:

```dotenv
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318
```

## Portal or console does not load

Check:

- `npm run dev:all` is still running
- Vite did not fail due to port conflict
- browser is pointed at the high-port URLs

Action:

```bash
lsof -i :18080 -i :18081
```

## Backend services are inconsistent

Action:

1. reset scenario state
2. refresh both UIs
3. run the three transactions in healthy mode
4. trigger cache pressure again

Useful checks:

```bash
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18103/knowledge/cache/status
```

## The support transaction does not degrade

Check:

- `Trigger Cache Pressure` was clicked
- `AI Claim Status` was rerun after the scenario became active
- `CLAIMS_KNOWLEDGE_CACHE_DIR` points at a writable lab directory

Action:

```bash
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18103/knowledge/cache/status
```

## Telemetry is not visible in Splunk

Check locally first:

1. collector is running
2. app processes started with `.env` loaded
3. fresh traffic was generated after collector startup
4. `INSTANCE` and `OTEL_RESOURCE_ATTRIBUTES` match the student lab

Look for:

- APM services such as `claims-knowledge`, `claims-assistant`, and `remediation-agent`
- host filesystem metric `disk.utilization`
- RUM data for the portal if `VITE_SPLUNK_RUM_TOKEN` is set

If the APM trace waterfall shows `Infrastructure (0)`:

1. generate fresh AI Claim Status traffic
2. wait for the collector log line `Updated dimension` with `claims-knowledge` and `method":"PUT"`
3. open the `claims-knowledge` service view or service map
4. use Infrastructure Monitoring filtered to the student `INSTANCE` and mountpoint `/var/cache/claims-knowledge`

The trace waterfall can outlive Splunk's current service-to-host related-content relation. The collector is configured with a longer `stale_service_timeout` for the workshop, but the reliable presenter path is still APM service view plus Infrastructure Monitoring.

If RUM sessions are missing:

1. confirm `VITE_SPLUNK_RUM_TOKEN` is configured for the portal container
2. restart the portal
3. generate fresh browser traffic after the restart
4. wait a few minutes, then use `Pages` or `Network Requests` first
5. use `Session Search` only if session replay is enabled and new sessions were generated

Useful check:

```bash
docker compose --env-file .env -f infra/docker/docker-compose.yml exec -T frontend env | grep VITE_SPLUNK
```

## Remediation recommendation or execution is missing

Check:

- `Gather MCP Evidence` created an evidence package in the operator console
- the orchestrator built an evidence bundle
- policy mode is visible
- remediation agent is reachable on `18800`

Action:

```bash
curl -s http://127.0.0.1:18800/agent/health
curl -s http://127.0.0.1:18110/remediation/health
```

## Optional webhook delivery does not work

This is not a core lab blocker. The primary workshop path opens a local incident and gathers Splunk evidence through MCP.

If testing webhooks:

1. prove local orchestrator behavior on `127.0.0.1`
2. start the tunnel
3. update `ORCHESTRATOR_PUBLIC_WEBHOOK_URL`
4. verify any shared secret values match

## Safe fallback

If the live path is unstable:

1. show the portal baseline
2. explain the cache-pressure trigger
3. show the operator console flow with fallback evidence text
4. explain the policy and approval gate
5. close on why validation matters
