# Instructor Lab Setup Agent

## Mission

Build the instructor-owned lab foundation for `CLUS-LTROBS-2001`.

This agent owns everything students should not have to build during the 4-hour lab:

- shared Kubernetes/GPU platform
- NVIDIA GPU Operator
- NVIDIA NIM endpoint
- instructor OpenTelemetry Collector for Kubernetes metrics and authoritative platform baseline
- per-student namespaces, RBAC, and secrets
- student collector templates
- `shopmate-ai` deployment templates
- accounts and access plan
- validation scripts
- teardown instructions

Students should arrive with a working namespace and focus on:

- deploying their student collector
- instrumenting `shopmate-ai`
- scraping GPU/NIM metrics
- analyzing tokenomics and chargeback

## Inputs

Read these first:

1. [`PLANNING.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/PLANNING.md)
2. [`docs/STUDENT_COLLECTOR_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/STUDENT_COLLECTOR_PLAN.md)
3. [`docs/GPU_NIM_METRIC_STRATEGY.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/GPU_NIM_METRIC_STRATEGY.md)
4. [`docs/APP_INSTRUMENTATION_EXERCISES.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/APP_INSTRUMENTATION_EXERCISES.md)
5. [`docs/BUILD_READY_CHECKLIST.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/BUILD_READY_CHECKLIST.md)
6. [`docs/ACCOUNTS_AND_ACCESS_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/ACCOUNTS_AND_ACCESS_PLAN.md)

## Assumptions

Default platform:

- AWS EKS
- `2 x g5.4xlarge` GPU worker nodes for the pilot
- one student namespace per participant
- 20 students
- one `shopmate-ai` deployment per student namespace
- one student collector per student namespace
- student collectors export directly to Splunk Observability Cloud
- instructor provides Splunk realm and ingest token
- Kubernetes metrics are collected only by the instructor collector
- students scrape shared DCGM/NIM endpoints from their collectors
- Cisco UCS/Nexus synthetic metrics are parked
- local Minikube testing uses fake NIM and fake DCGM before EKS is available

## Required Outputs

Create or update these files:

```text
infra/
  README.md
  accounts-and-access.md
  instructor-setup.md
  teardown.md
  validation.md
  terraform/
    README.md
    versions.tf
    providers.tf
    variables.tf
    locals.tf
    network.tf
    eks.tf
    addons.tf
    kubernetes.tf
    ecr.tf
    outputs.tf
    backend/
      dev.hcl.example
    env/
      dev.tfvars.example
  eks/
    cluster.md
    node-groups.md
    cost-notes.md
  k8s/
    namespaces.yaml
    rbac-students.yaml
    instructor-collector-values.yaml
    gpu-operator-values.yaml
    nim-values.yaml
    shopmate-ai-template.yaml
    student-collector-template.yaml
    student-collector-gpu-nim-scrape-values.yaml
    secrets-template.yaml
  scripts/
    create-student-namespaces.sh
    validate-instructor-platform.sh
    validate-student-namespace.sh
    generate-student-roster.sh
```

If implementation time is limited, prioritize:

```text
infra/instructor-setup.md
infra/accounts-and-access.md
infra/validation.md
infra/k8s/namespaces.yaml
infra/k8s/instructor-collector-values.yaml
infra/k8s/student-collector-template.yaml
infra/k8s/student-collector-gpu-nim-scrape-values.yaml
infra/k8s/shopmate-ai-template.yaml
```

## Phase 0: Accounts And Access

Complete this before platform setup.

Tasks:

1. Verify AWS account permissions and GPU quota.
2. Verify Splunk Observability org, realm, users, and ingest token.
3. Verify NVIDIA/NGC access and NIM model entitlement.
4. Verify container registry access.
5. Preload the lab-scoped Splunk token as the `splunk-observability-token` Kubernetes Secret in every student namespace.
6. Decide student Kubernetes access method.
7. Generate the student roster.

Required output:

- `infra/accounts-and-access.md`
- roster file or roster generation script
- list of required secrets
- student access distribution process

Follow [`docs/ACCOUNTS_AND_ACCESS_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/ACCOUNTS_AND_ACCESS_PLAN.md).

## Phase 0.5: Local Minikube Validation

Before building the full EKS environment, create a local Minikube validation path for macOS.

Purpose:

- validate manifests
- validate app instrumentation
- validate collector configuration
- validate fake GPU/NIM scraping
- validate tokenomics and multi-turn conversation flow

Required output:

- `local/minikube/README.md`
- `local/minikube/fake-nim.yaml`
- `local/minikube/fake-dcgm-exporter.yaml`
- `local/minikube/student-collector.yaml`
- `local/minikube/shopmate-ai.yaml`
- `local/minikube/validate.sh`

Follow [`docs/MINIKUBE_MACOS_TEST_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/MINIKUBE_MACOS_TEST_PLAN.md).

## Phase 1: Platform Setup

Document and automate the shared platform.

Tasks:

1. Create or document the EKS cluster.
2. Configure one GPU node group with `g5.4xlarge` instances.
3. Confirm GPU nodes can schedule NVIDIA workloads.
4. Install NVIDIA GPU Operator.
5. Confirm DCGM exporter is running.
6. Deploy NVIDIA NIM using the workshop-like shape.
7. Expose NIM service internally.
8. Confirm NIM `/v1/metrics` is reachable.

Validation commands must prove:

```text
kubectl get nodes
kubectl get pods -n gpu-operator
kubectl get svc -A | grep -i dcgm
kubectl get pods -A | grep -i nim
curl NIM_INTERNAL_SERVICE/v1/metrics
```

Use exact service names once validated. Do not leave ambiguous names like `<NIM_SERVICE>` in final setup docs unless they are unavoidable placeholders.

## Phase 2: Instructor Collector

Deploy the instructor collector as the authoritative platform telemetry path.

It should collect:

- Kubernetes cluster metrics
- Kubernetes pod/container metadata
- node metrics where available
- authoritative GPU/DCGM metrics
- authoritative NIM metrics

It should not be the endpoint students send app telemetry to.

Student collectors export directly to Splunk.

Validation:

- Kubernetes metrics appear in Splunk.
- Kubernetes metrics are filterable by `k8s.namespace.name`.
- GPU/DCGM metrics appear once as the instructor baseline.
- NIM metrics appear once as the instructor baseline.

Required documentation:

- where to find the instructor collector values
- what receivers are enabled
- what pipelines are enabled
- how to validate export errors
- what dashboards or metric searches prove success

## Phase 3: Student Namespaces

Prepare 20 student namespaces.

Namespace naming:

```text
student-01
student-02
...
student-20
```

Each namespace needs:

- namespace object
- student service account
- RBAC sufficient to deploy/read namespace resources
- Splunk realm value in the lab handout
- preloaded `splunk-observability-token` Secret
- app config placeholders
- collector config placeholders

Student identity mapping:

```text
student.id=student-01
team.name=team-a
department.name=marketing
department.cost_center=cc-4100
deployment.environment=student-01
k8s.cluster.name=clus-ltrobs-2001-student-01
k8s.namespace.name=student-01
chargeback.account=cb-student-01
```

Create a roster file with:

- student number
- namespace
- department
- cost center
- chargeback account
- app URL
- Splunk filters

## Phase 4: Student Collector Template

Prepare the collector template students will deploy.

Required features:

- OTLP HTTP receiver on `4318`
- OTLP gRPC receiver on `4317`
- direct Splunk exporter
- resource attributes for student identity
- batch processor
- memory limiter
- Prometheus receiver for DCGM
- Prometheus receiver for NIM `/v1/metrics`
- workshop-compatible GPU/NIM metric allowlist

Required guardrails:

- no DaemonSet
- no student `clusterReceiver`
- no student Kubernetes metrics collection
- no broad cluster RBAC
- conservative scrape interval, default `60s`
- collector CPU/memory limits

Validation:

- collector starts in `student-01`
- app can send OTLP to collector
- collector exports traces to Splunk
- collector scrapes DCGM metrics
- collector scrapes NIM metrics
- metrics are tagged with `student.id` and logical `k8s.cluster.name`

## Phase 5: shopmate-ai Student Deployment Template

Prepare one app deployment per student namespace.

Required environment variables:

```text
OTEL_SERVICE_NAME=shopmate-ai
OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_RESOURCE_ATTRIBUTES=student.id=student-01,team.name=team-a,department.name=marketing,department.cost_center=cc-4100,k8s.namespace.name=student-01,deployment.environment=student-01,k8s.cluster.name=clus-ltrobs-2001-student-01
OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
NIM_BASE_URL=<internal-nim-url>
NIM_API_KEY=<nim-api-key-or-placeholder>
CHARGEBACK_ACCOUNT=cb-student-01
```

The template should support:

- fake NIM mode for validation if NIM is not ready
- real NIM mode for the full lab
- department-specific identity
- conversation ID and turn index in API requests
- `agent-loop-token-burn` scenario requests with max-iteration and token-budget guardrails

## Phase 6: Student Access From Laptops

Document how students connect from their laptops.

Required decisions to document:

- kubeconfig distribution method
- whether students use `kubectl` locally
- whether access is namespace-scoped
- app URL or port-forward pattern
- Splunk login URL
- Splunk realm
- Splunk token handling

Preferred student commands should be simple:

```text
kubectl config use-context <lab-context>
kubectl get pods -n student-01
helm upgrade --install student-collector ...
kubectl apply -f shopmate-ai.yaml -n student-01
```

Avoid requiring students to debug AWS IAM, OIDC, IRSA, node groups, or cluster autoscaling.

## Phase 7: Validation Script

Create a single instructor validation script that checks:

- cluster reachable
- GPU nodes ready
- GPU Operator pods ready
- DCGM exporter reachable
- NIM pods ready
- NIM `/v1/metrics` reachable
- instructor collector running
- Kubernetes metrics visible in Splunk or local collector logs show successful export
- all 20 namespaces exist
- `student-01` can deploy collector
- `student-01` can deploy app
- `student-01` app trace reaches Splunk
- `student-01` GPU/NIM metrics reach Splunk
- `student-01` agent-loop-token-burn request returns and shows repeated `CatalogAgent` spans

If Splunk API validation is not implemented, document manual validation searches.

## Phase 8: Teardown

Create teardown instructions.

Must include:

- remove student apps
- remove student collectors
- remove NIM
- remove GPU Operator if needed
- remove instructor collector
- delete EKS cluster or scale GPU node group to zero
- verify no GPU instances remain running

Do not leave GPU instances running after the lab.

## Success Criteria

The instructor setup is ready when:

- the instructor can run one command or one documented sequence to validate the platform
- NIM is reachable and serving
- DCGM metrics are reachable
- instructor Kubernetes metrics are visible in Splunk
- one test student can deploy collector and app
- the test student's app trace appears in Splunk
- the test student's GPU/NIM scrape appears in Splunk
- tokenomics attributes are present
- prompt capture works for synthetic prompts
- agent-loop guardrail attributes are present when the loop scenario runs
- the setup can be repeated for 20 namespaces

## Explicit Non-Goals

Do not build these in the first pass:

- Cisco UCS synthetic telemetry
- Cisco Nexus synthetic telemetry
- Pure/NetApp storage simulation
- vector database simulation
- per-student Kubernetes metrics collection
- per-student DaemonSet collectors
- full production-grade identity federation

Park these items until the core lab path works end to end.
