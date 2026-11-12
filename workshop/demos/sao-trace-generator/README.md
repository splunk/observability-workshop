# SAO Trace Generator

Replays a fixed set of Splunk Agent Observability traces on a schedule, so demos and
workshop exercises always have deterministic data without running the real application.
It is designed to run as a Kubernetes CronJob (every 30 minutes).

## How it works

`input.csv` is a span export from Agent Observability (healthcare assistant scenario:
4 traces, 50 spans — agent, workflow, tool, LLM, retriever and Agent Control spans).
Each run of `generate_traces.py`:

- sends all 4 traces through `SplunkAOLogger`, including the Agent Control (`control`) spans
- generates new trace, span, session and tool-call IDs
- re-bases timestamps so the traces end "now"
- keeps the original relative timing and durations, with ±15% jitter per trace
- does **not** send evaluation metrics (instruction/context adherence) — Agent Observability
  computes those on ingest
- groups traces that shared a conversation in the source into the same new session

Intentional failures in the source (the hallucinated dosage answer, PII that the
Agent Control steer rule catches) are replayed as-is.

### Known limitation

`SplunkAOLogger` treats tool spans as leaves. In the source data a tool span contains
child spans (an LLM call, or the retrieval chain). On replay those children appear as
siblings of the tool span, under the `tools` workflow span, rather than nested in it.

## Configuration

| Variable | Source | Purpose |
|---|---|---|
| `SPLUNK_AO_REALM` | ConfigMap | Splunk Observability Cloud realm, e.g. `us1` |
| `SPLUNK_AO_PROJECT` | ConfigMap | Agent Observability project name (required) |
| `SPLUNK_AO_AGENT_STREAM` | ConfigMap | Agent stream name (defaults to `default`) |
| `SPLUNK_AO_O11Y_TOKEN` | Secret | Splunk Observability Cloud access token |

### Create the Secret and ConfigMap

```bash
kubectl create secret generic sao-trace-generator-secret \
  --from-literal=SPLUNK_AO_O11Y_TOKEN='<your-o11y-access-token>'

kubectl create configmap sao-trace-generator-config \
  --from-literal=SPLUNK_AO_REALM='us1' \
  --from-literal=SPLUNK_AO_PROJECT='Healthcare Assistant Demo' \
  --from-literal=SPLUNK_AO_AGENT_STREAM='ctf'
```

Use the same namespace as the CronJob (add `-n <namespace>` to each command).

## Build and deploy

```bash
docker build -t ghcr.io/splunk/sao-trace-generator:1.0 --platform linux/amd64 .
docker push ghcr.io/splunk/sao-trace-generator:1.0

# edit the image in cronjob.yaml if you used a different name, then:
kubectl apply -f cronjob.yaml

# run once immediately to test
kubectl create job --from=cronjob/sao-trace-generator sao-trace-generator-test
kubectl logs job/sao-trace-generator-test
```

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate_traces.py --dry-run          # print span trees, send nothing

export SPLUNK_AO_REALM=us1 SPLUNK_AO_PROJECT='Healthcare Assistant Demo' \
       SPLUNK_AO_AGENT_STREAM=ctf SPLUNK_AO_O11Y_TOKEN='<your-o11y-access-token>'
python generate_traces.py
```

Options: `--input <csv>`, `--jitter <fraction>`, `--seed <int>`, `-v`.

## Changing the traces

Edit `input.csv` (same columns as an Agent Observability span export, without
`project_id`) and rebuild the image. Before committing a new export, check it for real
customer or personal data and remove the `project_id` column.
