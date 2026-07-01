---
title: Configure Environment
linkTitle: 02. Configure Environment
weight: 2
time: 15 minutes
description: In this step, you'll create an `.env` file with your Splunk Observability Cloud credentials and workshop settings. 
---

{{% notice title="Validation Checklist" style="green" icon="running" %}}
Your environment should already have values for `SPLUNK_ACCESS_TOKEN`, `SPLUNK_REALM`, and `SPLUNK_RUM_ACCESS_TOKEN`

Run these commands from the project root after editing `.env`.

{{< tabs >}}
{{% tab title="Script" %}}

```bash
grep -E '^SPLUNK_(REALM|ACCESS_TOKEN|RUM_ACCESS_TOKEN)=' .env | cut -d= -f1
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
SPLUNK_REALM
SPLUNK_ACCESS_TOKEN
SPLUNK_RUM_ACCESS_TOKEN
```

{{% /tab %}}
{{< /tabs >}}

**If they do not exist export them as follows**


```bash
cp .env.example .env
```

Open `.env` in your editor and replace the placeholder values:

```bash
# Splunk Observability Cloud
SPLUNK_REALM=<splunk-realm>
SPLUNK_ACCESS_TOKEN=<your-org-access-token>

# RUM browser agent
SPLUNK_RUM_ACCESS_TOKEN=<your-rum-access-token>
SPLUNK_RUM_APP_NAME=cosmic-observatory-shop
SPLUNK_DEPLOYMENT_ENV=workshop-context-prop

# Kubernetes
K3D_CLUSTER_NAME=cosmic-shop
CLUSTER_NAME=cosmic-shop-cluster
REGISTRY=localhost:5111
TAG=latest

# Workshop: propagation
RABBITMQ_PROPAGATE_CONTEXT=false
```

{{% /notice %}}

## How instrumentation uses these values

### Splunk RUM (frontend)

Each **Place order** action starts a RUM custom workflow (`purchase.checkout`) -  distinct from the **Purchase** button click that only opens the confirmation dialog.

When you run `make build`, the values from `.env` are baked into the static JavaScript bundle. **Session replay** is enabled via `@splunk/otel-web-session-recorder` (requires a RUM token with session replay permissions in Splunk O11y).

```javascript
SplunkRum.init({
  realm: '<SPLUNK_REALM>',
  rumAccessToken: '<SPLUNK_RUM_ACCESS_TOKEN>',
  applicationName: 'cosmic-observatory-shop',
  deploymentEnvironment: 'workshop-context-prop',
});
```

### Splunk APM (backend services)

Node.js services use `@splunk/otel` and read configuration from **runtime environment variables** set in Kubernetes deployments:

- `OTEL_EXPORTER_OTLP_ENDPOINT=http://$(NODE_IP):4318` - sends spans to the Splunk OTel Collector DaemonSet
- `OTEL_SERVICE_NAME` - service name in APM (e.g. `order-api`, `payment-gateway`)
- `OTEL_RESOURCE_ATTRIBUTES` - includes `deployment.environment`, `k8s.cluster.name`, and `k8s.pod.name` for Infrastructure ↔ APM correlation
- `SPLUNK_ACCESS_TOKEN` and `SPLUNK_REALM` - Splunk distro credentials

---
