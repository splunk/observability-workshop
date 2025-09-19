---
title: Deploy the OpenTelemetry Collector
linkTitle: 4. Deploy the OpenTelemetry collector
weight: 4
time: 10 minutes
---

Now that our OpenShift cluster is up and running, let's deploy the
OpenTelemetry Collector, which gathers metrics, logs, and traces 
from the infrastructure and applications running in the cluster, and 
sends the resulting data to Splunk. 

## Deploy the OpenTelemetry Collector

First, we'll create a new project for the collector and switch to that project:

```bash
oc new-project otel 
oc project otel
```

Ensure Helm is installed: 

``` bash 
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

Add the Splunk OpenTelemetry Collector for Kubernetes' Helm chart repository:

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
````

Ensure the repository is up-to-date:

```bash
helm repo update
````

Define a file named `otel-collector-values.yaml` with the following content: 

``` yaml
distribution: openshift
readinessProbe:
  initialDelaySeconds: 180
livenessProbe:
  initialDelaySeconds: 180
operator:
  enabled: false
operatorcrds:
  installed: false
gateway:
  enabled: false
splunkObservability:
  profilingEnabled: true
clusterReceiver:
  resources:
    limits:
      cpu: 200m
      memory: 2000Mi
agent:
  discovery:
    enabled: true
  resources:
    limits:
      cpu: 200m
      memory: 2000Mi
  config:
    exporters:
      signalfx:
        send_otlp_histograms: true
    receivers:
      kubeletstats:
        insecure_skip_verify: true
```

Then install the collector using the following command:

> Note: update the command below before running it
> to include the desired cluster name, environment, access token, etc.
> for the target Splunk environment.

```bash
helm install splunk-otel-collector \
  --set="clusterName=<cluster name>" \
  --set="environment=<environment name>" \
  --set="splunkObservability.accessToken=***" \
  --set="splunkObservability.realm=<realm e.g. us0, us1, eu0>" \
  --set="splunkPlatform.endpoint=https://<hostname>:443/services/collector/event" \
  --set="splunkPlatform.token=***" \
  --set="splunkPlatform.index=<index name>" \
  -f ./otel-collector-values.yaml \
  -n otel \
  splunk-otel-collector-chart/splunk-otel-collector
```

Run the following command to confirm that all of the collector pods are running: 

````
oc get pods

NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-58rwm                             1/1     Running   0          6m40s
splunk-otel-collector-agent-8dndr                             1/1     Running   0          6m40s
splunk-otel-collector-k8s-cluster-receiver-7b7f5cdc5b-rhxsj   1/1     Running   0          6m40s
````

Confirm that you can see the cluster in Splunk Observability Cloud by navigating to 
Infrastructure Monitoring -> Kubernetes -> Kubernetes Pods and then filtering on your 
cluster name: 

![Kubernetes Pods](../images/KubernetesPods.png)