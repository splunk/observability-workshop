---
title: Configure Environment
linkTitle: 02. Configure Environment
weight: 2
time: 5 minutes

---
In this step, you'll ensure `env` variables are configured with your Splunk Observability Cloud credentials and workshop settings. 

## Validation Checklist
Your environment should already have values for `INSTANCE`, `CLUSTER`, `REALM`, `ACCESS_TOKEN` and `RUM_TOKEN`

Configure the additional required `env` values: 

```bash
export DEPLOYMENT_ENV="workshop-${INSTANCE}"
export RUM_APP_NAME="workshop-${INSTANCE}"
```

Run `env` command from the project root to verify.

{{< tabs >}}
{{% tab title="Script" %}}

```bash
env
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
INSTANCE=<your-instance>
CLUSTER_NAME=$INSTANCE-cluster
REALM=<splunk-realm>
ACCESS_TOKEN=<access-token>
RUM_TOKEN=<rum-token>
DEPLOYMENT_ENV=workshop-${INSTANCE}
RUM_APP_NAME=workshop-$INSTANCE
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="[Optional] Exercise" style="green" icon="running" %}}
**If these values do not exist in your instance you can configure them as follows**:

```bash
export REALM="us1"
export ACCESS_TOKEN="your-org-ingest-token"
export RUM_TOKEN="your-rum-access-token"
export DEPLOYMENT_ENV="workshop-${INSTANCE}"
export RUM_APP_NAME="workshop-${INSTANCE}"
export CLUSTER_NAME="workshop-cluster-${INSTANCE}"
```
{{% /notice %}}

{{% notice title="Note" style="info" %}}
Your instructor will provide you with all the required login credentials and environment details
{{% /notice %}}
