---
title: GPU and NIM Scraping
linkTitle: 5. GPU and NIM Scraping
weight: 5
archetype: chapter
time: 40 minutes
description: Extend the student collector to scrape selected DCGM and NVIDIA NIM Prometheus metrics.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **platform telemetry engineer** adding model-serving and accelerator evidence to the same Splunk environment as your app traces.
{{% /notice %}}

## What You Are Scraping

The source lab uses two shared Prometheus endpoints:

```bash
export DCGM_SCRAPE_TARGET=nvidia-dcgm-exporter.gpu-operator.svc.cluster.local:9400
export NIM_SCRAPE_TARGET=nim-service.nim-system.svc.cluster.local:8000
```

Confirm with your instructor before using different targets.

## Test The Targets

Test DCGM:

```bash
kubectl run scrape-test -n "$STUDENT_NAMESPACE" --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 -- \
  curl -sS "http://${DCGM_SCRAPE_TARGET}/metrics"
```

Test NIM:

```bash
kubectl run nim-test -n "$STUDENT_NAMESPACE" --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 -- \
  curl -sS "http://${NIM_SCRAPE_TARGET}/v1/metrics"
```

Expected result:

- Both commands return Prometheus-formatted metrics.

Cleanup:

```bash
kubectl delete pod scrape-test nim-test -n "$STUDENT_NAMESPACE" --ignore-not-found
```

## Snapshot The Collector File

```bash
cp student-collector-values.yaml student-collector-values.before-gpu-nim.yaml
grep -n "prometheus/gpu_nim\\|filter/gpu_nim_allowlist\\|DCGM_SCRAPE_TARGET\\|NIM_SCRAPE_TARGET" student-collector-values.yaml \
  || echo "No GPU/NIM scrape config yet"
```

## Add GPU and NIM Scraping

Use the source reference snippets:

```bash
workshop/clus-shopmate-exercises/workshop/lab-files/collector-observability-snippet.yaml
workshop/clus-shopmate-exercises/workshop/lab-files/student-collector-values-gpu-nim-reference.yaml
```

The final collector config should:

- Add a Prometheus receiver for DCGM and NIM endpoints.
- Add a separate `metrics/gpu_nim` pipeline.
- Apply metric filtering only to the GPU and NIM pipeline.
- Preserve normal OTLP app metrics for AI Agent Monitoring.
- Add `deployment.environment=$STUDENT_ID` to scraped metrics.

{{% notice title="Avoid A Common Mistake" style="warning" %}}
Do not apply the GPU/NIM allowlist filter to the main OTLP app metrics pipeline. That can hide GenAI app metrics needed by Splunk AI Agent Monitoring.
{{% /notice %}}

## Upgrade The Collector

```bash
helm upgrade --install student-collector "$COLLECTOR_CHART" \
  -n "$STUDENT_NAMESPACE" \
  -f student-collector-values.yaml
```

Validate:

```bash
kubectl rollout status deploy/student-collector -n "$STUDENT_NAMESPACE"
kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=100
```

## Splunk Validation

After several scrape intervals, search metrics with:

```text
deployment.environment=<your student id> job=dcgm
deployment.environment=<your student id> job=nim
```

Expected result:

- GPU metrics arrive with `job=dcgm`.
- NIM metrics arrive with `job=nim`.
- ShopMate traces and GenAI metrics still appear under the same `deployment.environment`.
