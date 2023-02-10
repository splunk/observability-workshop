---
title: Istio Setup
weight: 1
---

CAVEAT: THIS LAB IS DESIGNED FOR THE UBUNTU SANDBOX CREATED AT THE START OF THE APM WORKSHOP AND IS TESTED IN THAT ENVIRONMENT ONLY
THIS LAB IS A WORK IN PROCESS AND YOUR RESULTS MAY VARY  

This exercise will install an Istio service mesh on a Kubernetes cluster that directs external requests to a Python Flask server.
Both the service mesh and the Flask server will emit spans.
The result will show tracing of the external request to the node and through the mesh to the Flask server.  

## 1: Install OpenTelemetry Collector

If you have an existing collector running remove it.

Follow Data Setup wizard but add:

```text
--set autodetect.istio=true`
```

i.e.

```bash
helm install \
--set splunkAccessToken='YOURTOKENHERE' \
--set clusterName='YOURCLUSTERNAMEHERE' \
--set splunkRealm='YOURREALMHERE' \
--set autodetect.istio=true \
--set provider=' ' \
--set distro=' ' \
--set otelCollector.enabled='false' \
--generate-name \
splunk-otel-collector-chart/splunk-otel-collector
```

## 2: Set Up Istio

Download Istio:

```bash
cd ~
curl -L https://istio.io/downloadIstio | sh -
```

Follow instructions from the installer script that are now in your terminal to add Istio's bin path to your env then:

```bash
istioctl install
```

## 3: Deploy Istio configurations and example Flask microservice

Enable automatic Istio proxy injection. [More info here](https://istio.io/latest/docs/setup/additional-setup/sidecar-injection/#automatic-sidecar-injection)

```bash
kubectl label namespace default istio-injection=enabled
```

Change to the APM Workshop Istio directory:  

```bash
cd ~/otelworkshop/k8s/istio
```

Install the Splunk tracing profile for Istio:

```bash
istioctl install -f tracing.yaml
```

Set and validate ingress ports for Nodeport example and configure ingress host for local k3s workshop example:  

```bash
source setup-envs.sh
```

You should see a result that looks like:  

```text
TCP_INGRESS_PORT=
INGRESS_PORT=30785
INGRESS_HOST=172.31.19.248
SECURE_INGRESS_PORT=32071
```

Deploy Flask service configured for Istio:  

!!! important
    If you are doing this workshop as part of a group, before the next step, add your initials do the APM environment: 
    edit the `flask-deployment-istio.yaml` below and add your initials to the environment i.e. change all instances:  
    `deployment.environment=apm-workshop`  
    to    
    `deployment.environment=sjl-apm-workshop` 

```bash
kubectl apply -f flask-deployment-istio.yaml
```

Single test Flask service:  
`source test-flask.sh`  

Results should show a direct request to the Flask server:  

```bash
You getted: b'' Request headers: Host: localhost:30001
User-Agent: curl/7.68.0
Accept: */*
Server: 1
```

Single test Istio:

```bash
source test-istio.sh
```

When hitting the service mesh from outside the cluster, you'll receive the mesh diagnostic data plus the B3 Trace/Span ID:

```bash
You getted: b'' Request headers: Host: 172.31.19.248:31177
User-Agent: curl/7.68.0
Accept: */*
Server: 1
X-Forwarded-For: 10.42.0.1
X-Forwarded-Proto: http
X-Envoy-Internal: true
X-Request-Id: 447af547-7b8f-96db-a0b5-08efce526a8d
X-Envoy-Decorator-Operation: server-flask-otel-k8s.default.svc.cluster.local:5000/echo
X-Envoy-Peer-Metadata: ChQKDkFQUF9DT05UQUlORVJTEgIaAAoaCgpDTFVTVEVSX0lEEgwaCkt...
3NnYXRld2F5
X-Envoy-Peer-Metadata-Id: router~10.42.0.11~istio-ingressgateway-7d97f78f5-dg5zc.istio-system~istio-system.svc.cluster.local
X-Envoy-Attempt-Count: 1
X-B3-Traceid: 5035304e854aa834e990df295b1d98e9
X-B3-Spanid: e990df295b1d98e9
X-B3-Sampled: 1
```

To generate many requests so that the example appears in the APM service map, use the load generator:  

Load gen Istio for two minutes:

```bash
source loadgen.sh
```

You will see a service map with the Istio mesh and the Flask server:  

![Istio](../../../../images/istio1.png)

Traces will show the request hitting the service mesh and the mesh hitting the service itself:  

[Istio2](../../../../images/istio2.png)

Stop loadgen:

++ctrl+c++

Cleanup:  
remove k8s examples:

```bash
source delete-all.sh
```

Remove Istio:  
From the Istio bin directory:

```bash
istioctl x uninstall --purge
```
