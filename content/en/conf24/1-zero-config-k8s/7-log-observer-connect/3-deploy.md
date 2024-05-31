---
title: Deploy to Kubernetes
linkTitle: 3. Deploy to Kubernetes
weight: 3
---

To see the changes in effect, we need to redeploy the services, First, let's change the location of the images from the external repo to the local one by running the following script:

```bash
. ~/workshop/petclinic/scripts/set_local.sh
```

The result is a new file on disk called `petclinic-local.yaml`. Switch to the local versions by using the new version of the deployment YAML. First delete the old containers from the original deployment with:

```bash
kubectl delete -f ~/workshop/petclinic/petclinic-deploy.yaml
```

followed by:

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
```

This will cause the containers to be replaced with the local version, you can verify this by checking the containers:

```bash
kubectl describe pods api-gateway | grep Image:
```

The resulting output will show `localhost:9999`:

```text
  Image:         localhost:9999/spring-petclinic-api-gateway:local
```

However, as we only patched the deployment before, the new deployment does not have the right annotations for the **automatic discovery and configuration**, so let's fix that now by running the patch command again:

{{% notice note %}}

There will be no change for the **admin-server**, **config-server** and **discovery-server** as they are already annotated.

{{% /notice %}}

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
deployment.apps/config-server patched (no change)
deployment.apps/admin-server patched (no change)
deployment.apps/customers-service patched
deployment.apps/visits-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

Check the `api-gateway` container (again if you see two `api-gateway` containers, it's the old container being terminated so give it a few seconds):

```bash
kubectl describe pods api-gateway | grep Image:
```

The resulting output will show the local api gateway version `localhost:9999` and the auto-instrumentation container:

```text
  Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.32.1
  Image:         localhost:9999/spring-petclinic-api-gateway:local
```

Now that the Pods have been patched validate they are all running by executing the following command:

{{< tabs >}}
{{% tab title="Checking if all Pods are running" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
NAME                                                           READY   STATUS    RESTARTS   AGE
splunk-otel-collector-certmanager-cainjector-cd8459647-d42ls   1/1     Running   0          22h
splunk-otel-collector-certmanager-85cbb786b6-xgjgb             1/1     Running   0          22h
splunk-otel-collector-certmanager-webhook-75d888f9f7-477x4     1/1     Running   0          22h
splunk-otel-collector-agent-nmmkm                              1/1     Running   0          22h
splunk-otel-collector-k8s-cluster-receiver-7f96c94fd9-fv4p8    1/1     Running   0          22h
splunk-otel-collector-operator-6b56bc9d79-r8p7w                2/2     Running   0          22h
petclinic-loadgen-deployment-765b96d4b9-gm8fp                  1/1     Running   0          21h
petclinic-db-774dbbf969-2q6md                                  1/1     Running   0          21h
config-server-5784c9fbb4-9pdc8                                 1/1     Running   0          21h
admin-server-849d877b6-pncr2                                   1/1     Running   0          21h
discovery-server-6d856d978b-7x69f                              1/1     Running   0          21h
visits-service-c7cd56876-grfn7                                 1/1     Running   0          21h
customers-service-6c57cb68fd-hx68n                             1/1     Running   0          21h
vets-service-688fd4cb47-z42t5                                  1/1     Running   0          21h
api-gateway-59f4c7fbd6-prx5f                                   1/1     Running   0          20h
```

{{% /tab %}}
{{< /tabs >}}
