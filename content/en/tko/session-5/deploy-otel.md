---
title: Deploying the OpenTelemetry Collector in Kubernetes using a NameSpace
linkTitle: 1. Deploy the OTel Collector
weight: 1
---

## 1. New Kubernetes Navigator 2.0 UI

{{% notice title="Note" style="warning" icon="exclamation" %}}
As the new Kubernetes Navigator is still in Preview, some steps of this workshop might not work as expected. If you encounter any issues, please do the following:

- Switch back to the old Kubernetes Navigator by clicking on the big blue {{% button style="blue" %}}Switch to old navigator{{% /button %}} button in the top right corner of the Kubernetes Navigator.

- Let us know in the **#tko-2023-o11y-session-5 channel** in Slack.
{{% /notice %}}}

As we are in the process of switching to the new generation of the Kubernetes Navigator, please check if you are already on the new Kubernetes navigator.

When you select **Infrastructure** from the main menu on the left, followed by selecting **Kubernetes**, you should see two services panes for Kubernetes, similar like the ones below:

![k8s-navi-v-2](../images/k8s-nav2-two.png)

If you are taken straight to the Kubernetes Navigator v1 Map view after selecting **Kubernetes**, you need to opt-in to the new Navigator yourself for this workshop by clicking on the big blue {{% button style="blue" %}}Switch to new navigator{{% /button %}}.

You should now be in the K8s Node view with chart below the cluster map similar like shown below:

![k8s-navi-v-2](../images/new-k8s-view.png)

{{% notice title="Note" style="info" %}}
If you actually see three services for Kubernetes including one that is named `K8s clusters`, you need to turn off Precognition in the Superpowers view.
To do this, please change the Url in your browser to match the following: [https://app.[REALM].signalfx.com/#/superpowers](https://app.[REALM].signalfx.com/#/superpowers)

where [REALM] needs to match the Realm we are using for this workshop then remove the Precognition flag like in the example below. This is one of the first options you can set:

![Set-Precognition](../images/precognition.png)

Once its unset, you can refresh your page and reselect Kubernetes from the Infrastructure Navigator menu.
{{% /notice %}}

## 2. Connect to EC2 instance

You will be able to connect to the workshop instance by using SSH from your Mac, Linux or Windows device.

To use SSH, open a terminal on your system and type `ssh ubuntu@x.x.x.x` (replacing x.x.x.x with the IP address assigned to you).

{{% notice title="Note" color="info" %}}
Your workshop instance has been pre-configured with the correct `ACCESS_TOKEN` and `REALM` for this workshop. There is no need for you to configure these.
{{% /notice %}}

## 3. Namespaces in Kubernetes

Most of our customers will make use of some kind of private or public cloud service to run Kubernetes. They often choose to have only a few large Kubernetes clusters as it is easier to manage centrally.

Namespaces are a way to organize these large Kubernetes clusters into virtual sub-clusters. This can be helpful when different teams or projects share a Kubernetes cluster as this will give them the easy ability to just see and work with their own stuff.

Any number of namespaces are supported within a cluster, each logically separated from others but with the ability to communicate with each other. Components are only **visible** when selecting a namespace or when adding the `--all-namespaces` flag to `kubectl` instead of allowing you to view just the components relevant to your project by selecting your namespace.

Most customers will want to install the Splunk OpenTelemetry Collector in a separate namespace.  This workshop will follow that practice.

## 4. Install Splunk OTel using Helm

Install the OpenTelemetry Collector using the Splunk Helm chart. First, add the Splunk Helm chart repository and update.

{{< tabs >}}
{{% tab name="Helm Repo Add" %}}

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab name="Helm Repo Add Output" %}}

```text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

Install the OpenTelemetry Collector Helm chart into the `splunk` namespace with the following commands, do **NOT** edit this:

{{< tabs >}}
{{% tab name="Helm Install" %}}

``` bash
helm install splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
splunk-otel-collector-chart/splunk-otel-collector \
--namespace splunk \
--create-namespace \
-f ~/workshop/k3s/splunk-defaults.yaml
```

{{% /tab %}}
{{< /tabs >}}

## 5. Verify Deployment

You can monitor the progress of the deployment by running `kubectl get pods` and adding `-n splunk` to the command to see the pods in the `splunk` namespace which should typically report that the new pods are up and running after about 30 seconds.

Ensure the status is reported as **Running** before continuing.

{{< tabs >}}
{{% tab name="kubectl get pods" %}}

``` bash
kubectl get pods -n splunk
```

{{% /tab %}}
{{% tab name="kubectl get pods Output" %}}

``` text
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-pvstb                             2/2     Running   0          19s
splunk-otel-collector-k8s-cluster-receiver-6c454894f8-mqs8n   1/1     Running   0          19s
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Note" style="info" %}}

If you are using the Kubernetes Integration setup from the Data Management page from the O11y UI , you find that the guide will use
`--generate-name splunk-otel-collector-chart/splunk-otel-collector` instead of just `splunk-otel-collector-chart/splunk-otel-collector` as we do in the above example.

This will generate an unique name/label for the collector install and Pods by adding a unique number at the end of the object name, allowing you to install multiple collectors in your Kubernetes environment with different configurations.

Just make sure you use the correct label that is generated by the Helm chart if you wish to use the `helm` and `kubectl` commands from this workshop on an install done with the `--generate-name` option.
{{% /notice %}}

Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit).

{{< tabs >}}
{{% tab name="kubectl logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector -n splunk
```

{{% /tab %}}
{{< /tabs >}}

Or use the installed `k9s` terminal UI.

![k9s](../images/k9s.png)

{{% notice title="Deleting a failed installation" style="warning" %}}
If you make an error installing the Splunk OpenTelemetry Collector you can start over by deleting the installation using:

``` sh
helm delete splunk-otel-collector -n splunk
```
