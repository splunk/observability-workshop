# 1. Student Collector

## Goal

Validate the namespace-scoped Splunk OpenTelemetry Collector gateway for your student environment.

The gateway receives OTLP telemetry from the ShopMate Sports website workload and exports it to Splunk Observability Cloud. The app uses the standard OpenTelemetry `deployment.environment` resource attribute so you can filter your lab environment without adding custom tags.

The Kubernetes service may be named `shopmate-ai`. Treat that as the technical service name for the ShopMate Sports website.

## Why Gateway Mode

The lab uses one collector gateway per student namespace. This is intentionally different from a normal full-cluster Kubernetes collector install.

| Mode | Kubernetes shape | What it is good for | Why we use or avoid it here |
| --- | --- | --- | --- |
| Agent or node mode | DaemonSet on every node | Node, host, kubelet, container log, and per-node enrichment | Useful for platform telemetry, but too broad for student namespaces and can duplicate data if every student deploys it |
| Cluster receiver | Deployment or StatefulSet | Cluster metrics, Kubernetes objects, and events | Useful once per cluster, but not per student because it needs broader permissions and would duplicate shared cluster data |
| Gateway mode | Deployment plus ClusterIP service | Receives app OTLP telemetry, batches it, and exports to Splunk | Best fit for this lab because each namespace gets an isolated endpoint without node or cluster-wide collection |

In this workshop the gateway service name is `student-collector`, so ShopMate sends telemetry to:

```text
http://student-collector:4318
```

The full node/agent collector belongs in a shared platform or instructor namespace if the lab needs cluster-wide Kubernetes, node, or log telemetry. Student namespaces should not each run their own DaemonSet collector.

## Step 1: Confirm Your Namespace

```bash
kubectl get pods -n "$STUDENT_NAMESPACE"
kubectl auth can-i get pods -n "$STUDENT_NAMESPACE"
kubectl auth can-i create deployments -n "$STUDENT_NAMESPACE"
kubectl auth can-i create services -n "$STUDENT_NAMESPACE"
```

Expected result:

- commands succeed for your namespace
- you do not need cluster-admin permissions

Debug if this fails:

```bash
kubectl config current-context
kubectl get pods -n "$STUDENT_NAMESPACE"
kubectl auth can-i --list -n "$STUDENT_NAMESPACE"
```

If `kubectl auth can-i --list` does not show normal namespaced permissions, stop and ask the instructor to fix your Kubernetes access.

## Step 2: Confirm The Splunk Token Secret

The instructor preloads the Splunk Observability Cloud ingest token into every student namespace before class. You only need to confirm that the Kubernetes Secret exists in your namespace.

```bash
kubectl get secret "$SPLUNK_ACCESS_TOKEN_SECRET" -n "$STUDENT_NAMESPACE"
```

Expected result:

- the Secret named by `SPLUNK_ACCESS_TOKEN_SECRET` exists
- you do not print the token value

Debug if the command fails:

```bash
kubectl get secret -n "$STUDENT_NAMESPACE"
kubectl config current-context
```

If the Secret is missing, stop and ask the instructor to preload `splunk-observability-token` in your namespace. If collector logs later show `401 "Unauthorized"`, the Kubernetes deployment is running but Splunk rejected the credential. Ask the instructor to validate the preloaded token, organization, and realm. Do not paste tokens into chat, docs, or shell history.

## Step 3: Review The Baseline Helm Values

We use the official Splunk OpenTelemetry Collector Helm chart and pin the chart version for repeatability.

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update splunk-otel-collector-chart
helm search repo splunk-otel-collector-chart/splunk-otel-collector --versions | head
```

Current lab pin, selected for the May 31, 2026 lab build:

```text
splunk-otel-collector-chart/splunk-otel-collector 0.153.0
```

You will create `student-collector-values.yaml` in the next step with one full copy/paste command. The starter content is intentionally a baseline gateway. It receives OTLP from instrumented apps and exports to Splunk. It does not scrape GPU or NIM metrics yet.

Why these settings matter:

- `agent.enabled=false` prevents a per-student DaemonSet.
- `clusterReceiver.enabled=false` prevents duplicated cluster-level metrics and events.
- `gateway.enabled=true` creates the namespace-local OTLP endpoint.
- `gateway.extraEnvs` carries the lab identity values the collector needs when it enriches telemetry.
- `gateway.config.receivers.otlp` listens on OTLP gRPC `4317` and OTLP HTTP `4318`.
- `resource/environment` adds `deployment.environment` and `k8s.cluster.name` to telemetry that passes through the collector.
- the `traces` and `metrics` pipelines activate only the OTLP receiver for the first deployment.
- the baseline `metrics` pipeline is intentionally unfiltered so GenAI app metrics from Module 2 can reach Splunk AI Agent Monitoring.
- `rbac.create=false` and `serviceAccount.name=student` keep the collector inside student namespace permissions.
- `secret.create=false` tells Helm to use the existing Secret named by `SPLUNK_ACCESS_TOKEN_SECRET`.
- `k8s_attributes: null` removes a default processor that expects broader Kubernetes lookup permissions. ShopMate sends `deployment.environment` as a standard resource attribute.

The starter file should not include these GPU/NIM scrape components yet:

```text
DCGM_SCRAPE_TARGET
NIM_SCRAPE_TARGET
prometheus/gpu_nim
filter/gpu_nim_allowlist
```

You will add those in [Module 3](module-3-gpu-nim-scraping.md), redeploy the same collector, and then compare the difference in Splunk Observability Cloud. Module 3 adds a separate GPU/NIM metrics pipeline; it does not put the GPU/NIM allowlist on the app OTLP metrics pipeline.

## Step 4: Create The Core Collector Config

This is your first observability file change. Copy and paste the entire block below into your terminal to create a new file named `student-collector-values.yaml`.

Do not paste this command block into `student-collector-values.yaml` with an editor. The command creates the file for you.

The command uses the variables you set in [Before You Start](prerequisites.md#set-your-lab-variables). If one of those variables is missing, it stops before writing the file.

```bash
: "${STUDENT_ID:?Set STUDENT_ID from your lab handout first}"
: "${STUDENT_NAMESPACE:?Set STUDENT_NAMESPACE from your lab handout first}"
: "${LOGICAL_CLUSTER_NAME:?Set LOGICAL_CLUSTER_NAME from your lab handout first}"
: "${SPLUNK_REALM:?Set SPLUNK_REALM from your lab handout first}"
: "${SPLUNK_ACCESS_TOKEN_SECRET:?Set SPLUNK_ACCESS_TOKEN_SECRET to splunk-observability-token first}"

cat > student-collector-values.yaml <<EOF
fullnameOverride: student-collector
clusterName: "$LOGICAL_CLUSTER_NAME"

agent:
  enabled: false

clusterReceiver:
  enabled: false

gateway:
  enabled: true
  replicaCount: 1
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: "1"
      memory: 512Mi
  extraEnvs:
    - name: STUDENT_ID
      value: "$STUDENT_ID"
    - name: STUDENT_NAMESPACE
      value: "$STUDENT_NAMESPACE"
    - name: LOGICAL_CLUSTER_NAME
      value: "$LOGICAL_CLUSTER_NAME"
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    processors:
      k8s_attributes: null
      resource/environment:
        attributes:
          - key: deployment.environment
            value: \${env:STUDENT_ID}
            action: upsert
          - key: k8s.cluster.name
            value: \${env:LOGICAL_CLUSTER_NAME}
            action: upsert
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, resource/environment, batch]
          exporters: [otlp_http, signalfx]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, resource/environment, batch]
          exporters: [signalfx]

rbac:
  create: false

serviceAccount:
  create: false
  name: student

secret:
  create: false
  name: "$SPLUNK_ACCESS_TOKEN_SECRET"
  validateSecret: false

splunkObservability:
  realm: "$SPLUNK_REALM"
EOF
```

Review the generated file before deploying it:

| Config section | Required outcome |
| --- | --- |
| `clusterName` | Uses your logical cluster name |
| `gateway.extraEnvs` | Provides `STUDENT_ID`, `STUDENT_NAMESPACE`, and `LOGICAL_CLUSTER_NAME` to the collector pod |
| `gateway.config.receivers.otlp` | Receives app traces and metrics on `4317` and `4318` |
| `gateway.config.exporters.signalfx.send_otlp_histograms` | Preserves GenAI histogram metrics required by Splunk AI Agent Monitoring |
| `gateway.config.processors.resource/environment` | Adds standard environment and cluster attributes to telemetry that passes through the collector |
| `gateway.config.service.pipelines.traces` | Sends app traces through `memory_limiter`, `resource/environment`, and `batch` to Splunk APM with `otlp_http`; `signalfx` remains enabled for correlation metadata |
| `gateway.config.service.pipelines.metrics` | Sends app OTLP metrics through the same baseline processor path to Splunk |
| `splunkObservability.realm` | Matches the Splunk realm from your lab handout |

Validate that your file contains the core gateway components:

```bash
head -n 3 student-collector-values.yaml
grep -n \
  -e "$STUDENT_ID" \
  -e "$LOGICAL_CLUSTER_NAME" \
  -e "send_otlp_histograms" \
  -e "resource/environment" \
  -e "receivers: \\[otlp\\]" \
  -e "exporters: \\[otlp_http, signalfx\\]" \
  student-collector-values.yaml
```

Expected result:

- the first line is `fullnameOverride: student-collector`
- the file does not start with `:` or `cat > student-collector-values.yaml`
- your assigned `STUDENT_ID` exists
- your assigned `LOGICAL_CLUSTER_NAME` exists
- `send_otlp_histograms: true` exists under `gateway.config.exporters.signalfx`
- `resource/environment` exists
- traces and metrics pipelines list `receivers: [otlp]`
- the traces pipeline lists `exporters: [otlp_http, signalfx]`

If the file starts with `:` or `cat > student-collector-values.yaml`, you pasted the command into the file instead of running it. Delete the file, then rerun the full command block above in your terminal.

Confirm the GPU/NIM scrape components are still absent:

```bash
grep -n "prometheus/gpu_nim\\|filter/gpu_nim_allowlist\\|DCGM_SCRAPE_TARGET\\|NIM_SCRAPE_TARGET" student-collector-values.yaml \
  || echo "GPU/NIM scrape config is not enabled yet"
```

Expected result:

- the command prints `GPU/NIM scrape config is not enabled yet`
- your file still keeps `agent.enabled=false` and `clusterReceiver.enabled=false`

## Step 5: Deploy The Gateway

```bash
helm upgrade --install student-collector splunk-otel-collector-chart/splunk-otel-collector \
  --version 0.153.0 \
  --namespace "$STUDENT_NAMESPACE" \
  --values student-collector-values.yaml
```

Reset only your namespace resources if you need to reinstall:

```bash
helm uninstall student-collector -n "$STUDENT_NAMESPACE"
kubectl delete -n "$STUDENT_NAMESPACE" deploy/student-collector svc/student-collector configmap/student-collector-otel-collector --ignore-not-found
```

Then rerun the matching Helm command.

## Step 6: Validate Kubernetes Health

```bash
helm list -n "$STUDENT_NAMESPACE"
kubectl get deploy,svc,pods -n "$STUDENT_NAMESPACE" -l app=splunk-otel-collector
kubectl rollout status deploy/student-collector -n "$STUDENT_NAMESPACE"
kubectl logs -n "$STUDENT_NAMESPACE" deploy/student-collector --tail=100
```

Look for:

- Helm release status is `deployed`
- `deployment/student-collector` is `1/1`
- service `student-collector` exposes OTLP HTTP `4318` and OTLP gRPC `4317`
- collector logs say the service is ready
- no repeated `401 "Unauthorized"` exporter errors

More inspection:

```bash
kubectl get deploy,rs,pod,svc,cm -n "$STUDENT_NAMESPACE" -l app=splunk-otel-collector -o wide
kubectl logs -n "$STUDENT_NAMESPACE" deploy/student-collector --previous --tail=100
```

Common patterns:

| Symptom | What to inspect |
| --- | --- |
| `CrashLoopBackOff` | `kubectl logs --previous` for bad YAML, bad component names, or missing environment variables |
| `ImagePullBackOff` | image name, registry access, and image pull secret |
| `CreateContainerConfigError` | missing preloaded Secret, invalid Secret contents, or missing ConfigMap |
| `401 "Unauthorized"` | Splunk realm, token type, token org, or preloaded Secret contents |
| no app telemetry | ShopMate `OTEL_EXPORTER_OTLP_ENDPOINT`, collector service port `4318`, and app logs |

For `CreateContainerConfigError`, inspect the pod event:

```bash
kubectl describe pod -n "$STUDENT_NAMESPACE" -l app=splunk-otel-collector
```

If the event references the Splunk Secret or its token key, ask the instructor to recreate the preloaded Secret. Do not inspect Secret data yourself.

## Step 7: Record The Collector Baseline

Run a local baseline check from your terminal:

```bash
grep -n "prometheus/gpu_nim\\|filter/gpu_nim_allowlist\\|DCGM_SCRAPE_TARGET\\|NIM_SCRAPE_TARGET" student-collector-values.yaml \
  || echo "GPU/NIM scraping is not configured yet"

kubectl logs -n "$STUDENT_NAMESPACE" deploy/student-collector --tail=100
```

Expected result:

- the collector is running and ready
- OTLP receivers are listening on `4317` and `4318`
- no GPU/NIM scrape config exists yet
- no repeated Splunk exporter errors

Do not search Splunk for `job=nim` or `job=dcgm` yet. Module 1 has not enabled those scrape targets, so missing GPU/NIM results in Splunk are expected and do not indicate a broken collector.

This check matters because Module 3 is a collector configuration exercise. You will add Prometheus scrape targets, redeploy the collector, and then verify that new `job=nim` and `job=dcgm` metrics appear in Splunk under the same `deployment.environment`.

!!! success "Checkpoint"
    Your gateway collector pod is running, has a service, and has OTLP gRPC and HTTP receivers ready. This module proves the collector gateway is healthy; it does not prove Splunk has GPU or NIM metrics yet.

## Knowledge Check

??? question "Why are we using gateway mode instead of a node collector?"
    Gateway mode gives each student namespace a stable OTLP endpoint without requiring DaemonSet, kubelet, host filesystem, or cluster-wide permissions.

??? question "Where does the Splunk environment filter come from?"
    ShopMate sends `deployment.environment` through `OTEL_RESOURCE_ATTRIBUTES` for app telemetry. The collector also has a `resource/environment` processor so collector-scraped metrics in later modules get the same standard filter.

??? question "What does `401 Unauthorized` in collector logs mean?"
    The collector reached Splunk, but Splunk rejected the credential. Confirm your `SPLUNK_REALM` value matches the lab handout, then ask the instructor to validate the preloaded token and Splunk organization.

## Sources

- Splunk documents Helm-based Kubernetes collector configuration, including EKS options and using a gateway endpoint for instrumented applications: [Configure with Helm](https://help.splunk.com/en?resourceId=gdi_opentelemetry_collector-kubernetes_kubernetes-config).
- Splunk documents agent, cluster receiver, and gateway customization through `agent.config`, `clusterReceiver.config`, and `gateway.config`: [Advanced configuration](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/collector-for-kubernetes/advanced-configuration).
- Splunk explains collector deployment modes and gateway forwarding behavior: [Deployment modes](https://help.splunk.com/en?resourceId=gdi_opentelemetry_deployment-modes).
- The lab uses the official Splunk Helm chart and release stream: [Splunk OpenTelemetry Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) and [chart releases](https://github.com/signalfx/splunk-otel-collector-chart/releases).
- OpenTelemetry documents collector troubleshooting patterns used when checking pipelines and collector health: [OpenTelemetry Collector troubleshooting](https://opentelemetry.io/docs/collector/troubleshooting/).
