---
title: 2. Deploy the Baseline
weight: 2
---

## Add Your Splunk Credentials

{{% notice title="Exercise" style="green" icon="running" %}}

Open `collector.yaml` and replace the four placeholder values in the `env` section:

``` bash
vi ~/workshop/obi/03-obi-k8s/collector.yaml
```

``` yaml
          env:
            - name: SPLUNK_INGEST_TOKEN
              value: "YOUR_TOKEN_HERE"
            - name: SPLUNK_REALM
              value: "us0"
            - name: WORKSHOP_HOST_NAME
              value: "jsmith-k8s"
            - name: WORKSHOP_ENVIRONMENT
              value: "jsmith-k8s-workshop"
```

Save the file.

{{% /notice %}}

## Apply the Manifests

Apply the manifests in order:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/03-obi-k8s
kubectl apply -f namespace.yaml
kubectl apply -f collector-configmap.yaml
kubectl apply -f collector.yaml
kubectl apply -f apps.yaml
kubectl apply -f load-generator.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
namespace/obi-workshop created
configmap/collector-config created
deployment.apps/splunk-otel-collector created
service/splunk-otel-collector created
deployment.apps/frontend created
service/frontend created
deployment.apps/order-processor created
service/order-processor created
deployment.apps/payment-service created
service/payment-service created
deployment.apps/load-generator created
```

{{% /tab %}}
{{< /tabs >}}

## Verify Pods Are Running

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n obi-workshop
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
NAME                                     READY   STATUS    RESTARTS   AGE
frontend-7d8b9f4c5-x2k4n                1/1     Running   0          30s
load-generator-5c6d7e8f9-m3j2k          1/1     Running   0          28s
order-processor-8e9f0a1b2-p4q5r         1/1     Running   0          30s
payment-service-9f0a1b2c3-s6t7u         1/1     Running   0          30s
splunk-otel-collector-6a7b8c9d0-v8w9x   1/1     Running   0          30s
```

{{% /tab %}}
{{< /tabs >}}

## Test the Application

Access the frontend via the NodePort:

``` bash
curl -s http://localhost:30000/create-order | python3 -m json.tool
```

## Confirm APM is Empty

{{% notice title="Exercise" style="green" icon="running" %}}

Check Splunk APM, filtering by your K8s environment. It should be **empty** -- no traces, no services. Same as Phase 1.

{{% /notice %}}
