# ShopMate AI Pods Lab Project

This directory is a focused local copy of the source material for a Cisco Live
instructor-led lab about observing a Cisco AI POD-inspired AI/ML environment
with Splunk.

Run source-preview and app-maintenance commands from this directory:

```bash
cd workshop/clus-shopmate-exercises
```

The lab uses a shared Kubernetes GPU environment, NVIDIA NIM, OpenTelemetry, and
instrumented sample AI applications to show how operators can connect
infrastructure health, application traces, model behavior, token usage, and
chargeback data.

The project is intentionally text-first. Lab guides, planning notes, sample
apps, deployment assets, and validation material live together so the workshop
can be edited, tested, and published from one place.

## What This Repo Contains

- `workshop/` - main attendee-facing lab guide for `CLUS-LTROBS-2001`
- `shopmate-sports/` - retail AI app used by the main lab
- `infra/` - Terraform and Kubernetes assets for the instructor-managed lab environment
- `docs/` - project notes, setup plans, telemetry design, and validation checklists

This copy intentionally omits the alternate TicketMate workshop, editor/agent
rule files, raw Codex archives, and large presentation/PDF deliverables.

## Lab Theme

Students work through a realistic observability flow:

1. Deploy a namespace-scoped OpenTelemetry Collector.
2. Instrument an AI application.
3. Collect GPU and NIM metrics.
4. Correlate app behavior with infrastructure signals in Splunk.
5. Investigate token usage, cost, and chargeback attribution.

The lab uses real Kubernetes, GPU, NIM, application, and OpenTelemetry signals
where practical. Cisco UCS, Nexus, and storage behavior may be simulated or
represented conceptually unless those integrations are explicitly deployed.

## Local Preview

Main workshop:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

## More Detail

Use these files when you need implementation detail:

- `PLANNING.md` - current build plan
- `docs/PROJECT_BRIEF.md` - project goals and audience
- `infra/README.md` - infrastructure overview
- `shopmate-sports/README.md` - ShopMate app notes
- `ticketmate-ai/README.md` - TicketMate app notes
