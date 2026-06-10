---
title: Student Collector
linkTitle: 3. Student Collector
weight: 3
archetype: chapter
time: 35 minutes
description: Deploy and validate a namespace-scoped Splunk OpenTelemetry Collector gateway.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **collector owner** for your namespace. Your goal is to receive app OTLP telemetry and export it to Splunk without duplicating cluster-wide data.
{{% /notice %}}

## Why Gateway Mode?

The lab uses one collector gateway per student namespace.

| Mode | Kubernetes shape | Why it is or is not used here |
| --- | --- | --- |
| Agent or node mode | DaemonSet on every node | Useful for platform telemetry, but too broad for student namespaces and can duplicate data. |
| Cluster receiver | Deployment or StatefulSet | Useful once per cluster, but not per student because it needs broader permissions. |
| Gateway mode | Deployment plus ClusterIP service | Best fit because each namespace gets an isolated OTLP endpoint. |

The gateway service name is:

```text
student-collector
```

ShopMate sends telemetry to:

```text
http://student-collector:4318
```

## Add the Splunk Collector Helm Chart

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update
```

## Create Baseline Values

Use the source lab as the detailed reference:

```bash
workshop/clus-shopmate-exercises/workshop/module-1-collector.md
```

Your baseline collector values should:

- Set `fullnameOverride: student-collector`.
- Enable OTLP HTTP and gRPC receivers.
- Export traces and metrics to Splunk Observability Cloud.
- Add `deployment.environment=$STUDENT_ID`.
- Use the preloaded Kubernetes Secret for the ingest token.
- Avoid node, host, kubelet, and cluster-wide receivers in the student namespace.

## Install the Collector

```bash
helm upgrade --install student-collector "$COLLECTOR_CHART" \
  -n "$STUDENT_NAMESPACE" \
  -f student-collector-values.yaml
```

Validate rollout:

```bash
kubectl rollout status deploy/student-collector -n "$STUDENT_NAMESPACE"
kubectl get pods -n "$STUDENT_NAMESPACE" -l app=splunk-otel-collector
kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=100
```

Expected result:

- Collector pod is ready.
- Logs do not show repeated export errors.
- The OTLP receiver is available inside your namespace.

## Checkpoint

Before continuing, record:

| Item | Value |
| --- | --- |
| Student namespace | |
| `deployment.environment` | |
| Collector service | `student-collector` |
| OTLP endpoint | `http://student-collector:4318` |
| Splunk realm | |
