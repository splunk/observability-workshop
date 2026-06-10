# Quick Start

This is the shortest reliable path to a working workshop run.

## Outcome

At the end of this flow you should have:

- the docs site running locally
- the app stack running locally
- optional collector telemetry running
- the claims portal and operator console reachable
- a healthy starting state
- a deterministic cache-pressure incident
- a clear path through approval and recovery

## 1. Confirm tools

You need:

- Node.js and `npm`
- Python 3
- Docker Desktop or another local Docker daemon if you want the collector
- Splunk and OpenAI credentials if you want live telemetry and model-backed remediation

## 2. Install and serve docs

From the repo root:

```bash
python3 -m pip install -r requirements-docs.txt
python3 -m mkdocs serve -a 127.0.0.1:18082
```

Open `http://127.0.0.1:18082/`.

## 3. Create `.env`

From the repo root:

```bash
cp .env.example .env
```

Set these for a full shared-account lab:

```dotenv
INSTANCE=student-001
SPLUNK_ACCESS_TOKEN=...
SPLUNK_REALM=...
OPENAI_API_KEY=...
GALILEO_API_KEY_FILE=/path/to/galileo_api_key
```

Each student should use a different `INSTANCE`, such as `student-014`.

## 4. Install dependencies

```bash
npm install
python3 -m venv apps/remediation-agent/.venv
apps/remediation-agent/.venv/bin/pip install --index-url https://pypi.org/simple -e apps/remediation-agent
```

## 5. Start the collector

Use this only when you are validating telemetry:

```bash
set -a
source .env
set +a
npm run dev:collector
```

The collector listens on host OTLP ports `14317` and `14318`. Inside Docker it still listens on standard collector ports `4317` and `4318`.

## 6. Start the app stack

In another terminal:

```bash
set -a
source .env
set +a
npm run dev:all
```

Expected result:

- backend services bind to high local ports
- the Python remediation agent starts on `18800`
- Vite starts the portal on `18080`
- Vite starts the operator console on `18081`

## 7. Open the two main UIs

- claims portal: `http://127.0.0.1:18080`
- operator console: `http://127.0.0.1:18081`

## 8. Establish a healthy baseline

Before showing a fault:

1. Run `AI Claim Status`.
2. Run `Policy Coverage Lookup`.
3. Run `Claims FAQ Search`.
4. Confirm the operator console has no stale incident blocking the flow.

## 9. Trigger the incident

Use `Trigger Cache Pressure` from the portal or operator console.

Then:

1. Run `AI Claim Status` again.
2. Keep the other two transactions as healthy comparisons.
3. Open Splunk APM and Infrastructure Monitoring.
4. Look for claims-knowledge latency and filesystem utilization for the student `INSTANCE`.
5. Open the operator console.
6. Leave `Evidence Intake` blank unless you are using fallback operator notes.
7. Click `Gather MCP Evidence`.
8. Click `Explain`.
9. Click `Propose`.

## 10. Complete the remediation story

The intended live sequence is:

1. Show customer impact first.
2. Show the default Splunk signals: RUM/APM plus host filesystem metrics.
3. Use [Splunk Validation](splunk-validation.md) to confirm RUM, APM, infrastructure, MCP, remediation, and Galileo evidence.
4. Walk through orchestrator evidence and confidence.
5. Show approval-required policy.
6. Propose `clean_claims_knowledge_cache`.
7. Approve the action.
8. Verify recovery.

## If anything breaks

Go straight to [Troubleshooting](troubleshooting.md).
