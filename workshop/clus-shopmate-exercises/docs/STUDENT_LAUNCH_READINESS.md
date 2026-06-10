# Student Launch Readiness

## Current Status

Last validated: June 2, 2026.

Local student docs are ready:

- MkDocs strict build passes.
- Playwright student walkthrough passes against `http://127.0.0.1:8001/`.
- Student lab files are served by MkDocs:
  - `workshop/lab-files/collector-observability-snippet.yaml`
  - `workshop/lab-files/student-collector-values-gpu-nim-reference.yaml`
- YAML validation passes for the collector snippet and student collector values files.

Live cluster baseline is ready for `student-01` through `student-20`:

- Kubernetes context is `clus-ltrobs-2001-event`.
- All 20 student namespaces are active.
- All 20 namespaces have the preloaded `splunk-observability-token` Secret.
- Test workloads from `student-01`, `student-02`, and `student-05` were reset so students start clean.
- No `shopmate-ai`, `student-collector`, job, ingress, or PVC runtime resources remain in the student namespaces.

## Go/No-Go Gates

The lab is student-ready only when all gates pass.

| Gate | Status | Validation |
| --- | --- | --- |
| Student docs build | Passing | `.venv/bin/mkdocs build --strict` |
| Student docs walkthrough | Passing | `.venv/bin/python scripts/student_mkdocs_walkthrough.py --base-url http://127.0.0.1:8001/` |
| Student namespaces exist | Passing | `kubectl get ns student-01 ... student-20` |
| Splunk token Secret exists per namespace | Passing | `for ns in $(seq -f 'student-%02g' 1 20); do kubectl get secret splunk-observability-token -n "$ns"; done` |
| Student service port-forward RBAC | Passing | `for ns in $(seq -f 'student-%02g' 1 20); do kubectl auth can-i create pods/portforward --as=system:serviceaccount:workshop-access:workshop-students -n "$ns"; done` |
| Student namespaces start clean | Passing | no student namespace has residual `shopmate-ai`, `student-collector`, jobs, ingresses, or PVCs |
| Student collector deploys | Validate during smoke test | `helm list` and `kubectl rollout status deploy/student-collector` in one test namespace |
| ShopMate app deploys | Validate during smoke test | `kubectl rollout status deploy/shopmate-ai` in one test namespace |
| NIM endpoint reachable | Passing | curl from a temporary pod to `nim-service.nim-system.svc.cluster.local:8000/v1/metrics` |
| DCGM endpoint reachable | Passing | curl from a temporary pod to `nvidia-dcgm-exporter.gpu-operator.svc.cluster.local:9400/metrics` |
| ShopMate request uses NIM | Passing | `/api/chat` returned `nim_enabled: true` in both namespaces |
| Collector auth/export errors | Passing by logs | Fresh collector logs show no `401 Unauthorized`, `Exporting failed`, or dropped-data errors |
| Splunk traces visible | Manual UI confirmation still recommended | `service.name=shopmate-ai` with `deployment.environment=student-01` |
| Splunk GPU/NIM metrics visible | Manual UI confirmation still recommended after Module 3 scrape config | Separate searches for `deployment.environment=student-01 job=dcgm` and `deployment.environment=student-01 job=nim` |

## Pre-Class Repeat Checks

Run this sequence before opening the room or publishing the lab URL.

1. Confirm AWS and Kubernetes access.

   ```bash
   aws login
   kubectl config current-context
   ```

2. Confirm the expected cluster context.

   ```bash
   kubectl config current-context
   ```

   Expected:

   ```text
   clus-ltrobs-2001-event
   ```

3. Run the read-only namespace and preloaded Secret check.

   ```bash
   # Run this first after a rebuild or token rotation.
   # export SPLUNK_ACCESS_TOKEN='<lab-scoped-ingest-token>'
   # infra/scripts/preload-splunk-observability-token.sh

   kubectl get ns student-01 student-02 student-03 student-04 student-05 \
     student-06 student-07 student-08 student-09 student-10 \
     student-11 student-12 student-13 student-14 student-15 \
     student-16 student-17 student-18 student-19 student-20

   for ns in $(seq -f 'student-%02g' 1 20); do
     kubectl get secret splunk-observability-token -n "$ns"
     kubectl auth can-i create pods/portforward \
       --as=system:serviceaccount:workshop-access:workshop-students \
       -n "$ns"
     kubectl auth can-i get endpoints \
       --as=system:serviceaccount:workshop-access:workshop-students \
       -n "$ns"
     kubectl auth can-i list endpointslices.discovery.k8s.io \
       --as=system:serviceaccount:workshop-access:workshop-students \
       -n "$ns"
   done

   kubectl get deploy,svc,pod,job,ingress,pvc -A --ignore-not-found | rg '^student-' || true
   ```

4. Deploy or redeploy one test student collector.

   ```bash
   export STUDENT_ID=student-01
   export STUDENT_NAMESPACE=student-01
   export COLLECTOR_CHART=splunk-otel-collector-chart/splunk-otel-collector

   cp "infra/helm/student-collector-values-${STUDENT_ID}.yaml" student-collector-values.yaml

   helm upgrade --install student-collector "$COLLECTOR_CHART" \
     --version 0.153.0 \
     --namespace "$STUDENT_NAMESPACE" \
     --values student-collector-values.yaml

   kubectl rollout status deploy/student-collector -n "$STUDENT_NAMESPACE"
   kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=100
   ```

5. Validate one ShopMate app path.

   ```bash
   cp workshop/lab-files/shopmate-ai.yaml shopmate-ai.yaml
   kubectl apply -n "$STUDENT_NAMESPACE" -f shopmate-ai.yaml
   kubectl rollout status deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
   kubectl set env deploy/shopmate-ai -n "$STUDENT_NAMESPACE" \
     OTEL_SERVICE_NAME=shopmate-ai \
     OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318 \
     OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
     OTEL_RESOURCE_ATTRIBUTES="deployment.environment=${STUDENT_ID}" \
     NIM_BASE_URL=http://nim-service.nim-system.svc.cluster.local:8000/v1 \
     NIM_MODEL=meta/llama-3.2-1b-instruct \
     OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric \
     OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY \
     OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
   kubectl rollout status deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
   ```

6. Generate one test request.

   ```bash
   kubectl run shopmate-chat -n "$STUDENT_NAMESPACE" --rm -i --restart=Never \
     --image=curlimages/curl:8.10.1 -- \
     curl -fsS http://shopmate-ai:8080/api/chat \
       -H 'Content-Type: application/json' \
       -d '{"message":"Find a waterproof hiking jacket under $200 and explain the return policy."}'
   ```

7. Confirm Splunk evidence.

   Use these filters:

   ```text
   service.name=shopmate-ai
   deployment.environment=student-01
   k8s.cluster.name=clus-ltrobs-2001-student-01
   ```

   Confirm:

   - app trace is visible
   - custom `shopmate.workflow` and `shopmate.agent.*` spans make the workflow readable
   - OpenAI-compatible assistant or NIM spans are visible
   - token metrics are visible
   - `deployment.environment=student-01` is present

8. Confirm GPU and NIM metrics.

   This requires the Module 3 collector update. The final collector config must keep OTLP app metrics in the unfiltered `metrics` pipeline, put GPU/NIM Prometheus scrape metrics in a separate filtered `metrics/gpu_nim` pipeline, and set `send_otlp_histograms: true` under `exporters.signalfx`.

   Use these filters separately:

   ```text
   deployment.environment=student-01 job=dcgm
   ```

   ```text
   deployment.environment=student-01 job=nim
   ```

   Confirm:

   - `DCGM_FI_DEV_GPU_UTIL` is visible
   - GPU memory metrics are visible
   - NIM latency or request metrics are visible
   - NIM token metrics are visible where exposed by the lab NIM build

## Student-Ready Definition

Students can start when:

1. The MkDocs site is reachable.
2. Student namespaces and kubeconfigs are verified.
3. The preloaded `splunk-observability-token` Secret exists in each namespace.
4. One test student can deploy the collector from the documented values file.
5. One test student can apply app observability settings from the documented Module 2 variables.
6. One test request creates a Splunk trace with `service.name=shopmate-ai` and `deployment.environment=<student id>`.
7. One test request shows custom `shopmate.workflow` and `shopmate.agent.*` spans plus OpenAI/NIM spans.
8. One test student can see GPU and NIM metrics after the collector scrape change.
9. The instructor has a reset path for collector and app deployments.

## Reset Commands

Use only in the affected student namespace.

```bash
helm uninstall student-collector -n "$STUDENT_NAMESPACE"
kubectl delete -n "$STUDENT_NAMESPACE" deploy/student-collector svc/student-collector configmap/student-collector-otel-collector --ignore-not-found
kubectl rollout restart deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
kubectl rollout status deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
```

## Docs QA Commands

Run these before publishing or handing the URL to students:

```bash
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/student_mkdocs_walkthrough.py --base-url http://127.0.0.1:8001/
ruby -e 'require "yaml"; YAML.load_file("workshop/lab-files/collector-observability-snippet.yaml"); puts "YAML ok"'
ruby -e 'require "yaml"; YAML.load_file("workshop/lab-files/student-collector-values-gpu-nim-reference.yaml"); puts "YAML ok"'
```
