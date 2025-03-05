---
title: Installing the OpenTelemetry Collector
linkTitle: 2. Installing the Collector
weight: 2
---

## 1. Introduction

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}

If you have completed any other Observability workshops, please ensure you delete the collector running in Kubernetes before continuing. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 2. Confirm environment variables

To ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following command:

``` bash
env
```

In the output check the following environment variables are present and have values set:

```text
ACCESS_TOKEN
REALM
RUM_TOKEN
HEC_TOKEN
HEC_URL
```

For this workshop, **all** of the above are required. If any are missing, please contact your instructor.

## 3. Install the OpenTelemetry Collector

We can then go ahead and install the Collector. Some additional parameters are passed to the `helm install` command, they are:

* `--set="operator.enabled=true"` - Enabled the Splunk OpenTelemetry Collector Operator for Kubernetes.
* `--set="splunkObservability.profilingEnabled=true"` - Enables CPU/Memory profiling for supported languages.

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

``` bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="operatorcrds.install=true", \
--set="operator.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

Once the installation is completed, you can navigate to the **Kubernetes Navigator** to see the data from your host.

Click on **Add filters** select `k8s.cluster.name` and select the cluster of your workshop instance.
You can determine your instance name from the command prompt in your terminal session:

```bash
echo $INSTANCE
```

Once you see data flowing for your host, we are then ready to get started with the APM component.

![Kubernetes Navigator](../images/k8s-navigator.png)
