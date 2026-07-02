---
title: Configure Environment
linkTitle: 02. Configure Environment
weight: 2
time: 5 minutes
description: In this step, you'll create an `.env` file with your Splunk Observability Cloud credentials and workshop settings. 

---

{{% notice title="Validation Checklist" style="green" icon="running" %}}
Your environment should already have values for `SPLUNK_ACCESS_TOKEN`, `SPLUNK_REALM`, and `SPLUNK_RUM_ACCESS_TOKEN`

Run these commands from the project root to verify `.env`.

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

```

{{% /notice %}}

---
