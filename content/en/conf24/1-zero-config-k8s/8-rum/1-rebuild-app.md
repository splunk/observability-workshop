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

``` bash
cd  ~/spring-petclinic-microservices/spring-petclinic-api-gateway
../mvnw clean install -D skipTests -P buildDocker
```

and push the new container to the local registry

``` bash
. ~/workshop/petclinic/scripts/push_docker.sh
```

As soon as the container is pushed into the repository, just restart the `api-gateway` to apply the changes:

``` bash
kubectl rollout restart deployment api-gateway
```

Validate that the application is running by visiting **http://<IP_ADDRESS>:81** (replace **<IP_ADDRESS>** with the IP address you obtained above). Make sure the application is working correctly by visiting the **All Owners** **(1)** and select an owner, then add a **visit** **(2)**.  We will use this action when checking RUM 

![pet](../../images/petclinic-pet.png)

If you want, you can access this website on your phone/tablet as well as this data will also show up in RUM.
