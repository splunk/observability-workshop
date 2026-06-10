---
title: Prepare the Environment
linkTitle: 2. Prepare the Environment
weight: 2
archetype: chapter
time: 20 minutes
description: Install prerequisites, configure credentials and student identity, and verify local port availability.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **platform engineer** preparing a reliable lab environment. Your goal is to make the local app, Splunk evidence path, and optional agent monitoring path predictable before the incident starts.
{{% /notice %}}

## Required Software

Check your local tools:

```bash
node --version
npm --version
python3 --version
docker --version
docker info
```

Docker is required for the local collector and Docker Compose path. `cloudflared` is optional and is only needed if you test live detector webhook delivery.

## Configure the App Copy

Change into the local workshop copy:

```bash
cd workshop/support-portal-remediation-agent
```

Create a local environment file:

```bash
test -f .env || cp .env.example .env
```

Edit `.env` and set a unique `INSTANCE` value:

```dotenv
INSTANCE=student-001
OTEL_RESOURCE_ATTRIBUTES=lab.name=ciscolive26,lab.student.id=student-001,service.instance.id=student-001,host.name=student-001,deployment.environment=demo
```

Use a unique value for every student when sharing one Splunk Observability Cloud organization. This keeps traces, metrics, dashboards, and detector filters separated.

## Credentials

Recommended values for the full workshop:

```dotenv
SPLUNK_ACCESS_TOKEN=
SPLUNK_REALM=us1
VITE_SPLUNK_RUM_TOKEN=
OPENAI_API_KEY=
GALILEO_API_KEY=
GALILEO_API_KEY_FILE=
```

If credentials are missing:

- The local app still runs.
- Splunk telemetry export is absent or partial.
- The remediation agent uses fallback logic when no OpenAI key is present.
- Galileo monitoring is disabled when no Galileo key is present.

## Install Dependencies

Install Node workspace dependencies:

```bash
npm install
```

Create the remediation agent virtual environment:

```bash
python3 -m venv apps/remediation-agent/.venv
apps/remediation-agent/.venv/bin/pip install --index-url https://pypi.org/simple -e apps/remediation-agent
```

## Check Ports

The default local layout is:

| Port | Service |
| --- | --- |
| `18080` | claims portal |
| `18081` | operator console |
| `18100` | API gateway |
| `18101` | assistant service |
| `18102` | case service |
| `18103` | knowledge service |
| `18104` | scenario controller |
| `18110` | remediation orchestrator |
| `18800` | remediation agent |
| `14318` | collector OTLP HTTP endpoint |

Check for collisions:

```bash
lsof -i :18080 -i :18081 -i :18100 -i :18101 -i :18102 -i :18103 -i :18104 -i :18110 -i :18800 -i :14318
```

Resolve any conflicting process before starting the lab.
