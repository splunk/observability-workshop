---
title: 5. Verify Monitoring
weight: 5
---

Before creating the issue, verify both Kubernetes telemetry and APM service telemetry. If either signal is missing, the AI troubleshooting workflow will have less evidence to work with.

{{% notice title="Exercise" style="green" icon="running" %}}

* Confirm the Splunk OpenTelemetry Collector pods are running:

```bash
kubectl get pods | grep splunk-otel-collector
```

* Confirm the agent is receiving data without repeated export errors:

```bash
kubectl logs -l app=splunk-otel-collector --container otel-collector --tail=100
```

* In Splunk Observability Cloud, go to **Infrastructure** > **Kubernetes** > **Kubernetes Clusters**.
* Search for the cluster name:

```bash
echo "${CLUSTER_NAME:-ai-remediation-cluster}"
```

* Open **APM** and filter for:
  * Environment: `ai-remediation-workshop`
  * Services: `checkout-service`, `inventory-service`, and `remediation-loadgen`
* Open the service map and confirm the call path:

```text
remediation-loadgen -> checkout-service -> inventory-service
```

* Open **Log Observer** or related logs and search for:

```text
app.workshop=ai-troubleshooting-remediation
```

{{< tabs >}}
{{% tab title="Question" %}}
**Which two telemetry signals are required before continuing?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Kubernetes infrastructure telemetry for the cluster and APM telemetry for `checkout-service` and `inventory-service`.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

## Troubleshooting Missing Telemetry

| Symptom | Check |
|---------|-------|
| No Kubernetes cluster in Infrastructure | Confirm the collector Helm install used the correct `SPLUNK_REALM`, access token, and `CLUSTER_NAME`. |
| No APM services | Confirm app pods have `OTEL_EXPORTER_OTLP_ENDPOINT=http://$(NODE_IP):4317` and the load generator is running. |
| Services exist but environment is wrong | Check `OTEL_RESOURCE_ATTRIBUTES` in `k8s/app.yaml`. |
| Logs missing | Confirm `logsEngine: otel` is set in `k8s/collector-values.yaml` and pod logs are being collected. |
