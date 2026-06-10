# Build Ready Checklist

## Purpose

This checklist turns the workshop design into build tasks for implementation agents.

The first build should prove the end-to-end learning path:

```text
student collector -> app instrumentation -> prompt/agent flow -> GPU/NIM scrape -> Kubernetes correlation -> tokenomics challenge
```

## Build Workstreams

### 0. Local Minikube Test Build

Deliver:

- `local/minikube/README.md`
- fake NIM deployment and service
- fake DCGM exporter deployment and service
- student collector manifest
- `shopmate-ai` local deployment
- local validation script

Validation:

- Minikube starts on macOS
- fake NIM `/v1/metrics` is reachable
- fake DCGM `/metrics` is reachable
- student collector starts
- `shopmate-ai` starts in fake NIM mode
- one retail request succeeds
- traces and metrics reach Splunk if credentials are provided

### 1. App Build

Deliver:

- `shopmate-ai` FastAPI app
- static retail catalog
- shopping, catalog, inventory, checkout, policy, and cost agent functions
- OpenAI-compatible NIM client
- fake NIM mode for local testing
- SQLite token ledger
- leaderboard endpoint

Validation:

- `GET /healthz` returns success
- `POST /v1/chat` returns a retail answer
- fake NIM mode works without a GPU
- real NIM mode uses `NIM_BASE_URL` and `NIM_API_KEY`

### 2. App Instrumentation Build

Deliver:

- FastAPI tracing
- GenAI workflow instrumentation
- agent invocation instrumentation
- LLM invocation instrumentation around NIM
- safe prompt capture with synthetic prompts
- token and cost metrics
- chargeback attributes
- department and cost-center attributes
- conversation ID and turn-index attributes

Validation:

- Splunk shows workflow, agent, and LLM spans
- prompt and response content appear where supported
- token fields appear on traces and metrics
- token usage can be grouped by department and conversation
- traces filter by `student.id`

### 3. Student Collector Build

Deliver:

- Helm values or manifests for one collector per student namespace
- OTLP receiver for app telemetry
- Splunk direct exporter
- resource attributes for student/environment identity
- Prometheus receiver for DCGM and NIM
- workshop-compatible GPU/NIM metric allowlist

Validation:

- collector pod starts
- collector exports directly to Splunk
- app telemetry arrives through the collector
- GPU/NIM metrics arrive under student tags

### 4. Instructor Infrastructure Build

Owner:

- `Agent 1: Instructor Lab Setup Agent`

Primary instructions:

- [`docs/INSTRUCTOR_LAB_SETUP_AGENT.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/INSTRUCTOR_LAB_SETUP_AGENT.md)

Deliver:

- accounts and access guide
- EKS or Kubernetes setup guide
- GPU node setup
- NVIDIA GPU Operator
- NVIDIA NIM endpoint
- instructor collector for Kubernetes metrics and authoritative platform baseline
- per-student namespaces and RBAC
- student collector templates
- `shopmate-ai` deployment template
- validation scripts
- teardown guide

Validation:

- AWS, Splunk, NVIDIA/NGC, Kubernetes, and registry access are verified
- NIM serves requests
- DCGM endpoint is reachable
- NIM `/v1/metrics` is reachable
- Kubernetes metrics are visible in Splunk and filterable by namespace
- one test student namespace works end to end
- teardown prevents orphaned GPU instances

### 5. Scenario Build

Deliver:

- baseline shopping traffic
- free multi-turn conversation traffic
- promo campaign traffic
- token surge traffic
- agent-loop token burn traffic
- missing chargeback tag traffic
- optional retry storm

Validation:

- scenario changes are visible in traces
- token totals increase during surge
- agent-loop token burn shows repeated agent spans and stops at a max-iteration guardrail
- leaderboard identifies a top spender
- leaderboard can identify top department and top conversation
- missing tags are visible

### 6. Lab Content Build

Deliver:

- attendee lab guide
- instructor guide
- setup guide
- validation guide
- slide outline
- troubleshooting appendix

Validation:

- every module has expected results
- every module has a recovery path
- 4-hour timing fits
- final challenge can be completed from collected data

## Build Order

1. Build Minikube local test path.
2. Verify instructor accounts and access.
3. Build `shopmate-ai` with fake NIM.
4. Add token ledger and leaderboard.
5. Add GenAI instrumentation and safe prompt capture.
6. Build local OTLP collector path.
7. Add student collector Kubernetes manifest.
8. Add GPU/NIM scrape config.
9. Deploy one namespace end to end.
10. Validate Splunk traces, AI Agent Monitoring, and GPU/NIM metrics.
11. Scale to three test students.
12. Scale to 20 students.
13. Write final lab guide from validated commands.

Instructor setup should be built in parallel with app work, but must be validated before scaling past one test student.

## Non-Negotiable Build Rules

- Do not require students to collect Kubernetes metrics.
- Do not require students to deploy DaemonSets.
- Do not require students to debug cluster RBAC.
- Do not use real sensitive prompt data.
- Do not build Cisco UCS/Nexus synthetic metrics in the first pass.
- Do not make dashboard parity claims until validated in Splunk.
- Do not require real GPUs for Minikube validation.

## First End-To-End Test

Use `student-01`.

Expected evidence:

- `shopmate-ai` pod running
- `student-collector` pod running
- one retail request trace visible
- workflow span visible
- agent spans visible
- LLM invocation visible
- prompt content visible for synthetic prompt
- token metrics visible
- bounded agent-loop scenario visible with repeated `CatalogAgent` spans
- DCGM metrics visible
- NIM metrics visible
- Kubernetes metrics visible from instructor collector filtered by `k8s.namespace.name=student-01`
- leaderboard shows `student-01`
