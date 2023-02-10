---
title: APM for K8s
weight: 1
---
Identify your token and realm from the Splunk Observability Cloud Portal:   
`Organization Settings->Access Tokens` and `Your Name->Account Settings`  

> <ins>If using your own k8s cluster on an Ubuntu host</ins>  
> Remove the Otel Collector if its running on the same host as your k8s cluster:
> ```bash
> sudo sh /tmp/splunk-otel-collector.sh --uninstall
> ```
> Use this setup script to bootstrap your Debian based k8s environment with everything needed for the k8s workshop:  
```
bash <(curl -s https://raw.githubusercontent.com/signalfx/otelworkshop/master/setup-tools/k8s-env-only.sh)
```
> Ensure you have `helm` and `lynx` installed.  
>  
> Skip to: **2: Deploy APM for containerized apps: Python and Java**  
> If you are using k8s anywhere else you can still do this workshop but will need to ensure `helm`, `lynx` are available.

---
### 1: Use Data Setup Wizard for Splunk Otel Collector Pod on k3s

>**IMPORTANT: If you have the Otel Collector and prior lab examples running on a host, them at this time:**  
>Stop all the prior labs apps by using `ctrl-c` in each terminal window and then closing the window.  
>Remove the host based otel collector: 
>`sudo sh /tmp/splunk-otel-collector.sh --uninstall`

#### 1a: Splunk Observability Cloud Portal
 
In Splunk Observability Cloud: `Data Setup->Kubernetes->Add Connection`  

<img src="../../../images/17-datasetup-k8s.png" width="360">  

Choose the following:

| Key | Value |
| ----- | ---- |
| Access Token | Select from list |
| Cluster Name | Your initials-cluster i.e. SL-cluster |
| Provider | Other |
| Distribution | Other |
| Add Gateway | No |
| Log Collection | True |  

And then select `Next`  

Follow the steps on the `Install Integration` page.

<img src="../../../images/18-datasetup-k8sinstall.png" width="360"> 

A result will look like this:  
```
NAME: splunk-otel-collector-1620505665
LAST DEPLOYED: Sat May  8 20:27:46 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

Note the name of the deployment when the install completes i.e.:   `splunk-otel-collector-1620505665`  

#### 1b: Update k3s For Splunk Log Observer (Ignore if you are using k8s)

k3s has a different format that standard k8s for logging and we need to update our deployment for this.  

You'll need the Collector deployment from the Data Setup Wizard install.  

You can also dervice this from using `helm list` i.e.:  
```
NAME                                    NAMESPACE       REVISION        UPDATED                                 STATUS       CHART                           APP VERSION
splunk-otel-collector-1620504591        default         1               2021-05-08 20:09:51.625419479 +0000 UTC deployed     splunk-otel-collector-0.25.0  
```
The deployment name would be: `splunk-otel-collector-1620504591`  

#### Prepare values for Collector update  

If you run into any errors from helm, fix with:  
```
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
sudo chmod 755 /etc/rancher/k3s/k3s.yaml
```

Prep values for collector update:  

`helm list`  
`helm get values NAME`  

i.e. `helm get values splunk-otel-collector-1620609739`

make note of:  
`clusterNAME`  
`splunkAccessToken`  
`splunkRealm`  

#### Prepare values.yaml file for updating the Helm chart  

Start in k8s directory:
```bash
cd ~/otelworkshop/k8s
```

Edit `k3slogs.yaml` with thes values above.

#### Update the Collector 

Install the Collector configuration chart:  

```
helm upgrade \
YOURCOLLECTORHERE \
--values k3slogs.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

i.e.

```
helm upgrade \
splunk-otel-collector-1620609739 \
--values k3slogs.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

---
### 2: Deploy APM For Containerized Apps: Python and Java

!!! important
    If you are doing this workshop as part of a group, before the next step, add your initials do the APM environment: 
    edit the `py-deployment.yaml` below and add your initials to the environment i.e. change all instances:  
    `deployment.environment=apm-workshop`  
    to    
    `deployment.environment=sjl-apm-workshop` 

Deploy the Flask server deployment/service and the python-requests (makes requests of Flask server) pod:  
```
cd ~/otelworkshop/k8s
kubectl apply -f py-deployment.yaml
```

!!! important
    If you are doing this workshop as part of a group, before the next step, add your initials do the APM environment: 
    edit the `java-deployment.yaml` below and add your initials to the environment i.e. change all instances:  
    `deployment.environment=apm-workshop`  
    to    
    `deployment.environment=sjl-apm-workshop`  
     
Deploy the Java OKHTTP requests pod (makes requests of Flask server):  
```
kubectl apply -f java-deployment.yaml
```
Study the results:

The APM Dashboard will show the instrumented Python-Requests and Java OKHTTP clients posting to the Flask Server.  
Make sure you select the `apm-workshop` ENVIRONMENT to monitor.

<img src="../../../images/19-k8s-apm.png" width="360">  

Study the `deployment.yaml` files:

Example in Github or:  
```
~/otelworkshop/k8s/py-deployment.yaml   
~/otelworkshop/k8s/java-deployment.yaml   
```
The .yaml files show the environment variables telling the instrumentation to send spans to the OpenTelemetry Collector.

Normally we use an environment variable pointing to `localhost` on a single host application where the Collector is running. In k8s we have separate pods in a cluster for apps and the Collector.   

The Collector pod is running with <ins>node wide visibility</ins>, so to tell each application pod where to send spans:

```
- name: SPLUNK_OTEL_AGENT
  valueFrom:
    fieldRef:
      fieldPath: status.hostIP
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: "http://$(SPLUNK_OTEL_AGENT):4317"
```

---
### 3: Monitor JVM Metrics For a Java Container

JVM Metrics are emitted by the Splunk OpenTelemetry Java instrumentation and send to the Collector.  
 
Download this file to your local machine: [JVM Metrics Dashboard Template](https://raw.githubusercontent.com/signalfx/otelworkshop/master/k8s/dashboard_JVMMetrics.json)  

Select the + Icon on top right and create a new **Dashboard Group** called `test`  

Click the + Icon again and select `Import->Dahsboard`  
and select the downloaded `dashboard_JVMMetrics.json` file.   

<img src="../../../images/27-jvm.png" width="360">    

Filter by Application by adding `service:SERVICENAMEHERE`  

<img src="../../../images/28-jvm-filter.png" width="360">    

Complete JVM metrics available [at this link](https://github.com/signalfx/splunk-otel-java/blob/main/docs/metrics.md#jvm)

---
### 4:  Manually instrument a Java App And Add Custom Attributres (Tags)

Let's say you have an app that has your own functions and doesn't only use auto-instrumented frameworks- or doesn't have any of them!  

You can easily manually instrument your functions and have them appear as part of a service, or as an entire service.

Example is here:

`cd ~/otelworkshop/k8s/java/manual-inst`  

Deploy an app with ONLY manual instrumentation:  

!!! important
    If you are doing this workshop as part of a group, before the next step, add your initials do the APM environment: 
    edit the `java-reqs-manual-inst.yaml` below and add your initials to the environment i.e. change all instances:  
    `deployment.environment=apm-workshop`  
    to    
    `deployment.environment=sjl-apm-workshop`  
    
```
kubectl apply -f java-reqs-manual-inst.yaml
```

When this app deploys, it appears as an isolated bubble in the map. It has all metrics and tracing just like an auto-instrumented app does. 

<img src="../../../images/20-k8s-manual.png" width="360">  

Take a look at the traces and their spans to see the manually added values of Message, Logs etc.

<img src="../../../images/21-k8s-m-trace.png" width="360">  

You will see the function called ExampleSpan with custom `Logging` messages and a `message:myevent` span/tag.  

<img src="../../../images/22-k8s-m-span1.png" width="360">  

<img src="../../../images/23-k8s-m-span2.png" width="360">  

See the custom attribute `my.key` and value `myvalue`.  
This could be a transaction ID, user ID, or any custom value that you want to correlate and even metricize.  

<img src="../../../images/23-k8s-m-span3.png" width="360">  

Study the [manual instrumentation code example here.](https://github.com/signalfx/otelworkshop/blob/master/k8s/java/manual-inst/src/main/java/sf/main/GetExample.java)

There are two methods shown- the decorator @WithSpan method (easiest), and using the GlobalTracer method (more complicated/powerful)...

Note that this is the most minimal example of manual instrumentation- there is a vast amount of power available in OpenTelemetry- please see [the documentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation) and [in depth details](https://github.com/open-telemetry/opentelemetry-java/blob/master/QUICKSTART.md#tracing)

---
### 5: Process Spans with the Otel Collector

The Otel Collector has many powerful configuration options ranging from splitting telemetry to multiple destinations to sampling to span processing.  

[Processor documentation](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor)  

[Collector config examples](https://github.com/signalfx/splunk-otel-collector-chart/tree/main/examples)  

[Full documentation](https://github.com/signalfx/splunk-otel-collector)  

#### Prepare values for Collector update

```
helm list
```
```
helm get values NAME
```

i.e. `helm get values splunk-otel-collector-1620609739`

make note of:  
`clusterNAME`  
`splunkAccessToken`  
`splunkRealm`  

#### Span Processing Example: Redacting Data from a Span Attribute

Change to the example directory:
```
cd ~/otelworkshop/k8s/collectorconfig
```

#### Prepare values.yaml file for updating the Helm chart  

Edit `spanprocessor.yaml` with thes values from Step 1.  

#### Update the Collector 

Install the Collector configuration chart:  

```
helm upgrade --install \ 
YOURCOLLECTORHERE \
--values spanprocessor.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

i.e.

```
helm upgrade  --install \
splunk-otel-collector-1620609739 \
--values spanprocessor.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

Study the results:  

`Splunk Observability Portal -> APM -> Explore -> java-otel-manual-inst -> Traces`

Example `my.key` and you'll see that the value is `redacted` after applying the `spanprocessor.yaml` example

<img src="../../../images/25-span-redacted.png" width="360">  

If you want to make changes and update the `spanprocessor.yaml` or add more configurations, use:  
`helm upgrade --reuse-values`

---
### 6: Receive Prometheus Metrics at the Otel Collector

#### Add a Prometheus endpoint pod  

Change to the k8s Collector Config directory:  
```
cd ~/otelworkshop/k8s/collectorconfig
```

Add the Prometheus pod (source code is in the `k8s/python` directory):
```
kubectl apply -f prometheus-deployment.yaml
```

#### Update Otel Collector to Scrape the Prometheus Pod

Update realm/token/cluster in the `otel-prometheus.yaml`  

Verify your helm deployment of the collector:

```
helm list
```

Upgrade the Collector deployment with the values required for scraping Prometheus metrics from the Prometheus pod deployed in the previous step:

```
helm upgrade --reuse-values splunk-otel-collector-YOURCOLLECTORVALUE --values otel-prometheus.yaml splunk-otel-collector-chart/splunk-otel-collector
```

#### Find Prometheus Metric and Generate Chart

`Splunk Observabilty -> Menu -> Metrics -> Metric Finder`  

Search for: `customgauge`  

Click `CustomGauge`  

Chart appears with value `17`

Examine the collector update `otel-prometheus.yaml` to see how this works.

---
### 7: Configure Otel Collector to Transform a Metric Name

This example uses the [Metrics Transform Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor)  

Change to the k8s Collector Config directory:  
```
cd ~/otelworkshop/k8s/collectorconfig
```
Update realm/token/cluster in the `metricstransform.yaml` with your token/realm/cluster  

Upgrade the Collector deployment with the values required for scraping Prometheus metrics from the Prometheus pod deployed in the previous step:

```
helm upgrade --reuse-values splunk-otel-collector-YOURCOLLECTORVALUE --values metricstransform.yaml splunk-otel-collector-chart/splunk-otel-collector
```

#### Find Transformed Prometheus Metric and Generate Chart

`Splunk Observabilty -> Menu -> Metrics -> Metric Finder`  

Search for: `transformedgauge`  

Click `TransformedGauge`  

You'll now see the new chart for the metric formerly known as CustomGauge that has been transformed using the metrics transform processor.  

Examine the collector update `metricstransform.yaml` to see how this works.

---
### Monitoring and Troubleshooting  

#### View Otel Collector POD stats

```
kubectl get pods
```

Note the pod name of the `OpenTelemetry Collector` pod i.e.:  
`splunk-otel-collector-1620505665-agent-sw45w`

Send the Zpages stats to the lynx browser:  
```
kubectl exec -it YOURAGENTPODHERE -- curl localhost:55679/debug/tracez | lynx -stdin
```  
i.e.
```
kubectl exec -it splunk-otel-collector-1620505665-agent-sw45w -- curl localhost:55679/debug/tracez | lynx -stdin
```

<img src="../../../images/06-zpages.png" width="360"> 

#### Examine Otel Collector Config

get your Collector agent pod name via:
```
kubectl get pods
```

i.e.

`splunk-otel-collector-1626453714-agent-vfr7s` 

Show current Collector config:  
```
kubectl exec -it YOURAGENTPODHERE -- curl localhost:55554/debug/configz/effective
```

Show initial Collector config:  
```
kubectl exec -it YOURAGENTPODHERE -- curl localhost:55554/debug/configz/initial
```

---
### Bonus Instrumentation Examples: Istio and .NET

#### .NET: containerized example is [located here](../examples/dotnet/)  
#### Istio: service mesh [lab here](../examples/istio/)

---
### Clean up deployments and services

To delete all k8s lab work:  
in `~/otelworkshop/k8s/`  
```
source delete-all-k8s.sh
source delete-prometheus.sh
```

To delete the Collector from k8s:  
```
helm list
```  
`helm delete YOURCOLLECTORHERE`
i.e.
```
helm delete splunk-otel-collector-1620505665
```

k3s:
```
/usr/local/bin/k3s-uninstall.sh
```