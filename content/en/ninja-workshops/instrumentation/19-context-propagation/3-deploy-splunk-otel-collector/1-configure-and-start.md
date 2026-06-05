---
title: 1. Configure and Start the Stack
weight: 1
---

## Verify or Add Your Splunk Credentials

{{% exercise title="Configure and Start" %}}

``` bash
echo $ACCESS_TOKEN; echo $REALM; echo $INSTANCE
```

if no values are set then Create or edit `.env` in the repository root:

**Note:** Obtain your access token from Splunk Observability Cloud: **Settings → Access Tokens** (Ingest token with APM permissions).. You will need to paste them into configs.

```bash
cp .env.example .env
```

```bash
SPLUNK_ACCESS_TOKEN=<INGEST_TOKEN>
SPLUNK_REALM=<YOUR-REALM>
WORKSHOP_ENV=trace-propagation-<YOUR-INITIALS>
```

### Deploy the collector

This script:

1. Creates the `splunk-credentials` Kubernetes Secret from `.env`
2. Applies `k8s/splunk-otel-collector/` (gateway Deployment, agent DaemonSet, RBAC, ConfigMaps)
3. Waits for the gateway and infrastructure agent to become ready
4. Validates collector health on `http://localhost:13133/`

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
```bash
cd ~/workshop/context-propagation/scripts
./2-deploy-collector.sh
```

{{% /tab %}}
{{% tab title="Example Output (abbreviated)" %}}

``` text
Creating Splunk credentials secret...
Deploying Splunk OpenTelemetry Collector...
Waiting for splunk-otel-collector gateway...
Waiting for splunk-otel-collector-agent (infrastructure metrics)...
Splunk OTel Collector image: quay.io/signalfx/splunk-otel-collector:0.108.0
Validating collector health...
{"status":"Server available","upSince":"...","uptime":"..."}
Step 2 complete — Splunk OTel Collector is running.
Infrastructure metrics: host + kubelet (DaemonSet) + k8s_cluster (gateway) → Splunk IMM
Splunk IMM cluster:     trace-workshop ...

Validating collector health...
```

{{% /tab %}}
{{< /tabs >}}

The workshop deploys two collector workloads:

| Workload | Role |
| -------- | ---- |
| `deployment/splunk-otel-collector` | OTLP gateway + **k8s_cluster** receiver (cluster infrastructure metrics) |
| `daemonset/splunk-otel-collector-agent` | **hostmetrics** + **kubeletstats** (node, pod, container metrics) |

- **Image:** `quay.io/signalfx/splunk-otel-collector:0.108.0`
- **Gateway config:** `k8s/splunk-otel-collector/workshop-config.yaml`
- **Agent config:** `k8s/splunk-otel-collector/agent-config.yaml`

### Confirm collector health

```bash
curl -s http://localhost:13133/
```

### Check collector logs

Confirm the collector starts without pipeline errors (no repeated `401`, `403`, or export failures).

```bash
kubectl logs deployment/splunk-otel-collector -n trace-workshop --tail 20
kubectl logs daemonset/splunk-otel-collector-agent -n trace-workshop --tail 20
```

{{%/ exercise %}}
