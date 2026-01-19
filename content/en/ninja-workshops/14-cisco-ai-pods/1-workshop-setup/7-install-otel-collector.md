---
title: Install the OpenTelemetry Collector
linkTitle: 7. Install the OpenTelemetry Collector
weight: 7
time: 5 minutes
---

In this section, we'll install the OpenTelemetry collector with only the clusterReceiver enabled
(as the workshop participants will install their own agent in their namespace). 
We'll then take the ClusterRole created by this collector installation and bind it to 
each of the workshop participant namespaces. 

## Install the OpenTelemetry Collector 

First, we'll create a new project for the collector and switch to that project:

```bash
oc new-project admin-otel 
```

Add the Splunk OpenTelemetry Collector for Kubernetes' Helm chart repository:

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

Ensure the repository is up-to-date:

```bash
helm repo update
````

Review the file named `./admin-otel-collector/admin-otel-collector-values.yaml` as we'll be using it
to install the OpenTelemetry collector.

Set environment variables to configure the Splunk environment you'd like
the collector to send data to:

``` bash
export CLUSTER_NAME=rosa-test
export ENVIRONMENT_NAME=<which environment to send data to for Splunk Observability Cloud>
export SPLUNK_ACCESS_TOKEN=<your access token for Splunk Observability Cloud> 
export SPLUNK_REALM=<your realm for Splunk Observability Cloud i.e. us0, us1, eu0, etc.>
export SPLUNK_HEC_URL=<HEC endpoint to send logs to Splunk platform i.e. https://<hostname>:443/services/collector/event> 
export SPLUNK_HEC_TOKEN=<HEC token to send logs to Splunk platform> 
export SPLUNK_INDEX=<name of index to send logs to in Splunk platform>
```

Then install the collector using the following command:

```bash
helm install splunk-otel-collector \
  --set="clusterName=$CLUSTER_NAME" \
  --set="environment=$ENVIRONMENT_NAME" \
  --set="splunkObservability.accessToken=$SPLUNK_ACCESS_TOKEN" \
  --set="splunkObservability.realm=$SPLUNK_REALM" \
  --set="splunkPlatform.endpoint=$SPLUNK_HEC_URL" \
  --set="splunkPlatform.token=$SPLUNK_HEC_TOKEN" \
  --set="splunkPlatform.index=$SPLUNK_INDEX" \
  -f ./admin-otel-collector/admin-otel-collector-values.yaml \
  -n admin-otel \
  splunk-otel-collector-chart/splunk-otel-collector
```

Run the following command to confirm that all of the collector pods are running:

````
oc get pods -n admin-otel

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-k8s-cluster-receiver-7b7f5cdc5b-rhxsj   1/1     Running   0          6m40s
````

## Create Service Account for each Workshop Participant and Bind to Cluster Role

``` bash
for i in {1..20}; do
  ns="workshop-participant-$i"

  oc get ns "$ns" >/dev/null 2>&1 || continue
  oc -n "$ns" create sa splunk-otel-collector 2>/dev/null || true

  oc apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: splunk-otel-collector-${ns}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: splunk-otel-collector
subjects:
- kind: ServiceAccount
  name: splunk-otel-collector
  namespace: ${ns}
EOF
done
```

We also need to grant the SecurityContextConstraint (SCC) to each namespace ServiceAccount: 

``` bash
for i in {1..20}; do
  ns="workshop-participant-$i"
  oc get ns "$ns" >/dev/null 2>&1 || continue
  oc -n "$ns" adm policy add-scc-to-user splunk-otel-collector -z splunk-otel-collector
done
```