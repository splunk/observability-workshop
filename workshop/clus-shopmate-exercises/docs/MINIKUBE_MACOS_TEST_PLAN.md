# Minikube macOS Test Plan

## Purpose

This plan makes the workshop testable on a macOS laptop with Minikube before the full EKS/GPU environment exists.

The local Minikube path validates:

- `shopmate-ai` app deployment
- student collector deployment
- OTLP app telemetry path
- AI Agent Monitoring instrumentation shape
- safe prompt capture
- tokenomics attributes
- department and conversation tagging
- bounded agent-loop token burn behavior
- fake GPU/DCGM Prometheus scrape
- fake NIM Prometheus scrape
- leaderboard and multi-turn conversation flow

It does not validate:

- real NVIDIA GPU scheduling
- real DCGM metrics
- real NVIDIA NIM inference
- real GPU pressure
- production EKS RBAC
- Cisco UCS/Nexus/storage telemetry

## Local Architecture

```text
macOS laptop
  -> Minikube
      -> namespace student-01
          -> shopmate-ai
          -> student-collector
          -> fake-nim
          -> fake-dcgm-exporter
      -> optional namespace instructor
          -> optional mock/instructor collector
```

Telemetry path:

```text
shopmate-ai
  -> OTLP
  -> student-collector
  -> Splunk Observability Cloud

student-collector
  -> Prometheus scrape
  -> fake-dcgm-exporter
  -> fake-nim /v1/metrics
  -> Splunk Observability Cloud
```

## macOS Prerequisites

Required:

```text
Docker Desktop or compatible container runtime
minikube
kubectl
helm
curl
```

Optional:

```text
python3
jq
```

Students do not need this Minikube path for the Cisco Live lab. This is for developers and instructors building/testing the workshop.

## Minikube Start

Recommended local cluster:

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

Enable useful add-ons:

```bash
minikube addons enable metrics-server
minikube addons enable ingress
```

Validate:

```bash
kubectl get nodes
kubectl get pods -A
```

## Namespaces

Create one test student namespace:

```bash
kubectl create namespace student-01
```

Optional instructor namespace:

```bash
kubectl create namespace instructor
```

## Required Secrets

For direct export to Splunk:

```bash
kubectl create secret generic splunk-access-token \
  --namespace student-01 \
  --from-literal=SPLUNK_ACCESS_TOKEN='<token>'
```

Create config values as needed:

```bash
kubectl create configmap lab-identity \
  --namespace student-01 \
  --from-literal=STUDENT_ID='student-01' \
  --from-literal=TEAM_NAME='team-a' \
  --from-literal=DEPARTMENT_NAME='marketing' \
  --from-literal=DEPARTMENT_COST_CENTER='cc-4100' \
  --from-literal=DEPLOYMENT_ENVIRONMENT='student-01' \
  --from-literal=K8S_CLUSTER_NAME='clus-ltrobs-2001-student-01' \
  --from-literal=CHARGEBACK_ACCOUNT='cb-student-01'
```

## Fake NIM Service

Use a lightweight mock service that exposes:

- OpenAI-compatible chat endpoint if possible
- `/v1/metrics` with NIM-like Prometheus metrics

Minimum fake `/v1/metrics` output should include:

```text
num_requests_running
num_requests_waiting
prompt_tokens_total
generation_tokens_total
request_success_total
request_failure_total
e2e_request_latency_seconds
time_to_first_token_seconds
time_per_output_token_seconds
request_prompt_tokens
request_generation_tokens
http.server.active_requests
```

For first pass, fake NIM can be a simple app that returns static or incrementing Prometheus metrics.

Service name expected by collector:

```text
fake-nim.student-01.svc.cluster.local:8000
```

## Fake DCGM Exporter

Use a lightweight mock exporter that exposes DCGM-like Prometheus metrics.

Minimum fake metrics:

```text
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
DCGM_FI_DEV_FB_FREE
DCGM_FI_DEV_GPU_TEMP
DCGM_FI_DEV_POWER_USAGE
DCGM_FI_PROF_GR_ENGINE_ACTIVE
DCGM_FI_PROF_PIPE_TENSOR_ACTIVE
```

Service name expected by collector:

```text
fake-dcgm-exporter.student-01.svc.cluster.local:9400
```

## shopmate-ai Local Mode

Run `shopmate-ai` in fake NIM mode:

```text
NIM_MODE=fake
NIM_BASE_URL=http://fake-nim.student-01.svc.cluster.local:8000/v1
NIM_MODEL=meta/llama-3.2-1b-instruct
OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=shopmate-ai
OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
```

Resource attributes:

```text
student.id=student-01
team.name=team-a
department.name=marketing
department.cost_center=cc-4100
k8s.namespace.name=student-01
deployment.environment=student-01
k8s.cluster.name=clus-ltrobs-2001-student-01
```

## Student Collector Local Config

The Minikube student collector should match the real lab pattern:

- OTLP receiver
- resource processor
- batch processor
- memory limiter
- direct Splunk exporter
- Prometheus receiver scraping fake NIM
- Prometheus receiver scraping fake DCGM

Scrape targets:

```text
fake-dcgm-exporter.student-01.svc.cluster.local:9400
fake-nim.student-01.svc.cluster.local:8000/v1/metrics
```

Use the same metric allowlist as the real lab where possible.

## Local Validation Flow

### Step 1: Start Minikube

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

### Step 2: Deploy fake endpoints

Deploy:

- `fake-nim`
- `fake-dcgm-exporter`

Validate:

```bash
kubectl port-forward -n student-01 svc/fake-nim 8000:8000
curl http://localhost:8000/v1/metrics
```

```bash
kubectl port-forward -n student-01 svc/fake-dcgm-exporter 9400:9400
curl http://localhost:9400/metrics
```

### Step 3: Deploy student collector

Deploy collector in `student-01`.

Validate:

```bash
kubectl get pods -n student-01
kubectl logs -n student-01 deploy/student-collector
```

### Step 4: Deploy shopmate-ai

Deploy app in `student-01`.

Validate:

```bash
kubectl port-forward -n student-01 svc/shopmate-ai 8080:8080
curl http://localhost:8080/healthz
```

### Step 5: Send a retail prompt

```bash
curl -X POST http://localhost:8080/v1/chat \
  -H 'content-type: application/json' \
  -d '{
    "student_id": "student-01",
    "team": "team-a",
    "department": "marketing",
    "department_cost_center": "cc-4100",
    "namespace": "student-01",
    "chargeback_account": "cb-student-01",
    "conversation_id": "conv-student-01-001",
    "conversation_turn_index": 1,
    "prompt": "Find a waterproof running shoe under $120 and explain why it is a good choice.",
    "scenario": "baseline",
    "max_tokens": 256
  }'
```

### Step 6: Run a multi-turn conversation

Send 5 turns using the same `conversation_id` and incrementing `conversation_turn_index`.

Validate:

- traces appear in Splunk
- prompt content appears for synthetic prompt where supported
- `conversation.id` is present
- `department.name` is present
- token totals increase

### Step 7: Validate fake GPU/NIM metrics

In Splunk, search/filter by:

```text
deployment.environment=student-01
k8s.cluster.name=clus-ltrobs-2001-student-01
student.id=student-01
```

Confirm metrics:

```text
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
num_requests_running
num_requests_waiting
prompt_tokens_total
generation_tokens_total
e2e_request_latency_seconds
```

### Step 8: Run the bounded agent-loop scenario

```bash
curl -X POST http://localhost:8080/v1/chat \
  -H 'content-type: application/json' \
  -d '{
    "student_id": "student-01",
    "team": "team-a",
    "department": "marketing",
    "department_cost_center": "cc-4100",
    "namespace": "student-01",
    "chargeback_account": "cb-student-01",
    "conversation_id": "conv-student-01-loop-001",
    "conversation_turn_index": 1,
    "prompt": "Find waterproof trail running shoes under $40, available today, with carbon plate support, in every color, and explain all alternatives in detail.",
    "scenario": "agent-loop-token-burn",
    "max_tokens": 512
  }'
```

Validate:

- the request returns instead of running indefinitely
- traces show repeated `CatalogAgent` or `agent.catalog.search` spans
- loop attributes include `ai.agent.loop.detected=true` and `ai.agent.stop_reason=max_iterations_exceeded`
- token totals exceed the baseline request

## What This Proves

Minikube proves:

- manifests are valid
- namespace model works
- app runs in Kubernetes
- collector runs in Kubernetes
- app-to-collector OTLP works
- collector-to-Splunk export works
- fake GPU/NIM scraping works
- GenAI spans and tokenomics attributes work
- bounded agent-loop token burn is observable and guarded
- free multi-turn conversation produces chargeback data

Minikube does not prove:

- GPU Operator behavior
- actual DCGM behavior
- actual NIM latency or queueing
- real GPU saturation
- EKS IAM/RBAC behavior
- out-of-the-box Cisco AI POD dashboard parity

## Build Agent Instructions

Implementation agents should add a `local/minikube/` path:

```text
local/minikube/
  README.md
  fake-nim.yaml
  fake-dcgm-exporter.yaml
  student-collector.yaml
  shopmate-ai.yaml
  validate.sh
```

The `validate.sh` script should check:

- Minikube cluster reachable
- namespace exists
- fake NIM metrics reachable
- fake DCGM metrics reachable
- student collector running
- `shopmate-ai` running
- one chat request succeeds
- agent-loop-token-burn request succeeds and stops at the guardrail

Do not block local testing on real NIM or real GPUs.
