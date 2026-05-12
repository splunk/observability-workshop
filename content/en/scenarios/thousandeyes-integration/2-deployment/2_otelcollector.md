---
title: OTel Collector
linkTitle: 2.2 OTel Collector
weight: 2
time: 15 minutes
description: Deploy the OTel Collector.
---

Next we will deploy the open telemetry collector

## Step 1: Deploy the Open Telemetry Collector

If your application is already instrumented and traces are visible in Splunk APM, you can skip to Step 2. Otherwise, the fastest learning path in Kubernetes is to use the Splunk OpenTelemetry Collector with the Operator enabled for zero-code instrumentation.

### Install the Splunk OpenTelemetry Collector with the Operator

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

helm repo update

helm install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --set splunkObservability.realm=$REALM \
  --set splunkObservability.accessToken=$ACCESS_TOKEN \
  --set clusterName=$CLUSTER_NAME \
  --set environment="thousandeyes-$INSTANCE" \
  --set operator.enabled=true \
  --set operatorcrds.install=true \
  --set agent.service.enabled=true
```

Your cluster name is:
```bash
export | grep CLUSTER_NAME
```

Check if your Cluster is in **Splunk Observability Cloud**:
* Go to **Infrastructure > Kubernetes Entities**
* You should see your cluster in the list
  * It may take several minutes for it to show up