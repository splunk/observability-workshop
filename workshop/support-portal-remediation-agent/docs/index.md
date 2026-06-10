# Cisco Live 2026 Workshop Runbook

This site is the operator guide for running the `IBOBS-2002` workshop from this repository.

The goal is to get the environment running reliably, explain the architecture clearly, and give the presenter a step-by-step path for triggering a metric-driven incident and walking through governed remediation.

## What this repo demonstrates

- a customer-facing AI claims portal
- one degraded customer journey and two healthy comparison journeys
- Splunk RUM, APM, host filesystem metrics, and Galileo remediation-agent instrumentation
- a remediation orchestrator that turns investigation evidence into structured policy input
- a bounded remediation agent with approval and validation
- a repeatable cache-pressure scenario that does not depend on logs or custom app metrics

## Recommended reading order

1. [Quick Start](workshop/quickstart.md)
2. [Prerequisites](workshop/prerequisites.md)
3. [Environment Setup](workshop/environment.md)
4. [Install and Start](workshop/install-and-start.md)
5. [Splunk Validation](workshop/splunk-validation.md)
6. [Live Demo Flow](workshop/live-demo-flow.md)
7. [Troubleshooting](workshop/troubleshooting.md)

## Serve the docs locally

From the repo root:

```bash
python3 -m pip install -r requirements-docs.txt
python3 -m mkdocs serve -a 127.0.0.1:18082
```

Then open `http://127.0.0.1:18082/`.

## Core customer story

A company launches an AI-powered claims portal. During peak usage, the claims knowledge cache volume fills up and degrades the `AI Claim Status` workflow. Splunk observability surfaces customer impact, service latency, and filesystem pressure. The remediation orchestrator collects evidence, applies policy, asks for approval, executes `clean_claims_knowledge_cache`, and verifies recovery.

## Fast facts

- Claims portal: `http://127.0.0.1:18080`
- Operator console: `http://127.0.0.1:18081`
- API gateway: `http://127.0.0.1:18100`
- Assistant service: `http://127.0.0.1:18101`
- Case service: `http://127.0.0.1:18102`
- Knowledge service: `http://127.0.0.1:18103`
- Scenario controller: `http://127.0.0.1:18104`
- Remediation orchestrator: `http://127.0.0.1:18110`
- Remediation agent: `http://127.0.0.1:18800`
- Collector OTLP HTTP on host: `http://127.0.0.1:14318`
