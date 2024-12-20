---
title: Install the OpenTelemetry Collector in K8s
linkTitle: 7. Install the OpenTelemetry Collector in K8s
weight: 7
time: 15 minutes
---

At this point in the workshop, we've successfully: 

* Deployed the Splunk distribution of the OpenTelemetry Collector on our Linux Host
* Configured it to send traces and metrics to Splunk Observability Cloud
* Deployed a .NET application and instrumented it with OpenTelemetry 
* Dockerized the .NET application and ensured traces are flowing to o11y cloud

In the next part of the workshop, we want to run the application in Kubernetes instead. 

To do this, we first want to deploy the Splunk distribution of the OpenTelemetry Collector 
to our Kubernetes cluster. 

## Uninstall the Host Collector 

Before moving forward, let’s remove the collector we installed earlier on the Linux host: 

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

## What is Helm? 

We'll use Helm to deploy the OpenTelemetry collector in our K8s cluster.  But what is Helm? 

Helm is a package manager for Kubernetes.

“It helps you define, install, and upgrade even the most complex Kubernetes application.”

Source:  https://helm.sh/ 

## Benefits of Helm

* Manage Complexity
  * deal with a single values.yaml file rather than dozens of manifest files
* Easy Updates
  * in-place upgrades
* Rollback support
  * Just use helm rollback to roll back to an older version of a release 

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
the `/home/splunk` directory with the following contents: 

``` yaml
splunkObservability:
  realm: us1
  accessToken: <your access token> 
clusterName: $INSTANCE-cluster
environment: otel-$INSTANCE
```

> Replace $INSTANCE in the code snippet above with your instance name, which you 
> can find by running `echo $INSTANCE`.  Do the same with the access token, which 
> you can find by running `echo $ACCESS_TOKEN`. 

Now we can use the following command to install the collector: 

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
helm install \
splunk-otel-collector \
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
splunk-otel-collector-agent-8xvk8                            1/1     Running   0          49s
splunk-otel-collector-k8s-cluster-receiver-d54857c89-tx7qr   1/1     Running   0          49s
```

{{% /tab %}}
{{< /tabs >}}

## Confirm your K8s Cluster is in O11y Cloud

In Splunk Observability Cloud, navigate to **Infrastructure** -> **Kubernetes** -> **Kubernetes Nodes**, 
and then Filter on your Cluster Name (which is `$INSTANCE-cluster`). 

TODO:  show screenshot 

![Kubernetes node](../images/k8snode.png)
