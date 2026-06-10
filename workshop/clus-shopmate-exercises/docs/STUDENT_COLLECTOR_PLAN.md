# Student Collector Plan

## Purpose

Students should deploy their own OpenTelemetry Collector as part of the workshop. The student collector focuses on application telemetry and GPU/NIM scraping. Kubernetes metrics are collected by the instructor collector only.

The selected pattern is now **workshop-compatible mode**, which intentionally mimics the original workshop participant experience as closely as possible while keeping this lab's retail app and scenarios original.

The pattern is:

- instructor deploys the setup prerequisites and the authoritative Kubernetes/infrastructure collector
- each student deploys a Splunk OpenTelemetry Collector in their own namespace
- each student's `shopmate-ai` app sends OTLP data to that student's collector
- each student collector exports directly to Splunk Observability Cloud
- each student collector is tagged with a unique logical `k8s.cluster.name`
- each student collector scrapes shared DCGM and NIM metrics directly
- Kubernetes metrics are not collected by student collectors

This keeps the lab simpler than the original workshop while still preserving the most important hands-on learning: app instrumentation, collector deployment, GPU scraping, NIM scraping, and tokenomics.

## Exact Workshop-Compatible Mode

If the goal is to match the original workshop as closely as possible, each student should:

1. Deploy the Splunk OpenTelemetry Collector with Helm in their own namespace.
2. Use a unique logical cluster name, for example `clus-ltrobs-2001-student-01`.
3. Use a unique environment name, for example `student-01`.
4. Export directly to Splunk using the instructor-provided realm and token.
5. Verify the collector is exporting to Splunk.
6. Update the collector configuration to scrape NVIDIA DCGM exporter.
7. Update the collector configuration to scrape NVIDIA NIM `/v1/metrics`.
8. Validate GPU and NIM dashboards or charts.
9. Deploy or validate `shopmate-ai` in their namespace.
10. Configure `shopmate-ai` to send OTLP to their collector.
11. Instrument `shopmate-ai` for AI Agent Monitoring.
12. Run retail traffic and tokenomics scenarios.

Key logical identity:

```text
k8s.cluster.name=clus-ltrobs-2001-student-01
deployment.environment=student-01
student.id=student-01
k8s.namespace.name=student-01
```

This preserves the useful logical isolation pattern from the original workshop without requiring each student to collect Kubernetes metrics.

## Tradeoff

Workshop-compatible mode is a better learning experience, but it creates duplicated metrics.

Expected duplication:

- DCGM GPU metrics per student
- NIM metrics per student

This is acceptable for a 20-student lab if guardrails are applied:

- use one student namespace per participant
- use unique `k8s.cluster.name` per participant
- apply the workshop-compatible metric allowlist
- use `60s` scrape interval unless testing proves `10s` is safe
- keep collector resource limits
- avoid unnecessary additional integrations

The instructor collector remains useful as the clean baseline and troubleshooting source.

## Collector Responsibilities

### Instructor collector

Runs once for the whole cluster.

Collects:

- Kubernetes node and pod metadata
- GPU/DCGM metrics
- NIM metrics
- cluster-level infrastructure metrics

Owned by:

- instructor or platform team

### Student collector

Runs once per student namespace.

Collects:

- traces from that student's `shopmate-ai` app
- zero-code app metrics from Splunk OpenAI/OpenAI Agents instrumentation
- token and chargeback metrics
- optional app logs
- optional scrape of that student's app `/metrics` endpoint
- scrape of shared DCGM and NIM Prometheus endpoints for the GPU instrumentation exercise

Owned by:

- student

## Student Learning Outcome

Each student learns to:

1. Install a collector in Kubernetes.
2. Configure an OTLP receiver.
3. Configure batching and resource attributes.
4. Configure direct export to Splunk Observability Cloud.
5. Point the app to the collector.
6. Validate that traces and metrics arrive in Splunk.
7. Add dimensions such as `student.id`, `team.name`, and `chargeback.account`.

## Recommended Architecture

```text
student namespace

shopmate-ai app
  -> OTLP HTTP/gRPC
  -> student collector
  -> Splunk Observability Cloud

student collector
  -> Prometheus scrape
  -> shared DCGM exporter and shared NIM /v1/metrics endpoint

student collector
shared platform namespace

GPU Operator + DCGM + NIM
  -> instructor collector
  -> Splunk Observability Cloud

Kubernetes API / kubelet / kube-state-metrics
  -> instructor collector
  -> Splunk Observability Cloud
```

## Deployment Decision: Student Collector Exports Directly To Splunk

This is the selected workshop design.

Each student collector needs:

- Splunk realm
- Splunk ingest token
- environment name
- student/team attributes

Pros:

- easiest to understand
- each student has a complete end-to-end collector path
- fewer moving parts

Cons:

- every student can see or use an ingest token unless the lab hides it in a Kubernetes Secret
- harder to centrally enforce filtering

For this lab, the instructor will provide the Splunk realm and token. Prefer using a lab-scoped ingest token with limited blast radius.

## Alternative: Student Collector Exports To Instructor Gateway

This is not the selected design, but it remains a fallback if token handling becomes a problem.

In this fallback option, each student collector sends OTLP to a shared instructor-managed gateway collector. Only the gateway has the Splunk ingest token.

Pros:

- students do not need Splunk ingest tokens
- instructor can centrally filter, batch, and route data
- simpler governance

Cons:

- students deploy a collector, but not the final Splunk exporter
- one more component for the instructor to run

Use only if direct student export becomes operationally risky.

## GPU Scraping Adaptation

To make the exercise closer to the original workshop, each student can add a Prometheus receiver to their namespace collector that scrapes:

- NVIDIA DCGM exporter metrics
- NVIDIA NIM metrics

This teaches the mechanics students need:

- finding exporter endpoints
- configuring a Prometheus receiver
- filtering high-volume metrics
- adding a metrics pipeline
- validating GPU and NIM data in Splunk

Important boundary:

- students are scraping the same shared physical GPU/NIM endpoints
- each student gets a logical view of GPU metrics, not isolated GPU hardware
- metrics are duplicated per student collector unless filtered and scoped carefully

Recommended guardrails:

- deploy student collector as a `Deployment`, not a DaemonSet
- do not enable full `clusterReceiver` per student
- do not enable broad Kubernetes node scraping per student
- scrape DCGM and NIM at `60s` by default, or `120s` if ingest pressure is high
- use the workshop-compatible metric allowlist in [`docs/GPU_NIM_METRIC_STRATEGY.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/GPU_NIM_METRIC_STRATEGY.md)
- set collector CPU and memory limits
- add `student.id`, `team.name`, and `environment` resource attributes
- teach students not to aggregate all student environments together when reviewing shared GPU charts

For 20 students, this should be feasible if the metric allowlist and scrape interval are controlled. The larger risk is not GPU exhaustion; it is duplicate metric ingest, confusing dashboards, higher cardinality, and unnecessary load on the Kubernetes API or exporters.

## Recommended Student GPU Metrics Scope

Start with the workshop-compatible allowlist, not the reduced list.

Reason:

- it is more likely to populate out-of-the-box dashboard panels
- the original workshop describes the filter list as metrics used by charts or detectors
- the lab objective is to teach realistic GPU/NIM collection, not only a toy subset

See [`docs/GPU_NIM_METRIC_STRATEGY.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/GPU_NIM_METRIC_STRATEGY.md) for the full list and fallback reduced list.

Fallback reduced list if resource or ingest pressure is high:

```text
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
DCGM_FI_DEV_FB_FREE
DCGM_FI_DEV_GPU_TEMP
DCGM_FI_DEV_POWER_USAGE
DCGM_FI_PROF_GR_ENGINE_ACTIVE
DCGM_FI_PROF_PIPE_TENSOR_ACTIVE
```

Start with a small NIM allowlist:

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

## Student Collector Minimum Config

The student collector should run as a Kubernetes `Deployment`, not a DaemonSet.

It should expose:

- OTLP gRPC on `4317`
- OTLP HTTP on `4318`
- health check on `13133`

It should include:

- `otlp` receiver
- `memory_limiter` processor
- `batch` processor
- `resource` processor adding student metadata
- Splunk `signalfx`/OTLP exporter direct to Splunk Observability Cloud

Example logical config:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 256
  resource/student:
    attributes:
      - action: upsert
        key: student.id
        value: ${env:STUDENT_ID}
      - action: upsert
        key: team.name
        value: ${env:TEAM_NAME}
      - action: upsert
        key: k8s.namespace.name
        value: ${env:POD_NAMESPACE}
  batch: {}

exporters:
  signalfx:
    access_token: ${env:SPLUNK_ACCESS_TOKEN}
    realm: ${env:SPLUNK_REALM}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, resource/student, batch]
      exporters: [otlp_http, signalfx]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, resource/student, batch]
      exporters: [signalfx]
```

## Student App Configuration

Each student's app sends telemetry to the collector in the same namespace:

```text
OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=shopmate-ai
STUDENT_ID=student-01
TEAM_NAME=team-a
CHARGEBACK_ACCOUNT=cb-student-01
```

## Workshop Exercise

### Exercise 1: Deploy Your Collector

Student steps:

1. Open the assigned namespace.
2. Review the collector values or manifest.
3. Set `STUDENT_ID`, `TEAM_NAME`, `SPLUNK_REALM`, and `SPLUNK_ACCESS_TOKEN`.
4. Deploy the collector.
5. Verify collector pod is running.
6. Check collector logs for export errors.

Expected result:

- one collector pod is running in the student namespace
- collector health endpoint is available
- no authentication or connection errors appear in logs

### Exercise 2: Point The App To Your Collector

Student steps:

1. Set `OTEL_EXPORTER_OTLP_ENDPOINT` on `shopmate-ai`.
2. Restart the app deployment.
3. Send a retail prompt.
4. Confirm the app logs show a successful request.
5. Confirm the collector logs show received/exported telemetry.

Expected result:

- app traces flow through the student collector
- Splunk shows traces for that `student.id`

### Exercise 3: Add Business Attributes

Student steps:

1. Add or validate `student.id`.
2. Add or validate `chargeback.account`.
3. Add or validate `retail.intent`.
4. Send a second request.
5. Find the trace in Splunk and inspect attributes.

Expected result:

- traces and metrics can be filtered by `student.id`
- token metrics can be grouped by `chargeback.account`

### Exercise 4: Tokenomics Challenge

Student steps:

1. Run baseline shopping traffic.
2. Run promo campaign, token surge, or `agent-loop-token-burn` traffic.
3. Query token totals by student.
4. Identify the most expensive student.
5. If the loop scenario was used, inspect repeated `CatalogAgent` and NIM spans.
6. Explain whether the spend was properly chargeback-tagged and whether it came from normal demand or agent-loop behavior.

Expected result:

- students can find the top token spender using Splunk
- students can explain the relationship between app usage, token volume, and cost attribution
- students can identify a bounded agent loop from trace shape and guardrail attributes

## GPU Instrumentation Exercise

Students should learn GPU monitoring by configuring their collector to scrape a small, controlled set of GPU and NIM metrics.

Use this pattern:

1. Instructor collector gathers authoritative GPU/DCGM and NIM metrics once.
2. Student collector scrapes the same shared DCGM and NIM endpoints using a limited config.
3. Students query their logical GPU/NIM metric view in Splunk.
4. Students correlate their app traces, token surge, or agent-loop token burn with shared GPU/NIM behavior.
5. Instructor explains why duplicate scraping is acceptable for a lab but usually not ideal in production.

Optional advanced exercise:

- provide a non-production mock DCGM or NIM metrics endpoint per namespace
- have students add a Prometheus receiver in their collector to scrape only that mock endpoint

Do not use 20 student collectors to scrape every Kubernetes or node endpoint. If students scrape real DCGM/NIM endpoints, keep the scrape target list narrow and filtered.

## Kubernetes Metrics Decision

Kubernetes metrics are instructor-only.

Use this pattern:

- instructor collector gathers authoritative cluster-wide Kubernetes metrics
- students filter Kubernetes metrics by `k8s.namespace.name`
- app traces include `k8s.namespace.name`, `k8s.pod.name`, `k8s.container.name`, and `service.name`
- correlation happens through shared Kubernetes resource attributes

This teaches correlation without making students debug Kubernetes RBAC or duplicate cluster metrics.

Students should use these filters:

```text
k8s.namespace.name=student-01
service.name=shopmate-ai
k8s.deployment.name=shopmate-ai
```

Student collector does not collect:

- kubelet/cAdvisor metrics
- kube-state-metrics
- Kubernetes events
- node metrics
- clusterReceiver data

Why:

- EKS Kubernetes metric permissions are more complex than the app/GPU/NIM exercises
- duplicated Kubernetes collection adds noise
- the workshop goal is to teach app instrumentation and AI infrastructure scraping
- this split is closer to production, where platform teams own broad cluster telemetry

## Reference To Original Workshop Pattern

The public Splunk Cisco AI Pods workshop uses a similar split: the setup installs a collector with only cluster-level components enabled while workshop participants install their own agent in their namespace. Participants then modify their collector to scrape NVIDIA DCGM and NIM metrics. This project can reuse that teaching pattern while keeping the app and scenarios original.

## Definition Of Done

The student collector exercise is ready when:

- each student can deploy a namespace collector without cluster-admin privileges
- app telemetry flows through the student collector
- infrastructure/GPU telemetry remains collected once by the instructor collector as the authoritative view
- student collectors scrape limited shared DCGM/NIM metrics for the exercise
- Kubernetes metrics are visible from the instructor collector and filterable by student namespace
- Splunk can filter app traces and metrics by `student.id`
- tokenomics and chargeback exercises still work
