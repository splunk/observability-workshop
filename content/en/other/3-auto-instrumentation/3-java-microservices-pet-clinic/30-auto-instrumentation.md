---
title: Setting up Auto instrumentation for APM
linkTitle: 3. Auto-instrumentation & APM
weight: 30
---

## 1. setting up the Java auto instrumentation

Patch all the deployments (labeled with `app.kubernetes.io/part-of=spring-petclinic`) to add the inject annotation.
 **This automatically causes pods to restart.**

```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"true\"}}}}}"
```

Next, run the script that will use the `maven` command to compile/build the PetClinic microservices:
{{< tabs >}}
{{% tab title="Running maven" %}}

```bash
./mvnw clean install -DskipTests #-P buildDocker
```

{{% /tab %}}
{{% tab title="Maven Output" %}}

```text

Successfully tagged quay.io/phagen/spring-petclinic-api-gateway:latest
[INFO] Built quay.io/phagen/spring-petclinic-api-gateway
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] spring-petclinic-microservices 0.0.1 ............... SUCCESS [  0.770 s]
[INFO] spring-petclinic-admin-server ...................... SUCCESS [01:03 min]
[INFO] spring-petclinic-customers-service ................. SUCCESS [ 29.031 s]
[INFO] spring-petclinic-vets-service ...................... SUCCESS [ 22.145 s]
[INFO] spring-petclinic-visits-service .................... SUCCESS [ 20.451 s]
[INFO] spring-petclinic-config-server ..................... SUCCESS [ 12.260 s]
[INFO] spring-petclinic-discovery-server .................. SUCCESS [ 14.174 s]
[INFO] spring-petclinic-api-gateway 0.0.1 ................. SUCCESS [ 29.832 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 03:14 min
[INFO] Finished at: 2024-01-02T12:43:20Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

{{% notice style="info" %}}
This will take a few minutes the first time you run, `maven` will download a lot of dependencies before it compiles the application. Future builds will be a lot quicker.
{{% /notice %}}

## 3. Check Docker Images

Once the build completes, you need to verify if the containers are indeed built:

{{< tabs >}}
{{% tab title="Check Docker Containers" %}}

```bash
docker images
```

{{% /tab %}}
{{% tab title="Docker Output" %}}

``` text

splunk@show-no-config-i-027057abec7c0c6d3:~/spring-petclinic-microservices$ docker images
REPOSITORY                                          TAG       IMAGE ID       CREATED              SIZE
quay.io/phagen/spring-petclinic-api-gateway         latest    f954254824ed   7 seconds ago        510MB
<none>                                              <none>    5dbbb7d1fbb2   9 seconds ago        563MB
quay.io/phagen/spring-petclinic-discovery-server    latest    0761e73d679d   26 seconds ago       500MB
<none>                                              <none>    d71dc0ff96f4   28 seconds ago       544MB
quay.io/phagen/spring-petclinic-config-server       latest    81a0ab6495c2   39 seconds ago       488MB
<none>                                              <none>    69d60a035bb9   40 seconds ago       519MB
quay.io/phagen/spring-petclinic-visits-service      latest    ca306495bf11   50 seconds ago       526MB
<none>                                              <none>    b60155eb8ab4   52 seconds ago       596MB
quay.io/phagen/spring-petclinic-vets-service        latest    29f1b1909b8b   About a minute ago   527MB
<none>                                              <none>    b07e8de54c99   About a minute ago   598MB
quay.io/phagen/spring-petclinic-customers-service   latest    5b21e448c91e   About a minute ago   526MB
<none>                                              <none>    722fa001614c   About a minute ago   596MB
quay.io/phagen/spring-petclinic-admin-server        latest    4a1906a91210   About a minute ago   498MB
<none>                                              <none>    96f61c7bb66a   About a minute ago   540MB
eclipse-temurin                                     17        807dd649ff14   13 days ago          407MB

```

{{% /tab %}}
{{< /tabs >}}
