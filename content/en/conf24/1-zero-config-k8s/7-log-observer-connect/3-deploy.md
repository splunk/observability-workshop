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

```bash
kubectl get pods
```
