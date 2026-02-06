---
title: Review AI POD Dashboards
linkTitle: 6. Review AI POD Dashboards
weight: 6
time: 10 minutes
---

## Update the OpenTelemetry Collector Config

We can apply the collector configuration changes by running the following Helm command:

``` bash
helm upgrade splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./otel-collector-values.yaml \
  -n $USER_NAME \
  splunk-otel-collector-chart/splunk-otel-collector
```

## Review the AI POD Overview Dashboard Tab

Navigate to `Dashboards` in Splunk Observability Cloud, then search for the
`Cisco AI PODs Dashboard`, which is included in the `Built-in dashboard groups`.
Ensure the dashboard is filtered on your OpenShift cluster name.
The charts should be populated as in the following example:

![Kubernetes Pods](../../images/Cisco-AI-Pod-dashboard.png)

## Review the Pure Storage Dashboard Tab

Navigate to the `PURE STORAGE` tab and ensure the dashboard is filtered
on your OpenShift cluster name. The charts should be populated as in the
following example:

![Pure Storage Dashboard](../../images/PureStorage.png)

## Review the Weaviate Infrastructure Navigator

Since Weaviate isn't included by default with an AI POD, it's 
not included on the out-of-the-box AI POD dashboard. Instead, 
we can view Weaviate performance data using one of the infrastructure 
navigators. 

In Splunk Observability Cloud, navigate to `Infrastructure` -> `AI Frameworks` -> `Weaviate`.
Filter on the `k8s.cluster.name` of interest, and ensure the navigator is populated as in the
following example:

![Kubernetes Pods](../../images/WeaviateNavigator.png)

