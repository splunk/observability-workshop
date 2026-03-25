---
title: Deploy the OpenTelemetry Collector
linkTitle: 3. Deploy the OpenTelemetry Collector
weight: 3
time: 10 minutes
---

## Install the Collector using Helm

Let’s use the command line rather than the in-product wizard to create our own
`helm` command to install the collector.

We first need to add the helm repo:

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
```

And ensure the repo is up-to-date:

``` bash
helm repo update
```

To configure the helm chart deployment, let's create a new file named `values.yaml` in
the `/home/splunk` directory:

``` bash
# swith to the /home/splunk dir
cd /home/splunk
# create a values.yaml file in vi
vi values.yaml
```
> Press ‘i’ to enter into insert mode in vi before pasting the text below.

Then paste the following contents:

``` yaml
agent:
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
```

> To save your changes in vi, press the `esc` key to enter command mode, then type `:wq!` followed by pressing the `enter/return` key.

Now we can use the following command to install the collector:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
  helm upgrade --install splunk-otel-collector --version {{< otel-version >}} \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=agentic-ai-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
  splunk-otel-collector-chart/splunk-otel-collector 
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME: splunk-otel-collector
LAST DEPLOYED: Fri Dec 20 01:01:43 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm us1.
```

{{% /tab %}}
{{< /tabs >}}

## Confirm the Collector is Running

We can confirm whether the collector is running with the following command:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-dkn88                            1/1     Running   0          53s
splunk-otel-collector-agent-ksmh4                            1/1     Running   0          53s
splunk-otel-collector-agent-lc2lf                            1/1     Running   0          53s
splunk-otel-collector-k8s-cluster-receiver-dbf64995b-xgm9b   1/1     Running   0          53s
```

{{% /tab %}}
{{< /tabs >}}

## Confirm your K8s Cluster is in O11y Cloud

In Splunk Observability Cloud, navigate to **Infrastructure** -> **Kubernetes** -> **Kubernetes Clusters**,
and then search for your cluster name (which is `$INSTANCE-cluster`):

![Kubernetes node](../images/k8snode.png)

