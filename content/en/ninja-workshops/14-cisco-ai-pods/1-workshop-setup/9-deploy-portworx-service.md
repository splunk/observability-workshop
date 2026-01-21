---
title: Deploy the Portworx Metrics Endpoint
linkTitle: 9. Portworx Metrics Endpoint
weight: 9
time: 10 minutes
---

In this step, we'll deploy a Python service that mimics the Portworx metrics endpoint. 
This will be used in the workshop to configure monitoring for Pure Storage. 

## Deploy the Portworx Metrics Endpoint

Run the following command to deploy the Portworx metrics endpoint service: 

``` bash
oc create project portworx
oc apply -f ./portworx/k8s.yaml -n portworx
```

## Test the Portworx Metrics Endpoint

Let's ensure the Portworx metrics endpoint is working as expected. 

Start a pod that has access to the curl command:

``` bash
oc run --rm -it -n default curl --image=curlimages/curl:latest -- sh
```

Then run the following command to send a prompt to the endpoint:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl http://portworx-metrics-sim.portworx:17001/metrics
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
# HELP px_cluster_cpu_percent Percentage of CPU Used
# TYPE px_cluster_cpu_percent gauge
px_cluster_cpu_percent{cluster="ocp-pxclus-32430549-ad99-4839-bf9b-d6beb8ddc2d6",clusterUUID="e870909b-6150-4d72-87cb-a012630e42ae",node="worker2.flashstack.local",nodeID="f63312a2-0884-4878-be4e-51935613aa80"} 1.91
...
```

{{% /tab %}}
{{< /tabs >}}
