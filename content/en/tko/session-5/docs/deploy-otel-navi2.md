---
title: Deploying the OpenTelemetry Collector in Kubernetes using a NameSpace
linkTitle: Prep UI & Deploy the OTel Collector 
weight: 21
---
## 1. Switching to the new Kubernetes Navigator 2.0 UI

As we are in the process of switched to the new generation of the Kubernetes Navigator please check if you are already on the new Kubernetes navigator.

When you select `Infrastructure` from the main menu on the left, followed by selecting `Kubernetes`, you should see a number of services panes for Kubernetes, similar like the ones below:

![k8s-navi-v-2](../images/k8s-nav2.png)

If you taken straight to the Kubernetes Navigator v1 Map view after selecting `Kubernetes`, you need to set the feature flag for the new Navigator yourself.

To do this, please change the Url in your browser to match the following: [https://app.[REALM].signalfx.com/#/superpowers](https://app.[REALM].signalfx.com/#/superpowers)

Where [REALM] needs to match the Realm we are using for this workshop.

First make sure you have the Precognition flag set like the example below, this is one of the first options to set:

![Set-Precognition](../images/Precognition.png)

Then scroll down or search the list of features and find the option: `newKubernetesNavigators` and set it like below if it is not set already.

![Set-New-NAvi](../images/set_new_k8s_navi.png)

Once its set, you can refresh you page, and reselect Kubernetes from the infrastructure navigator menu.

{{% alert title="Note" color="info" %}}
Be aware that your login may still be configured internally to use the original navigator on the underlying services.  You will se that even with the new panes you still see parts of the old Navigator.

You can fix this by pressing the ![new-k8-button](../images/new-k8s-button.png) button that will popup on the top right side of you screen if your still configured to use the old services.

You may need to do this once per service type (Cluster/Nodes/Workloads).
{{% /alert %}}

## 2. Connect to EC2 instance

You will be able to connect to the workshop instance by using SSH from your Mac, Linux or Windows device.

To use SSH, open a terminal on your system and type `ssh ubuntu@x.x.x.x` (replacing x.x.x.x with the IP address assigned to you).

{{% alert title="Note" color="info" %}}
Your workshop instance has been pre-configured with the correct `ACCESS_TOKEN` and `REALM` for this workshop. There is no need for you to configure these.
{{% /alert %}}

## 3. Namespaces in Kubernetes

Most of our customers will make use of some kind of private or public cloud service to run Kubernetes. They often choose to have only a few large Kubernetes clusters as it is easier to manage centrally.

Namespaces are a way to organize these large Kubernetes clusters into virtual sub-clusters. This can be helpful when different teams or projects share a Kubernetes cluster as this will give them the easy ability to just see and work with their own stuff.

Any number of namespaces are supported within a cluster, each logically separated from others but with the ability to communicate with each other. Components are only "visible" when selecting a namespace or when adding the `--all-namespaces` flag to `kubectl` instead of allowing you to view just the components relevant to your project by selecting your namespace.

Most customers will want to install the Splunk OpenTelemetry Collector in a separate namespace.  This workshop will follow that practice.

## 4. Install Splunk OTel using Helm

Install the OpenTelemetry Collector using the Splunk Helm chart. First, add the Splunk Helm chart repository and update.

{{< tabpane >}}
{{< tab header="Helm Repo Add" lang="text" >}}
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
{{< /tab >}}
{{< tab header="Helm Repo Add Output" lang="text" >}}
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
{{< /tab >}}
{{< /tabpane >}}

Install the OpenTelemetry Collector Helm chart into the `splunk` namespace with the following commands, do **NOT** edit this:

{{< tabpane >}}
{{< tab header="Helm Install" lang="text" >}}
helm install splunk-otel-collector \
--version "0.68.0" \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
splunk-otel-collector-chart/splunk-otel-collector \
--namespace splunk \
--create-namespace \
-f ~/splunk-defaults.yaml

{{< /tab >}}
{{< tab header="Helm Install Single Line" lang="bash" >}}
helm install splunk-otel-collector --set="splunkObservability.realm=$REALM" --set="splunkObservability.accessToken=$ACCESS_TOKEN" --set="clusterName=$(hostname)-k3s-cluster" --set="splunkObservability.logsEnabled=true" --set="clusterReceiver.eventsEnabled=true" --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" splunk-otel-collector-chart/splunk-otel-collector --namespace splunk --create-namespace
{{< /tab >}}
{{< /tabpane >}}

## 5. Verify Deployment

You can monitor the progress of the deployment by running `kubectl get pods` and adding `-n splunk` to the command to see the pods in the `splunk` NameSpace which should typically report that the new pods are up and running after about 30 seconds.

Ensure the status is reported as Running before continuing.

{{< tabpane >}}
{{< tab header="kubectl Get Pods" lang="bash" >}}
kubectl get pods -n splunk
{{< /tab >}}
{{< tab header="kubectl Get Pods Output" lang="text" >}}
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-2sk6k                             0/1     Running   0          10s
splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7   0/1     Running   0          10s
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="Note" color="info" %}}

If you are using the Kubernetes Integration setup from the Data Management page from the O11y UI , you find that the guide will use
`--generate-name splunk-otel-collector-chart/splunk-otel-collector` instead of just `splunk-otel-collector-chart/splunk-otel-collector` as we do in the above example.

This will generate an unique name/label for the collector install and Pods by adding a unique number at the end of the object name, allowing you to install multiple collectors in your Kubernetes environment with different configurations.

Just make sure you use the correct label that is generated by the helm chart if you wish to use the `helm` and `kubectl` commands from this workshop on an install done with the `--generate-name` option.
{{% /alert %}}

Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit). Or use the installed `k9s` terminal UI.

{{< tabpane >}}
{{< tab header="Kubectl Logs" lang="bash" >}}
kubectl logs -l app=splunk-otel-collector -f --container otel-collector -n splunk
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="Deleting a failed installation" color="warning" %}}
If you make an error installing the Splunk OpenTelemetry Collector you can start over by deleting the installation using:

``` bash
helm delete splunk-otel-collector -n splunk
```

{{% /alert %}}
