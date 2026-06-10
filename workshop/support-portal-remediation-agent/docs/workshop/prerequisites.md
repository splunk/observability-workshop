# Prerequisites

Use this pre-flight checklist before debugging application code.

## Required software

### Node.js and npm

```bash
node --version
npm --version
```

### Python 3

```bash
python3 --version
```

### Docker

Required for the local collector and Docker Compose flow.

```bash
docker --version
docker info
```

### Optional: cloudflared

Only needed for optional live detector webhook delivery.

```bash
cloudflared --version
```

## Credentials

Recommended for a realistic workshop:

- `SPLUNK_ACCESS_TOKEN`
- `SPLUNK_REALM`
- `OPENAI_API_KEY`
- `GALILEO_API_KEY_FILE` or `GALILEO_API_KEY`
- `VITE_SPLUNK_RUM_TOKEN`

If credentials are missing:

- the local app still runs
- telemetry export to Splunk is absent or partial
- the remediation agent uses fallback logic when no OpenAI key is present
- Galileo agent monitoring is disabled when no Galileo key is present

## Ports

Default local layout:

- `18080` claims portal
- `18081` operator console
- `18082` docs, when served with the workshop command
- `18100` API gateway
- `18101` assistant service
- `18102` case service
- `18103` knowledge service
- `18104` scenario controller
- `18110` remediation orchestrator
- `18800` remediation agent
- `14318` collector OTLP HTTP on host

Check for collisions:

```bash
lsof -i :18080 -i :18081 -i :18082 -i :18100 -i :18101 -i :18102 -i :18103 -i :18104 -i :18110 -i :18800 -i :14318
```

## Required local files

- repo checked out locally
- `.env` if using real credentials
- `apps/remediation-agent/.venv` after Python setup

## Presenter setup

Recommended windows:

- claims portal
- operator console
- Splunk Observability Cloud
- terminal running the app stack
- terminal running the collector, if telemetry export is enabled

## Final go/no-go checklist

- Node and npm work
- Python 3 works
- Docker is running if collector is needed
- dependencies are installed
- remediation agent virtual environment exists
- each student has a unique `INSTANCE`
- intended local ports are free
