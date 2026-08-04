---
title: Configure Environment
linkTitle: 02. Configure Environment
weight: 2
time: 5 minutes

---
In this step, you'll create an `.env` file with your Splunk Observability Cloud credentials and workshop settings. 

## Validation Checklist
Your environment should already have values for `SPLUNK_ACCESS_TOKEN`, `SPLUNK_REALM`, and `SPLUNK_RUM_ACCESS_TOKEN`

Run `env` command from the project root to verify .

{{< tabs >}}
{{% tab title="Script" %}}

```bash
env
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
SPLUNK_REALM=<splunk-realm-value>
SPLUNK_ACCESS_TOKEN=<org-access-token-value>
SPLUNK_RUM_ACCESS_TOKEN=<rum-access-token-value>
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="[Optional] Exercise" style="green" icon="running" %}}
**If these values do not exist in your instance you can configure them as follows** - From the project root [~/workshop/context-propagation]:

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

{{% notice title="Note" style="info" %}}
Your instructor will provide you with all the required login credentials and environment details
{{% /notice %}}
