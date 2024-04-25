---
title: Deploy to Kubernetes
linkTitle: 4. Deploy to Kubernetes
weight: 4
---

To see the changes in effect, we need to redeploy the services, First, let's change the location of the images from the external repo to the local one by running the following script:

```bash
. ~/workshop/petclinic/scripts/set_local.sh
```

The result is a new file on disk called **petclinic-local.yaml**. Let's switch to the local versions by using the new version of the `deployment.yaml`. First delete the old containers from the original deployment with:

```bash
kubectl delete -f ~/workshop/petclinic/petclinic-deploy.yaml
```

followed by:

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
```

This will cause the containers to be replaced with the local version, you can verify this by checking the containers:

```bash
kubectl describe pods api-gateway |grep Image:
```

The resulting output should say `localhost:9999`:

```text
  Image:         localhost:9999/spring-petclinic-api-gateway:local
```

However, as we only patched the deployment before, the new deployment does not have the right annotations for zero config auto-instrumentation, so let's fix that now by running the patch command again:

Note, that there will be no change for the *config-server & discovery-server* as they do have the annotation included in the deployment.

{{< tabs >}}
{{% tab title="Patch all Petclinic services" %}}

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```

{{% /tab %}}
{{% tab title="kubectl patch Output" %}}

```text
deployment.apps/config-server patched (no change)
deployment.apps/admin-server patched
deployment.apps/customers-service patched
deployment.apps/visits-service patched
deployment.apps/discovery-server patched (no change)
deployment.apps/vets-service patched
deployment.apps/api-gateway patched
```

{{% /tab %}}
{{< /tabs >}}

Let's check the `api-gateway` container again

```bash
kubectl describe pods api-gateway |grep Image:
```

The resulting output should say (again if you see double, it's the old container being terminated, give it a few seconds):

```text
  Image:         ghcr.io/signalfx/splunk-otel-java/splunk-otel-java:v1.30.0
  Image:         localhost:9999/spring-petclinic-api-gateway:local
```
