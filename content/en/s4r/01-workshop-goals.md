---
title: Workshop Agenda
weight: 10
---
The goal of this workshop is to make you famliar with the Splunk Observability Suite and its key features.
For this we have provided you with a complete application that includes a Website and a number of back end services  that make up the complete application.

During this workshop you will expierince issues with this application. The goal of this excercise is to use several of the key features from the Splunk observability suite to detect the issue, locate  the cause of the issue, allowing you developerers to very quickly resolve the issue.

### 1. Inital Setup 
For attendees that are taking the **pre-configured workshop**, the application will already be deployed for you and your instructor will provide with a link to the Online Boutique application.

For attendees taking the **interactive workshop**, you will need to install OpenTelemetry and deploy the application. Hit the {{% badge style=primary icon=user-ninja %}}**Ninja{{% /badge %}} button below to expand the instructions.

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Interactive workshop build steps{{% /badge %}}" %}}

Install the OpenTelemetry Collector using the Splunk Helm chart. First, add the Splunk Helm chart repository to Helm and update.

{{< tabs >}}
{{% tab title="Helm Repo Add" %}}

``` bash
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart && helm repo update
```

{{% /tab %}}
{{% tab title="Helm Repo Add Output" %}}
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
"splunk-otel-collector-chart" has been added to your repositories
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "splunk-otel-collector-chart" chart repository
Update Complete. ⎈Happy Helming!⎈
{{% /tab %}}
{{< /tabs >}}

Install the OpenTelemetry Collector Helm chart with the following commands, do **NOT** edit this:

{{< tabs >}}
{{% tab title="Helm Install" %}}

```bash
helm install splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$(hostname)-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml
```

{{% /tab %}}
{{% tab title="Helm Install Output" %}}

``` text
Using ACCESS_TOKEN={REDACTED}
Using REALM=eu0
NAME: splunk-otel-collector
LAST DEPLOYED: Fri May  7 11:19:01 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

{{% /tab %}}
{{< /tabs >}}

You can monitor the progress of the deployment by running `kubectl get pods` which should typically report a new pod is up and running after about 30 seconds.

Ensure the status is reported as Running before continuing.

{{< tabs >}}
{{% tab title="Kubectl Get Pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Kubectl Get Pods Output" %}}

``` text
NAME                                                          READY   STATUS    RESTARTS   AGE
splunk-otel-collector-agent-2sk6k                             0/1     Running   0          10s
splunk-otel-collector-k8s-cluster-receiver-6956d4446f-gwnd7   0/1     Running   0          10s
```

{{% /tab %}}
{{< /tabs >}}

To deploy the Online Boutique application into K3s apply the deployment:

{{< tabs >}}
{{% tab title="Deploy Online Boutique" %}}

``` bash
cd ~/workshop/apm
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Deployment Output" %}}

``` text
APM Only Deployment
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/rum-loadgen-deployment created
```

{{% /tab %}}
{{< /tabs >}}

To ensure the Online Boutique application is running:

{{< tabs >}}
{{% tab title="Get Pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Get Pods Output" %}}

``` text
NAME                                                       READY  STATUS  RESTARTS      AGE
splunk-otel-collector-k8s-cluster-receiver-849cf595bf-l7mnq 1/1   Running   0           31m
splunk-otel-collector-agent-pxrgp                           2/2   Running   0           31m
productcatalogservice-8464cd56d-n8f89                       1/1   Running   0            1m
redis-cart-bcf44df97-djv6z                                  1/1   Running   0            1m
checkoutservice-8558fd7b95-b9pn8                            1/1   Running   0            1m
shippingservice-7cc4bdd6f4-xsvnx                            1/1   Running   0            1m
recommendationservice-647d57fd44-l7tkq                      1/1   Running   0            1m
frontend-66c5d589d-55vzb                                    1/1   Running   0            1m
emailservice-6ff5bbd67d-pdcm2                               1/1   Running   0            1m
paymentservice-6866558995-8xmf2                             1/1   Running   0            1m
currencyservice-8668d75d6f-mr68h                            1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-cr4pr                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-qjr4b                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-fvb4x                     1/1   Running   0            1m
cartservice-7b58c88c45-xvxhq                                1/1   Running   0            1m
loadgenerator-6bdc7b4857-9kxjd                              1/1   Running   2 (49s ago)  1m
adservice-7b68d5b969-89ft2                                  1/1   Running   0            1m
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Info" style="info" %}}
Usually it should only take around 1min 30secs for the pods to transition into a Running state.
{{% /notice %}}

{{% /expand %}}

---

### 2. A quick tour of the Splunk Observability User Interface

To make finding your way in the Splunk Observability suite User interface, We will take you on a quick tour that will give you the highlights and is designed to make the rest of the workhop simpler as you are already fmailiar with the locations of various components.

---

### 3. Using the Online Boutique Webshop to create traffic
The next step in the workshop is to use the Web ui of the application we provided, We wil assk you to run several scenario's, and if possible repeat some of the actions on an other device, something like a mobile phone for example.

This will generate traffic acorr our appliction and with that traffic comes the Open Telemetry signals, Metrics, Traces and logs,  that we can use to find and indentify the cause of the underlying issues. 

---

### 4. Splunk Real User Monitoring

During this session we will examine the Real User  data that has been provided by the telemetry  recieved  from your website. The goal is to fidn and identify the activity you have created  with your browser, and if possible from a different device like a mobile phone.  This will show you some of the issues you can detect with Splunk RUM.  It will also show you how we can  folow intereactiosn from the front end website to the underlying dunctions in the back end services

---

### 5 Splunk Application Perfomance Monitoring

Follwing up form our finsing in the RUm session, we will follow theroute are request have takne though the underlying backend service.s for this we are using Application Monitoring or APM, all our services are sneding telemtry,or Traces and spans, that the Splunk observability suite can visualise, analyze and use to detect anomolise and errrors.
In this session we show you several ways to find and detect errors mannually or with the support of our smart Analytics.

---

### 6 Using Logs with Splunk Log Observer
Generally, you use metrics and traces to detect  and identify an issue, and use Logs with itch richer information pool, to indity the why, or the casue of the issue.  Within this section we will examine the functionality of Log observer, our gateway in the logs generated by our apllications.

---

### 7 Splunk Synthetics
The next step is is to make sure we do not rely on manual testing of our application, and we will look at how you can create  tests that can keep track of the performance and behaviour of your application that can run 24/7 from different location.
We also look into how these test can alert you when ther is a deviation in behaviour of your site.

---

### 8 Wrapping upp

Last but not least we will show some of the other features that can be help full in finding problems  befor clsoing the session.
