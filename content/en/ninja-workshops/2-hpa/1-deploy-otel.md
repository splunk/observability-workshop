---
title: Deploying the OpenTelemetry Collector in Kubernetes
linkTitle: 1. Deploy the OTel Collector
weight: 1
---

## 1. Connect to EC2 instance

You will be able to connect to the workshop instance by using SSH from your Mac, Linux or Windows device. Open the link to the sheet provided by your instructor. This sheet contains the IP addresses and the password for the workshop instances.

{{% notice style="info" %}}
Your workshop instance has been pre-configured with the correct **Access Token** and **Realm** for this workshop. There is no need for you to configure these.
{{% /notice %}}

## 2. Install Splunk OTel using Helm

Install the OpenTelemetry Collector using the Splunk Helm chart. First, add the Splunk Helm chart repository and update:

{{< tabs >}}
{{% tab title="helm repo add" %}}

```bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="helm repo add output" %}}

```text
Using ACCESS_TOKEN=<REDACTED>
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN=<REDACTED>
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
```

{{% /tab %}}
{{< /tabs >}}

Install the OpenTelemetry Collector Helm with the following commands, do **NOT** edit this:

{{< tabs >}}
{{% tab title="helm install" %}}

``` bash
helm install splunk-otel-collector --version {{< otel-version >}} \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

{{% /tab %}}
{{< /tabs >}}

## 3. Verify Deployment

You can monitor the progress of the deployment by running `kubectl get pods` which should typically report that the new pods are up and running after about 30 seconds.

Ensure the status is reported as **Running** before continuing.

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

``` text
NAME                                                         READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-ks9jn                            1/1     Running   0          27s
splunk-otel-collector-agent-lqs4j                            0/1     Running   0          27s
splunk-otel-collector-agent-zsqbt                            1/1     Running   0          27s
splunk-otel-collector-k8s-cluster-receiver-76bb6b555-7fhzj   0/1     Running   0          27s
```

{{% /tab %}}
{{< /tabs >}}

Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit).

{{< tabs >}}
{{% tab title="kubectl logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{< /tabs >}}

Or use the installed `k9s` terminal UI.

![k9s](../images/k9s.png)

{{% notice title="Deleting a failed installation" style="warning" %}}
If you make an error installing the Splunk OpenTelemetry Collector you can start over by deleting the installation using:

``` sh
helm delete splunk-otel-collector
```

{{% /notice %}}
