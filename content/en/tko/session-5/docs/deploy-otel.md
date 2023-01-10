---
title: Deploying the OpenTelemetry Collector in Kubernetes using a NameSpace
linkTitle: Deploy the OTel Collector
weight: 1
---

## 1. Namespaces in Kubernetes

Namespaces are a way to organize kubernetes clusters into virtual sub-clusters. They can be helpful when different teams or projects share a Kubernetes cluster.

Any number of namespaces are supported within a cluster, each logically separated from others but with the ability to communicate with each other.

Most customers will want to install the Splunk OpenTelemetry Collector in a NameSpace.  This workshop will follow that practice.

## 2. Obtain Access Token

You will need to obtain your Access Token from the Splunk UI. You can find the workshop Access Token by clicking **>>** bottom left and then selecting **Settings → Access Tokens**.

Expand the workshop token that your host has instructed you to use e.g. **O11y-Workshop-ACCESS**, then click on **Show Token** to expose your token. Click the {{% labelbutton color="ui-button-grey" %}}Copy{{% /labelbutton %}} button to copy to clipboard. Please do not use the **Default** token!

You will also need to obtain the name of the Realm for your Splunk account.  At the top of the side menu, click on your name. This will direct you to the **Account Settings** Page. Click the **Organizations**-tab. The Realm can be found at the top of the displayed information in the tab.

## 3. Installation using Helm using 'splunk' as a Namespace

Create the `ACCESS_TOKEN` and `REALM` environment variables to use in the proceeding Helm install command.

{{< tabpane >}}
{{< tab header="Export Variables" lang="bash" >}}
export ACCESS_TOKEN=<replace_with_Workshop_ACCESS_TOKEN>
export REALM=<replace_with_REALM>
{{< /tab >}}
{{< /tabpane >}}

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
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="clusterReceiver.eventsEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
splunk-otel-collector-chart/splunk-otel-collector \
--namespace splunk \
--create-namespace \
-f \home\ubuntu\splunk-defaults.yaml

{{< /tab >}}
{{< tab header="Helm Install Single Line" lang="bash" >}}
helm install splunk-otel-collector --set="splunkObservability.realm=$REALM" --set="splunkObservability.accessToken=$ACCESS_TOKEN" --set="clusterName=$(hostname)-k3s-cluster" --set="splunkObservability.logsEnabled=true" --set="clusterReceiver.eventsEnabled=true" --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" splunk-otel-collector-chart/splunk-otel-collector --namespace splunk --create-namespace
{{< /tab >}}
{{< /tabpane >}}

## 3. Verify Deployment

You can monitor the progress of the deployment by running `kubectl get pods` and adding `-n splunk` to the command to see the pods in the `splunk` NameSpace which should typically report that the new pods are up and running after about 30 seconds.

Ensure the status is reported as Running before continuing.

{{< tabpane >}}
{{< tab header="Kubectl Get Pods" lang="bash" >}}
kubectl get pods -n splunk
{{< /tab >}}
{{< tab header="Kubectl Get Pods Output" lang="text" >}}
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-2sk6k                             0/1     Running   0          10s
splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7   0/1     Running   0          10s
{{< /tab >}}
{{< /tabpane >}}

---

**Note**
If you are using the Kubernetes Integration setup from the Data Management page from the O11y UI , you find that the guide will use
`--generate-name splunk-otel-collector-chart/splunk-otel-collector` instead of just `splunk-otel-collector-chart/splunk-otel-collector` as we do in the above example.

This will generate an unique name/label for the collector install and Pods by adding a unique number at the end of the object name, allowing you to install multiple collectors in your Kubernetes environment with different configurations.

Just make sure you use the correct label that is generated by the helm chart if you wish to use the `helm` and `kubectl` commands from this workshop on an install done with the `--generate-name` option.  

---

Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit). Or use the installed `k9s` terminal UI.

{{< tabpane >}}
{{< tab header="Kubectl Logs" lang="bash" >}}
kubectl logs -l app=splunk-otel-collector -f --container otel-collector -n splunk
{{< /tab >}}
{{< /tabpane >}}

{{% alert title="Deleting a failed installation" color="danger" %}}
If you make an error installing the Splunk OpenTelemetry Collector you can start over by deleting the installation using:

``` bash
helm delete splunk-otel-collector -n splunk
```

{{% /alert %}}
