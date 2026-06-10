# Appendix: Troubleshooting

## Fast Triage Checklist

Start with these commands in your namespace:

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

## Collector Issues

!!! failure "Collector pod is CrashLoopBackOff"
    Run `kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --previous`. Common causes are invalid YAML, missing token Secret, unsupported collector component names, or bad environment variable substitution.

    Reset:

    ```bash
    helm uninstall student-collector -n "$STUDENT_NAMESPACE"
    kubectl delete deploy/student-collector svc/student-collector configmap/student-collector-otel-collector -n "$STUDENT_NAMESPACE" --ignore-not-found
    ```

    Then recreate `student-collector-values.yaml` from the Module 1 baseline snippet and reinstall with Helm.

!!! failure "Helm says `failed to parse student-collector-values.yaml`"
    Inspect the start of the file:

    ```bash
    head -n 5 student-collector-values.yaml
    ```

    The first line should be:

    ```text
    fullnameOverride: student-collector
    ```

    If the file starts with `:` or `cat > student-collector-values.yaml`, you saved the shell command into the file instead of running it. Delete `student-collector-values.yaml`, then rerun the full Module 1 collector creation command in your terminal.

!!! failure "Collector pod is CreateContainerConfigError"
    Kubernetes could not build the collector container configuration. The most common cause is a missing preloaded Secret, invalid Secret contents, or a missing ConfigMap.

    Inspect the pod event:

    ```bash
    kubectl describe pod -n "$STUDENT_NAMESPACE" -l app=splunk-otel-collector
    ```

    Confirm the preloaded token Secret exists:

    ```bash
    kubectl get secret "$SPLUNK_ACCESS_TOKEN_SECRET" -n "$STUDENT_NAMESPACE"
    ```

    If the Secret exists but the pod still cannot start, ask the instructor to validate the preloaded Secret. Do not inspect or print Secret data yourself.

!!! failure "Collector runs but exports nothing"
    Confirm the app points to `http://student-collector:4318`, the OTLP receiver is enabled, and the Splunk exporter has the right realm and token.

!!! failure "AI overview is empty but ShopMate traces exist"
    Check two collector settings:

    - the collector must preserve OTLP histogram metrics with `send_otlp_histograms: true`
    - the collector must not filter OTLP app metrics through the GPU/NIM allowlist

    The app metrics pipeline must stay unfiltered, and only the separate `metrics/gpu_nim` pipeline should use `filter/gpu_nim_allowlist`.

    Inspect the rendered collector config:

    ```bash
    kubectl get configmap student-collector-otel-collector -n "$STUDENT_NAMESPACE" \
      -o jsonpath='{.data.relay}' \
      | grep -n "send_otlp_histograms\\|metrics/gpu_nim\\|filter/gpu_nim_allowlist\\|receivers: \\[otlp\\]"
    ```

    Correct shape:

    ```yaml
    exporters:
      signalfx:
        send_otlp_histograms: true
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, resource/environment, batch]
    metrics/gpu_nim:
      receivers: [prometheus/gpu_nim]
      processors: [memory_limiter, resource/environment, filter/gpu_nim_allowlist, batch]
    ```

!!! failure "Authentication errors to Splunk"
    Confirm the Kubernetes Secret exists in your namespace and was mounted or referenced by the collector values file.

!!! tip "Collector references"
    Use Splunk's collector troubleshooting guide for receiver, processor, exporter, and credential failures: [Troubleshoot the Splunk OpenTelemetry Collector](https://help.splunk.com/en?resourceId=gdi_opentelemetry_splunk-collector-troubleshooting). Use OpenTelemetry's guide for internal telemetry and deeper collector debugging: [OpenTelemetry Collector troubleshooting](https://opentelemetry.io/docs/collector/troubleshooting/).

## App Instrumentation Issues

!!! failure "No ShopMate service appears in Splunk"
    Confirm `OTEL_SERVICE_NAME=shopmate-ai` or the lab-provided service name, app logs do not show exporter errors, and the collector received OTLP traffic.

    Useful commands:

    ```bash
    kubectl get deploy,svc,pod -n "$STUDENT_NAMESPACE" -l app=shopmate-ai
    kubectl logs deploy/shopmate-ai -n "$STUDENT_NAMESPACE" --tail=100
    kubectl rollout restart deploy/shopmate-ai -n "$STUDENT_NAMESPACE"
    ```

!!! failure "Agent flow is flat or incomplete"
    Confirm the app emits the `shopmate.workflow` span and child `shopmate.agent.*` spans, then look inside those spans for OpenAI Agents SDK and NIM LLM activity. The custom spans explain the app workflow; zero-code instrumentation provides the SDK, tool, model, token, and GenAI metric details.

!!! failure "Prompt content is missing"
    Confirm safe capture is enabled with `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY` and the instrumentation library supports content capture in the selected mode.

!!! tip "AI Agent Monitoring references"
    Splunk's AI Agent Monitoring setup explains how to get traces and metrics into the Agents view: [Set up AI Agent Monitoring](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring). Splunk's Python GenAI configuration explains `OTEL_INSTRUMENTATION_GENAI_EMITTERS`, prompt capture, evaluations, and metric temporality: [Configure the Python agent for AI applications](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/configure-ai-agent-monitoring/configure-the-python-agent-for-ai-applications-0.1.14-and-higher).

## GPU and NIM Issues

!!! failure "DCGM metrics are missing"
    Confirm the DCGM endpoint, port, namespace DNS, and NetworkPolicy. Test with a temporary curl pod from your namespace.

!!! failure "NIM metrics are missing"
    Confirm the NIM metrics path is `/v1/metrics`, the service name is correct, and the collector scrape job uses the right port.

!!! failure "Dashboards are empty after scraping"
    Wait 3 to 5 minutes with a 60-second scrape interval, then confirm metric names and dimensions match the dashboard filters.

    Useful commands:

    ```bash
    kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=100
    kubectl get configmap student-collector-otel-collector -n "$STUDENT_NAMESPACE" -o yaml
    kubectl delete pod scrape-test nim-test -n "$STUDENT_NAMESPACE" --ignore-not-found
    ```

## Correlation Issues

!!! failure "App traces do not correlate with Kubernetes dashboards"
    Use `k8s.namespace.name`, pod name, and `service.name`. Kubernetes metrics come from the shared platform telemetry path, not your student collector.

!!! failure "GPU metrics appear duplicated"
    This is expected in workshop-compatible mode because each student collector scrapes shared endpoints. Filter by `deployment.environment`.

## Tokenomics Issues

!!! failure "Environment grouping fails"
    Confirm `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=<your student id>` is attached to the app deployment before export.

!!! failure "Token totals look too low"
    Confirm every NIM call records prompt and completion tokens, and check whether retries or tool calls are represented as separate spans.

!!! failure "Agent loop spend is not explainable"
    The zero-code app does not emit custom loop attributes. Look for repeated OpenAI Agents SDK activity, repeated NIM-backed LLM calls, high token usage, and long latency in the trace.

!!! failure "One student dominates class metrics"
    Confirm this is not caused by missing filters, duplicated traffic generation, or a collector using the wrong `deployment.environment`.

## Important Environment Variables

| Variable | Correct lab value or pattern | If wrong, you see |
| --- | --- | --- |
| `OTEL_SERVICE_NAME` | `shopmate-ai` or the lab-provided ShopMate service name | App appears under an unexpected service name |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://student-collector:4318` | App cannot send telemetry or collector receives nothing |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | Protocol mismatch or exporter errors |
| `OTEL_RESOURCE_ATTRIBUTES` | `deployment.environment=<your student id>` | Splunk data appears but cannot be filtered by environment |
| `OTEL_INSTRUMENTATION_GENAI_EMITTERS` | `span_metric` | Missing GenAI spans or token metrics |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | `SPAN_ONLY` | Prompt/response content missing from spans |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | `delta` | Counter-style metrics may not behave as expected |
| `SPLUNK_REALM` | instructor-provided realm | Collector exports to the wrong endpoint |
| `SPLUNK_ACCESS_TOKEN_SECRET` | `splunk-observability-token`, the preloaded Kubernetes Secret name | Collector cannot authenticate to Splunk |
