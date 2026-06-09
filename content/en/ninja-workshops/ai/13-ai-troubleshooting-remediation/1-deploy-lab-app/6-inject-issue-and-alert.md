---
title: 6. Inject the Example Issue and Create an Alert
weight: 6
---

Now create a controlled incident. Use the APM issue path for the primary workshop because it produces a clear service-level root cause and remediation path. Use the Kubernetes issue path as an advanced variant.

{{% notice title="Exercise" style="green" icon="running" %}}

## APM Issue Path

* Inject the latency and error issue:

```bash
cd workshop/ai-troubleshooting-remediation
./scripts/inject-issue.sh latency-errors
```

For MicroK8s, use:

```bash
KUBECTL_CMD="microk8s kubectl" ./scripts/inject-issue.sh latency-errors
```

* Wait three to five minutes for traces and service metrics to show the new behavior.
* In **APM**, open `checkout-service` or `inventory-service`.
* Confirm that latency and error rate increased after the issue injection time.
* Create or clone a detector using standard APM service metrics. Use one of these alert conditions:
  * Service error rate is above a low lab threshold for several minutes.
  * Service latency is above a low lab threshold for several minutes.
* Route the detector to a workshop notification target or keep the alert visible in **Active Alerts**.
* When the alert fires, copy the alert URL into your incident brief.

## Kubernetes Issue Path

Use this variant when you want a Kubernetes Infrastructure Monitoring alert.

```bash
./scripts/inject-issue.sh crashloop
```

For MicroK8s, use:

```bash
KUBECTL_CMD="microk8s kubectl" ./scripts/inject-issue.sh crashloop
```

* Confirm that `inventory-service` restarts:

```bash
kubectl -n ai-remediation get pods -l app=inventory-service
kubectl -n ai-remediation describe deploy inventory-service
```

* Create or clone a detector using standard Kubernetes workload or pod metrics, such as pod restarts, unavailable replicas, or workload readiness.
* When the alert fires, copy the alert URL into your incident brief.

{{< tabs >}}
{{% tab title="Question" %}}
**Which issue path should most students use first?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Use `latency-errors` first. It creates an APM service alert with traces, logs, and a clear downstream dependency issue for the AI troubleshooting agent to analyze.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Reset the Lab" style="info" %}}
To remediate the injected issue manually, run:

```bash
./scripts/remediate.sh
```

For MicroK8s, use:

```bash
KUBECTL_CMD="microk8s kubectl" ./scripts/remediate.sh
```

Do not run remediation yet if you still need the alert to stay active for the next chapter.
{{% /notice %}}
