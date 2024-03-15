---
title: Preparation of the Pet Clinic application. 
linkTitle: 10. Preparation
weight: 10
---

## 1. Validate the settings for your workshop

The instructor will provide you with the login information for the instance that we will be using during the workshop.
When you first log into your instance, you will be greeted by the Splunk Logo as shown below:

```text
❯ ssh -p 2222 splunk@[IP-ADDRESS]

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗  
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗ 
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝ 
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  
Last login: Mon Feb  5 11:04:54 2024 from [Redacted]
Waiting for cloud-init status...
Your instance is ready!
splunk@show-no-config-i-0d1b29d967cb2e6ff:~$ 
```

If this isn't shown, or you see an error, log out and give it a minute or so, then try to log in again as the instance might not have finished the initial boot sequence. If it still does not show the above Welcome page, reach out to your Instructor.

Next, let's ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following command:

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

In the output check the following environment variables are present and have actual valid values set:

{{% tab title="Example output" %}}

```text
ACCESS_TOKEN = [Redacted]
REALM = [Realm]
RUM_TOKEN = [Redacted]
HEC_TOKEN = [Redacted]
HEC_URL = https://[...]/services/collector/event
INSTANCE = [Your workshop name]
```

{{% /tab %}}

Please make a note of the `INSTANCE` environment variable value as this is the reference to your workshop instance and we will need it later to filter data in the **Splunk Observability Suite** UI.

For this workshop, **all** of the above are required. If any have values missing, please contact your instructor.

{{% notice title="Delete any existing OpenTelemetry Collectors" style="warning" %}}
If you have completed a Splunk Observability workshop using this EC2 instance, please ensure you have deleted the collector running in Kubernetes before continuing with this workshop. This can be done by running the following command:

``` bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 2. The Splunk OpenTelemetry Collector

The Splunk OpenTelemetry Collector is the core component of instrumenting infrastructure and applications.  Its role is to collect and send:

* Infrastructure metrics (disk, CPU, memory, etc)
* Application Performance Monitoring (APM) traces
* Profiling data
* Host and Application logs

To get Observability signals (**Metrics, Traces** and **Logs**) into the **Splunk Observability Cloud** we need to add an OpenTelemetry Collector to our Kubernetes cluster.
For this workshop, we will be using the Splunk Kubernetes Helm Chart for the Opentelemetry collector and installing the collector in `Operator` mode as this is required for Zero-config.

## 3. Install the OpenTelemetry Collector using Helm

First, we need to add the Splunk Helm chart repository to Helm and update it so it knows where to find it:

{{< tabs >}}
{{% tab title="Helm Repo Add" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Helm Repo Add Output" %}}

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

The Splunk Observability Cloud offers wizards in the **Splunk Observability Suite** UI to walk you through the setup of the Collector on  Kubernetes, but in the interest of time, we will use a setup created earlier. As we want the auto instrumentation to be available, we will install the OpenTelemetry Collector with the OpenTelemetry Collector Helm chart with some additional options:

* `--set="operator.enabled=true"` - this will install the Opentelemetry operator, that will be used to handle auto instrumentation
* `--set="certmanager.enabled=true"` - This will install the required certificate manager for the operator.
* `--set="splunkObservability.profilingEnabled=true"` - This enabled Code profiling via the operator

To install the collector run the following commands, do **NOT** edit this:

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
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

{{% /tab %}}
{{% tab title="Helm Install Output" %}}

```text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
NAME: splunk-otel-collector
LAST DEPLOYED: Tue Jan  2 13:46:16 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-o11y-suite-eu0.stg.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.

[INFO] You've enabled the operator's auto-instrumentation feature (operator.enabled=true), currently considered ALPHA.
- Instrumentation library maturity varies (e.g., Java is more mature than Go). For library stability, visit: https://opentelemetry.io/docs/instrumentation/#status-and-releases
  - Some libraries may be enabled by default. For current status, see: https://github.com/open-telemetry/opentelemetry-operator#controlling-instrumentation-capabilities
  - Splunk provides best-effort support for native OpenTelemetry libraries, and full support for Splunk library distributions. For used libraries, refer to the values.yaml under "operator.instrumentation.spec".
```

{{% /tab %}}
{{< /tabs >}}

You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds.

Ensure the status is reported as **Running** before continuing.

{{< tabs >}}
{{% tab title="Kubectl Get Pods" %}}

``` bash
kubectl get pods|grep splunk-otel 
```

{{% /tab %}}
{{% tab title="Kubectl Get Pods Output" %}}

``` text
splunk-otel-collector-certmanager-cainjector-5c5dc4ff8f-95z49   1/1     Running   0          10m
splunk-otel-collector-certmanager-6d95596898-vjxss              1/1     Running   0          10m
splunk-otel-collector-certmanager-webhook-69f4ff754c-nghxz      1/1     Running   0          10m
splunk-otel-collector-k8s-cluster-receiver-6bd5567d95-5f8cj     1/1     Running   0          10m
splunk-otel-collector-agent-tspd2                               1/1     Running   0          10m
splunk-otel-collector-operator-69d476cb7-j7zwd                  2/2     Running   0          10m
```

{{% /tab %}}
{{< /tabs >}}

Ensure there are no errors by tailing the logs from the OpenTelemetry Collector pod. The output should look similar to the log output shown in the Output tab below.
Use the label set by the `helm` install to tail logs (You will need to press `ctrl + c` to exit). Or use the installed `k9s` terminal UI for bonus points!

{{< tabs >}}
{{% tab title="Kubectl Logs" %}}

``` bash
kubectl logs -l app=splunk-otel-collector -f --container otel-collector
```

{{% /tab %}}
{{% tab title="Kubectl Logs Output" %}}

```text
2021-03-21T16:11:10.900Z        INFO    service/service.go:364  Starting receivers...
2021-03-21T16:11:10.900Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "prometheus", "component_name": "prometheus"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:70 Receiver is starting... {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/watcher.go:195       Configured Kubernetes MetadataExporter  {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster", "exporter_name": "signalfx"}
2021-03-21T16:11:11.009Z        INFO    builder/receivers_builder.go:75 Receiver started.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.009Z        INFO    healthcheck/handler.go:128      Health Check state change       {"component_kind": "extension", "component_type": "health_check", "component_name": "health_check", "status": "ready"}
2021-03-21T16:11:11.009Z        INFO    service/service.go:267  Everything is ready. Begin running and processing data.
2021-03-21T16:11:11.009Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:59       Starting shared informers and wait for initial cache sync.      {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
2021-03-21T16:11:11.281Z        INFO    k8sclusterreceiver@v0.21.0/receiver.go:75       Completed syncing shared informer caches.       {"component_kind": "receiver", "component_type": "k8s_cluster", "component_name": "k8s_cluster"}
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Deleting a failed installation" style="info" %}}
If you make an error installing the OpenTelemetry Collector you can start over by deleting the installation using:

``` sh
helm delete splunk-otel-collector
```

{{% /notice %}}

## 4. Deploying the PetClinic Application with prebuilt containers into Kubernetes

The next thing we need to do, well ..., is to set up our application. The first deployment of our application will be using prebuilt containers to give us the base scenario: a regular Java microservices-based application running in Kubernetes that we want to start observing.

So let's deploy our application:
{{< tabs >}}
{{% tab title="kubectl apply" %}}

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-deploy.yaml
```

{{% /tab %}}
{{% tab title="kubectl apply Output" %}}

```text
deployment.apps/config-server created
service/config-server created
deployment.apps/discovery-server created
service/discovery-server created
deployment.apps/api-gateway created
service/api-gateway created
service/api-gateway-external created
deployment.apps/customers-service created
service/customers-service created
deployment.apps/vets-service created
service/vets-service created
deployment.apps/visits-service created
service/visits-service created
deployment.apps/admin-server created
service/admin-server created
service/petclinic-db created
deployment.apps/petclinic-db created
configmap/petclinic-db-initdb-config created
deployment.apps/petclinic-loadgen-deployment created
configmap/scriptfile created
```

{{% /tab %}}
{{< /tabs >}}

<!-- {{% notice title="In case of error Unable to read /etc/rancher/k3s/k3s.yaml" style="warning" %}}
On rare occasions, you may encounter the above error at this point.  please log out and back in, and verify the above env variables are all set correctly. If not please, please contact your instructor.

{{% /notice %}} -->
At this point, we can verify the deployment by checking if the Pods are running, Not that these containers need to be downloaded and started, this may take a minute or so.
{{< tabs >}}
{{% tab title="kubectl get pods" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

```text
NAME                                                            READY   STATUS    RESTARTS   AGE
splunk-otel-collector-certmanager-dc744986b-z2gzw               1/1     Running   0          114s
splunk-otel-collector-certmanager-cainjector-69546b87d6-d2fz2   1/1     Running   0          114s
splunk-otel-collector-certmanager-webhook-78b59ffc88-r2j8x      1/1     Running   0          114s
splunk-otel-collector-k8s-cluster-receiver-655dcd9b6b-dcvkb     1/1     Running   0          114s
splunk-otel-collector-agent-dg2vj                               1/1     Running   0          114s
splunk-otel-collector-operator-57cbb8d7b4-dk5wf                 2/2     Running   0          114s
petclinic-db-64d998bb66-2vzpn                                   1/1     Running   0          58s
api-gateway-d88bc765-jd5lg                                      1/1     Running   0          58s
visits-service-7f97b6c579-bh9zj                                 1/1     Running   0          58s
admin-server-76d8b956c5-mb2zv                                   1/1     Running   0          58s
customers-service-847db99f79-mzlg2                              1/1     Running   0          58s
vets-service-7bdcd7dd6d-2tcfd                                   1/1     Running   0          58s
petclinic-loadgen-deployment-5d69d7f4dd-xxkn4                   1/1     Running   0          58s
config-server-67f7876d48-qrsr5                                  1/1     Running   0          58s
discovery-server-554b45cfb-bqhgt                                1/1     Running   0          58s
```

{{% /tab %}}
{{< /tabs >}}

Make sure the output of get pods matches the output as shown above. This may take a minute or so, try again until all services are shown as **RUNNING**.  

Once they are running, the application will take a few minutes to fully start up, create the database and synchronize all the services, so let's use the time to see if our local repository is active.

## 5. Verify the local Docker Repository

Once we have tested our Zero Auto-Config Instrumentation in the existing containers, we are going to build our containers to show some of the additional instrumentation features of Opentelemetry Java. Only then we will touch the config files or the source code. Once we build these containers, Kubernetes will need to pull these new images from somewhere. To enable this we have created a local repository to store these new containers, so Kubernetes can pull the images locally.

We can see if the repository is up and running by checking the inventory with the below command:

```bash
 curl -X GET http://localhost:9999/v2/_catalog 
```

It should return an empty list  

{{% tab title="Example output" %}}

```text
**{"repositories":[]}**
```

{{% /tab %}}
If this is not up, reach out to your Instructor for a replacement instance.
