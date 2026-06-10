---
title: Troubleshooting
linkTitle: 9. Troubleshooting
weight: 9
archetype: chapter
time: 15 minutes
description: Recover from collector, app, trace, GPU, NIM, and Splunk filter issues.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **workshop facilitator**. Your goal is to restore the lab path while preserving the evidence-based investigation workflow.
{{% /notice %}}

## Fast Triage

Start with:

```bash
kubectl get all -n "$STUDENT_NAMESPACE"
kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=100
kubectl logs deploy/shopmate-ai -n "$STUDENT_NAMESPACE" --tail=100
```

Use this order:

1. Confirm Kubernetes resources are running.
2. Confirm the app can reach the collector.
3. Confirm the collector can export to Splunk.
4. Confirm Splunk filters are not too narrow.
5. Confirm the time range includes your latest request.

## Collector CrashLoopBackOff

Inspect previous logs:

```bash
kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --previous
```

Common causes:

- Invalid YAML.
- Missing token Secret.
- Unsupported collector component name.
- Bad environment variable substitution.

Reset if needed:

```bash
helm uninstall student-collector -n "$STUDENT_NAMESPACE"
kubectl delete deploy/student-collector svc/student-collector configmap/student-collector-otel-collector \
  -n "$STUDENT_NAMESPACE" --ignore-not-found
```

Then recreate `student-collector-values.yaml` from the Module 1 baseline.

## Helm Cannot Parse Values

Inspect the file:

```bash
head -n 5 student-collector-values.yaml
```

The first line should be:

```text
fullnameOverride: student-collector
```

If the file starts with shell command text, you saved the command into the file instead of running it. Delete the file and rerun the creation command.

## Collector Exports Nothing

Confirm:

- The app points to `http://student-collector:4318`.
- OTLP receivers are enabled.
- The Splunk exporter has the correct realm and token Secret.
- The collector logs do not show repeated `401 Unauthorized` or DNS errors.

## ShopMate Traces Are Missing

Check:

```bash
kubectl get deploy/shopmate-ai -n "$STUDENT_NAMESPACE" -o yaml | grep -E "OTEL_|NIM_|SHOPMATE_"
kubectl logs deploy/shopmate-ai -n "$STUDENT_NAMESPACE" --tail=100
```

Then:

1. Generate a fresh browser request.
2. Wait a minute.
3. Search with a recent time range.
4. Start with `service.name=shopmate-ai`.
5. Add `deployment.environment=<STUDENT_ID>` only after confirming traces exist.

## AI Overview Is Empty But Traces Exist

Check two collector settings:

- The collector must preserve OTLP histogram metrics.
- The GPU/NIM allowlist filter must not apply to the OTLP app metrics pipeline.

The app metrics pipeline must stay unfiltered. Only the separate `metrics/gpu_nim` pipeline should use `filter/gpu_nim_allowlist`.

## GPU or NIM Metrics Are Missing

Test from the namespace:

```bash
kubectl run scrape-test -n "$STUDENT_NAMESPACE" --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 -- \
  curl -sS "http://${DCGM_SCRAPE_TARGET}/metrics"

kubectl run nim-test -n "$STUDENT_NAMESPACE" --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 -- \
  curl -sS "http://${NIM_SCRAPE_TARGET}/v1/metrics"
```

If DNS works but `curl` fails, check service name, port, path, or NetworkPolicy with the instructor.

## Token Metrics Are Missing

Check:

- The app is started with Splunk/OpenTelemetry instrumentation.
- GenAI emitters are enabled.
- The NIM/OpenAI-compatible request is actually executed.
- Splunk search uses the correct metric name for the installed package version.

The source app notes are in:

```bash
workshop/clus-shopmate-exercises/shopmate-sports/README.md
```
