---
title: Rebuild PetClinic with RUM enabled
linkTitle: 1. Rebuild PetClinic
weight: 1
---

At the top of the previous code snippet, there is a reference to the file `/static/env.js`, which contains/sets the variables used by RUM, currently these are not configured and therefore no RUM traces are currently being sent.

Run the script that will update variables to enable RUM traces so they are viewable in **Splunk Observability Cloud**. Note, that the `env.js` script contains a deliberate JavaScript error, that will be picked up in RUM:

{{< tabs >}}
{{% tab title="Update env.js for RUM" %}}

``` bash
. ~/workshop/petclinic/scripts/push_env.sh
```

{{% /tab %}}
{{% tab title=" Output" %}}

```text
Repository directory exists.
JavaScript file generated at: /home/splunk/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/env.js
```

{{% /tab %}}
{{< /tabs >}}

Verify if the `env.js` has been created correctly:

{{< tabs >}}
{{% tab title="cat env.js" %}}

``` bash
cat ~/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/scripts/env.js
```

{{% /tab %}}
{{% tab title=" Output" %}}

``` javascript
 env = {
  RUM_REALM: 'eu0',
  RUM_AUTH: '[redacted]',
  RUM_APP_NAME: 'k8s-petclinic-workshop-store',
  RUM_ENVIRONMENT: 'k8s-petclinic-workshop-workshop'

}
```

{{% /tab %}}
{{< /tabs >}}

Change into the `api-gateway` directory and force a new build for just the `api-gateway` service:

{{< tabs >}}
{{% tab title="Building api-gateway" %}}

``` bash
cd  ~/spring-petclinic-microservices/spring-petclinic-api-gateway
../mvnw clean install -D skipTests -P buildDocker
```

{{% /tab %}}
{{% tab title=" Output" %}}

```text
Successfully built 2d409c1eeccc
Successfully tagged localhost:9999/spring-petclinic-api-gateway:local
[INFO] Built localhost:9999/spring-petclinic-api-gateway:local
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 26.250 s
[INFO] Finished at: 2024-05-31T15:51:20Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

and now push the new container to the local registry, the others get skipped:

{{< tabs >}}
{{% tab title="Updating docker repo with RUM api-gateway" %}}

``` bash
. ~/workshop/petclinic/scripts/push_docker.sh
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
The push refers to repository [localhost:9999/spring-petclinic-api-gateway]
9a7b16677cf9: Pushed
f2e09ed98998: Layer already exists
291752eeb66b: Layer already exists
ac28fe526c24: Layer already exists
0a37fe4a02de: Layer already exists
4b1e7b998de9: Layer already exists
a2a8ef39e636: Layer already exists
86cb6a9eb3cd: Layer already exists
985fdc63de98: Layer already exists
4ab2850febd7: Layer already exists
2db7720a8970: Layer already exists
629ca62fb7c7: Layer already exists
```

{{% /tab %}}
{{< /tabs >}}

As soon as the container is pushed into the repository, just restart the `api-gateway` to apply the changes:

{{< tabs >}}
{{% tab title="Rollout restart api-gateway" %}}

``` bash
kubectl rollout restart deployment api-gateway
```

{{% /tab %}}
{{% tab title=" Output" %}}

```text
deployment.apps/api-gateway restarted
```

{{% /tab %}}
{{< /tabs >}}

Validate that the application is running by visiting **http://<IP_ADDRESS>:81** (replace **<IP_ADDRESS>** with the IP address you obtained above). Make sure the application is working correctly by visiting the **All Owners** **(1)** and select an owner, then add a **visit** **(2)**.  We will use this action when checking RUM 

![pet](../../images/petclinic-pet.png)

If you want, you can access this website on your phone/tablet as well as this data will also show up in RUM.
