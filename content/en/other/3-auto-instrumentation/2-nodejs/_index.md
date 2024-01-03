---
title: NodeJS Workshop
weight: 2
description: A workshop using Zero Configuration Auto-Instrumentation for NodeJS.
hidden: true
---

The goal is to walk through the basic steps to configure the following components of the **Splunk Observability Cloud** platform:

* Splunk Infrastructure Monitoring (IM)
* Splunk Zero Configuration Auto Instrumentation for NodeJS (APM)
  * AlwaysOn Profiling

We will deploy the OpenTelemetry Astronomy Shop application in Kubernetes, which contains a NodeJS service. Once the application is up and running, we will instantly start seeing metrics and traces via the **Zero Configuration Auto Instrumentation** for NodeJS that will be used by the **Splunk APM** product.

{{% notice title="Prerequisites" style="primary" icon="info" %}}

* Outbound SSH access to port `2222`.
* Outbound HTTP access to port `8083`.
* Familiarity with the `bash` shell and `vi/vim` editor.

{{% /notice %}}

``` bash
cd ~/workshop/apm
kubectl apply -n otel-demo -f otel-demo.yaml
kubectl port-forward svc/opentelemetry-demo-frontend 8083:8080 -n otel-demo --address='0.0.0.0'
```

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
helm install splunk-otel-collector \
--set="operator.enabled=true", \
--set="certmanager.enabled=true", \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.logsEnabled=false" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

``` bash
kubectl patch deployment opentelemetry-demo-frontend -n otel-demo -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-nodejs":"default/splunk-otel-collector"}}}} }'
```

```
kubectl patch deployment opentelemetry-demo-paymentservice -n otel-demo -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-nodejs":"default/splunk-otel-collector"}}}} }'
```
