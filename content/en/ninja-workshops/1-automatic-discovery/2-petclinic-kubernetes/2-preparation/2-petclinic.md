---
title: Deploy the PetClinic Application
linkTitle: 2. Deploy PetClinic Application
weight: 3
---

The first deployment of our application will be using prebuilt containers to give us the base scenario: a regular Java microservices-based application running in Kubernetes that we want to start observing. So let's deploy our application:

{{< tabs >}}
{{% tab title="kubectl apply" %}}

``` bash
kubectl apply -f ~/workshop/petclinic/petclinic-deploy.yaml
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
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

At this point, we can verify the deployment by checking if the Pods are running. The containers need to be downloaded and started so this may take a couple of minutes.

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
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

Make sure the output of `kubectl get pods` matches the output as shown above. Ensure all the services are shown as **Running** (or use `k9s` to contuuously monitor the status).

Once they are running, the application will take a few minutes to fully start up, create the database and synchronize all the services, so let's use the time to check the local private repository is active.

#### Verify the local Private Registry

Later on, when we test our **automatic discovery and configuration** we are going to build new containers to highlight some of the additional features of Splunk Observability Cloud.

As configuration files and source code will be changed, the containers will need to be built and stored in a local private registry (which has already been enabled for you).

To check if the private registry is avaiable, run the following command (this will return an empty list):

{{< tabs >}}
{{% tab title="Check the local Private Registry" %}}

``` bash
curl -X GET http://localhost:9999/v2/_catalog
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
**{"repositories":[]}**
```

{{% /tab %}}
{{< /tabs >}}
